from dataclasses import dataclass


@dataclass
class PlayerStats:
    osu_id: int
    is_restricted: bool
    is_active: bool = None
    name: str = None
    global_rank: int = None
    performance: int = None

    def to_dict(self):
        base_dict = {"is_restricted": self.is_restricted}

        if self.is_active:
            base_dict["is_active"] = self.is_active
        if self.name:
            base_dict["name"] = self.name
        if self.global_rank:
            base_dict["global_rank"] = self.global_rank
        if self.performance:
            base_dict["performance"] = self.performance

        return base_dict
