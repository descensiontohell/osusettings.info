class LeaderboardFilter:
    def __init__(
            self,
            is_mouse: bool = True,
            order_by: str = None,
            min_rank: int = None,
            max_rank: int = None,
            playstyle: list[int] = None,
            page: int = 1,
            name: str = None,
            country: str = None,
            min_edpi: int = None,
            max_edpi: int = None,
            min_area_width: int = None,
            min_area_height: int = None,
            max_area_width: int = None,
            max_area_height: int = None,
            mouse: str = None,
            mousepad: str = None,
            tablet: str = None,
            keyboard: str = None,
            switch: str = None,

    ):
        self.is_mouse: bool = is_mouse
        self.order_by: str = order_by
        self.min_rank: int = min_rank
        self.max_rank: int = max_rank
        self.playstyle: list[int] = playstyle
        self.page: int = page
        self.name: str = name
        self.country: str = country
        self.min_edpi: int = min_edpi
        self.max_edpi: int = max_edpi
        self.min_area_width: int = min_area_width
        self.min_area_height: int = min_area_height
        self.max_area_width: int = max_area_width
        self.max_area_height: int = max_area_height
        self.mouse: str = mouse
        self.mousepad: str = mousepad
        self.tablet: str = tablet
        self.keyboard: str = keyboard
        self.switch: str = switch
