"""Network transmission helpers and retries."""

class TransmissionManager:
    """Helper managing holographic packet compression and decompression.

    Supports ``zlib`` (default), ``bz2``, ``lzma`` or ``auto`` algorithms.
    ``auto`` picks the smallest result between zlib and lzma to limit bandwidth
    and processing requirements.
    """

    def __init__(
        self,
        encrypt_key: bytes | None = None,
        level: int = 6,
        algorithm: str = "zlib",
        sign_key=None,
    ) -> None:
        self.encrypt_key = encrypt_key
        self.level = level
        self.algorithm = algorithm
        self.sign_key = sign_key

    def compress(self, msg):
        from .holographic_compression import compress_packet

        return compress_packet(
            msg,
            key=self.encrypt_key,
            level=self.level,
            algorithm=self.algorithm,
            sign_key=self.sign_key,
        )

    def decompress(self, packet):
        from .holographic_compression import decompress_packet

        return decompress_packet(packet, key=self.encrypt_key)
