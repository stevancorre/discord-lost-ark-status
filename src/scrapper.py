from typing import List
from dataclasses import dataclass

from requests_cache import CachedSession, Response
from datetime import timedelta
from bs4 import BeautifulSoup, Tag

from helper import try_getenv

session: CachedSession = CachedSession(
    "dlas_cache",
    expire_after=timedelta(minutes=try_getenv("CACHE_LIFETIME", float)),
    allowable_methods=["GET"],
    allowable_codes=[200],
    stale_if_error=True
)


@dataclass
class Server:
    name: str
    status: str


@dataclass
class ServerRegion:
    name: str
    servers: List[Server]


@dataclass
class ScrapperResult:
    regions: List[ServerRegion]
    last_updated: str


def get_servers_statuses() -> ScrapperResult:
    page: Response = session.get(
        "https://www.playlostark.com/en-gb/support/server-status")
    soup: BeautifulSoup = BeautifulSoup(page.content, features="html.parser")

    server_regions: List[ServerRegion] = __extract_server_regions(soup)
    last_updated: str = __extract_last_updated_date(soup)
    return ScrapperResult(server_regions, last_updated)


def __extract_server_regions(root: BeautifulSoup) -> List[ServerRegion]:
    server_regions: List[ServerRegion] = []
    region_tags: List[Tag] = root.find_all(
        "a", class_="ags-ServerStatus-content-tabs-tabHeading")

    for group in region_tags:
        name: str = group.text.strip()
        data_index: str = group.attrs.get("data-index")
        servers: List[Server] = __extract_servers(root, data_index)

        server_regions.append(ServerRegion(name, servers))

    return server_regions


def __extract_servers(root: BeautifulSoup, data_index: str) -> List[Server]:
    servers: List[Server] = []
    server_tags_wrapper: Tag = root.find(
        "div", class_="ags-ServerStatus-content-responses-response", attrs={"data-index": data_index})
    server_tags: List[Tag] = server_tags_wrapper.find_all(
        "div", class_="ags-ServerStatus-content-responses-response-server")

    for server_tag in server_tags:
        servers.append(__extract_server_data(server_tag))

    return servers


def __extract_server_data(server_tag: Tag) -> Server:
    # get name
    name_container: Tag = server_tag.find(
        "div", class_="ags-ServerStatus-content-responses-response-server-name")
    name: str = name_container.text.strip()

    status_container: Tag = server_tag.find(
        "div", class_="ags-ServerStatus-content-responses-response-server-status")
    # looks like `ags-ServerStatus-content-responses-response-server-status--XXXXX`
    status: str = status_container.attrs.get("class")[1].split("--")[1]

    return Server(name, status)


def __extract_last_updated_date(root: BeautifulSoup) -> str:
    return root.find("div", class_="ags-ServerStatus-content-lastUpdated").text.strip().replace("&#39;", "'")
