from dataclasses import dataclass


@dataclass
class PlayerStats:
    name: str = None
    osu_id: int = None
    global_rank: int = None
    performance: int = None
    is_restricted: bool = None
