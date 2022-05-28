from dataclasses import dataclass
from typing import Optional


@dataclass
class PlayerEdpi:
    osu_id: int
    edpi: Optional[int]
    area_width: Optional[int]
    area_height: Optional[int]

    def to_dict(self):
        return {
            "mouse_edpi": self.edpi,
            "play_area_width": self.area_width,
            "play_area_height": self.area_height,
        }
