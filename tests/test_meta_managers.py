"""Tests for meta managers."""

from hololive_coliseum.replay_manager import ReplayManager
from hololive_coliseum.bot_manager import BotManager
from hololive_coliseum.telemetry_manager import TelemetryManager
from hololive_coliseum.ai_moderation_manager import AIModerationManager
from hololive_coliseum.dynamic_content_manager import DynamicContentManager
from hololive_coliseum.geo_manager import GeoManager
from hololive_coliseum.device_manager import DeviceManager
from hololive_coliseum.season_manager import SeasonManager
from hololive_coliseum.daily_task_manager import DailyTaskManager
from hololive_coliseum.weekly_manager import WeeklyManager
from hololive_coliseum.tutorial_manager import TutorialManager
from hololive_coliseum.onboarding_manager import OnboardingManager
from hololive_coliseum.arena_manager import ArenaManager
from hololive_coliseum.war_manager import WarManager
from hololive_coliseum.tournament_manager import TournamentManager
from hololive_coliseum.raid_manager import RaidManager
from hololive_coliseum.party_manager import PartyManager


def test_replay_manager():
    rm = ReplayManager()
    rm.record({'win': True})
    assert rm.list_replays() == [{'win': True}]


def test_bot_and_telemetry():
    bm = BotManager()
    tm = TelemetryManager()
    bm.add_bot('cpu')
    tm.log('jump')
    assert bm.list_bots() == ['cpu']
    assert tm.get_events() == ['jump']


def test_ai_moderation_and_dynamic_content():
    aim = AIModerationManager({'bad'})
    dcm = DynamicContentManager()
    assert aim.check('bad word')
    cid = dcm.create('quest')
    assert dcm.list_content()[cid] == 'quest'


def test_geo_and_device():
    gm = GeoManager()
    dm = DeviceManager()
    gm.update(1.0, 2.0)
    dm.register('haptic', {'type': 'pad'})
    assert gm.last() == (1.0, 2.0)
    assert dm.get('haptic')['type'] == 'pad'


def test_season_and_tasks():
    sm = SeasonManager()
    dt = DailyTaskManager()
    wk = WeeklyManager()
    sm.next_season()
    dt.add_task('a')
    wk.add('b')
    dt.complete('a')
    wk.complete('b')
    dt.reset()
    wk.reset()
    assert sm.current() == 2
    assert dt.tasks['a'] is False
    assert wk.challenges['b'] is False


def test_tutorial_and_onboarding():
    tm = TutorialManager()
    om = OnboardingManager()
    tm.complete_step('move')
    om.show('welcome')
    assert tm.progress() == ['move']
    assert om.history() == ['welcome']


def test_competition_managers():
    arena = ArenaManager()
    war = WarManager()
    tourn = TournamentManager()
    raid = RaidManager()
    party = PartyManager()
    arena.record_win('p1')
    war.add_points('f1', 5)
    tourn.create_bracket(['a', 'b'])
    raid.create_group(['x', 'y'])
    party.create_party('h')
    party.join('h', 'i')
    assert arena.top_player() == 'p1'
    assert war.leading() == 'f1'
    assert tourn.list_brackets()[0] == ['a', 'b']
    assert raid.list_groups()[0] == ['x', 'y']
    assert party.get_party('h') == ['h', 'i']
