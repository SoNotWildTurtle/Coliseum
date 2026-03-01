"""Tests for additional managers."""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from hololive_coliseum.auth_manager import AuthManager
from hololive_coliseum.cheat_detection_manager import CheatDetectionManager
from hololive_coliseum.ban_manager import BanManager
from hololive_coliseum.data_protection_manager import DataProtectionManager
from hololive_coliseum.logging_manager import LoggingManager
from hololive_coliseum.ui_manager import UIManager
from hololive_coliseum.notification_manager import NotificationManager
from hololive_coliseum.input_manager import InputManager
from hololive_coliseum.accessibility_manager import AccessibilityManager
from hololive_coliseum.chat_manager import ChatManager
from hololive_coliseum.voice_chat_manager import VoiceChatManager
from hololive_coliseum.emote_manager import EmoteManager
from hololive_coliseum.sound_manager import SoundManager
from hololive_coliseum.effect_manager import EffectManager


def test_auth_and_ban_managers():
    auth = AuthManager()
    auth.register('u', 'p')
    assert auth.users['u']['hash'] != 'p'
    token = auth.login('u', 'p')
    assert token and auth.verify(token)
    ban = BanManager()
    ban.ban('u')
    assert ban.is_banned('u')
    ban.unban('u')
    assert not ban.is_banned('u')


def test_auth_login_limit():
    """Ensure repeated failures lock the account."""
    auth = AuthManager()
    auth.register('x', 'y')
    for _ in range(3):
        assert auth.login('x', 'bad') is None
    assert auth.login('x', 'y') is None


def test_auth_token_expiry():
    """Tokens should expire after the configured lifetime."""
    t = [0]
    auth = AuthManager(token_lifetime=1, time_func=lambda: t[0])
    auth.register('u', 'p')
    token = auth.login('u', 'p')
    assert token and auth.verify(token)
    t[0] = 2
    assert not auth.verify(token)


def test_auth_logout():
    """Logout should invalidate the session token."""
    auth = AuthManager()
    auth.register('u', 'p')
    token = auth.login('u', 'p')
    assert token
    auth.logout(token)
    assert not auth.verify(token)


def test_cheat_detection_and_logging():
    cheat = CheatDetectionManager()
    log = LoggingManager()
    if cheat.check_speed(11, 10):
        log.log('speed')
    assert log.events == ['speed']


def test_data_protection_roundtrip():
    dp = DataProtectionManager(b'k')
    enc = dp.encrypt(b'abc')
    assert dp.decrypt(enc) == b'abc'


def test_data_protection_packet():
    dp = DataProtectionManager(b'k', secret=b's')
    packet = dp.encode({'x': 1})
    out = dp.decode(packet)
    assert out == {'x': 1}


def test_data_protection_replay():
    dp = DataProtectionManager(b'k', secret=b's')
    packet = dp.encode({'x': 2})
    assert dp.decode(packet) == {'x': 2}
    # second decode should be rejected due to nonce replay
    assert dp.decode(packet) is None


def test_data_protection_expiry():
    t = [0]
    dp = DataProtectionManager(b"k", secret=b"s", time_func=lambda: t[0], max_age=1)
    packet = dp.encode({"x": 3})
    t[0] = 2
    assert dp.decode(packet) is None


def test_data_protection_sanitization():
    dp = DataProtectionManager(sanitize_fields={"password"})
    packet = dp.encode({"x": 1, "password": "secret"})
    out = dp.decode(packet)
    assert out == {"x": 1} and "password" not in out


def test_data_protection_rotate_keys():
    dp = DataProtectionManager(b"old", secret=b"so")
    pkt1 = dp.encode({"v": 1})
    assert dp.decode(pkt1) == {"v": 1}
    dp.rotate_keys(b"new", b"sn")
    assert dp.decode(pkt1) is None
    pkt2 = dp.encode({"v": 2})
    assert dp.decode(pkt2) == {"v": 2}


def test_ui_and_notification_managers():
    ui = UIManager()
    ui.add('menu')
    ui.remove('menu')
    assert not ui.elements
    nm = NotificationManager()
    nm.push('hi')
    assert nm.pop() == 'hi'


def test_input_and_accessibility():
    class Joy:
        def __init__(self) -> None:
            self.pressed: set[int] = set()

        def get_button(self, btn: int) -> bool:
            return btn in self.pressed

    joy = Joy()
    im = InputManager({'jump': 1}, {'jump': 0}, [joy], mode='keyboard')
    assert im.get('jump') == 1
    im.set('fire', 2)
    assert im.get('fire') == 2
    keys = [0] * 10
    keys[2] = 1
    im.set('dash', 2)
    assert im.pressed('dash', keys)
    im.set_mode('controller')
    assert not im.pressed('dash', keys)
    joy.pressed.add(0)
    assert im.pressed('jump', keys)
    am = AccessibilityManager()
    orig = am.options['colorblind']
    am.toggle('colorblind')
    assert am.options['colorblind'] != orig


def test_chat_and_voice_managers():
    chat = ChatManager(max_messages=2)
    chat.show()
    assert chat.open
    chat.send('a', 'hi')
    chat.send('b', 'yo')
    chat.send('c', 'hey')
    assert chat.history() == [('b', 'yo'), ('c', 'hey')]
    chat.hide()
    assert not chat.open
    voice = VoiceChatManager()
    voice.join('a', 'c1')
    assert 'a' in voice.channels['c1']
    voice.leave('a', 'c1')
    assert 'c1' not in voice.channels


def test_emote_sound_effect():
    em = EmoteManager()
    em.add('smile', ':)')
    assert em.get('smile') == ':)'
    sound = SoundManager(volume=0.0)
    sound.play('ding')
    assert sound.last_played == 'ding'
    sound.stop()
    assert sound.last_played is None
    sound.cycle_volume()
    assert sound.volume == 0.5
    effect = EffectManager()
    effect.trigger('boom')
    assert 'boom' in effect.active
