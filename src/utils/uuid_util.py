import random
import uuid
import time

class UuidUtil:
    """UUID Utils"""
    
    # ─── UUID v7 ──────────────────────────────────────────────────────────────────
    @staticmethod
    def uuid_v7() -> str:
        timestamp_ms = int(time.time() * 1000)
        rand_a = random.getrandbits(12)
        rand_b = random.getrandbits(62)
        msb = (timestamp_ms << 16) | (7 << 12) | rand_a
        lsb = rand_b | (0b10 << 62)
        return str(uuid.UUID(int=(msb << 64) | lsb))