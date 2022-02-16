from typing import Dict, List

from nextcord import Embed, Color

from scrapper import ServerRegion, Server

COL_COUNT = 3

STATUS_ICONS: Dict[str, str] = {
    "good": ":white_check_mark:",
    "busy": ":clock1:",
    "full": ":no_entry:",
    "maintenance": ":construction:"
}

STATUS_WEIGHTS: Dict[str, float] = {
    "good": 1,
    "busy": 0.3,
    "full": 0,
    "maintenance": 0
}


class ServerStatusEmbed(Embed):
    def __init__(self, region: ServerRegion, last_updated: str):
        super().__init__()

        self.title = "Lost Ark servers status"
        self.url = "https://www.playlostark.com/en-gb/support/server-status"

        self.set_thumbnail(url="https://i.imgur.com/J42CmnO.jpg")
        self.set_footer(text=last_updated)

        self.__init_color(region.servers)

        self.__init_fields(region.name, region.servers)

    def __init_color(self, servers: List[Server]):
        # get color (lerp green -> orange -> red)
        server_count = len(servers)
        server_ok_count: float = sum(
            [STATUS_WEIGHTS[server.status] for server in servers])
        server_ok_p = 1 - (server_ok_count / server_count)

        color: Color =  \
            Color(color_lerp(0x2ecc71, 0xe67e22, server_ok_p)) if server_ok_p < 0.5 else \
            Color(color_lerp(0xe67e22, 0xe74c3c, server_ok_p))

        self.colour = color

    def __init_fields(self, region_name: str, servers: List[Server]):
        cols: List[str] = [""] * COL_COUNT
        for i, server in enumerate(servers):
            cols[i % COL_COUNT] += f"{format_server_with_status(server)}\n"

        is_first_col: bool = True
        for col in cols:
            name: str = "_ _"
            if is_first_col:
                name = region_name
                is_first_col = False

            self.add_field(name=name, value=col)


def format_server_with_status(server: Server) -> str:
    icon: str = STATUS_ICONS[server.status]

    if server.status == "good":
        return f"{icon} {server.name}"
    elif server.status == "busy":
        return f"{icon} *{server.name}*"
    else:
        return f"{icon} ~~{server.name}~~"


def color_lerp(a: int, b: int, t: float) -> int:
    ra: int = (a >> 16) & 0xff
    ga: int = (a >> 8) & 0xff
    ba: int = a & 0xff

    rb: int = (b >> 16) & 0xff
    gb: int = (b >> 8) & 0xff
    bb: int = b & 0xff

    rc: int = round(((rb - ra) * t + ra)) << 16
    gc: int = round(((gb - ga) * t + ga)) << 8
    bc: int = round(((bb - ba) * t + ba))

    return rc | gc | bc
