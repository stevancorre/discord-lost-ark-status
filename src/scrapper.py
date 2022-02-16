from typing import List, Optional
from functools import lru_cache
from dataclasses import dataclass

from requests_cache import CachedSession, Response
from datetime import timedelta
from bs4 import BeautifulSoup, Tag

from helper import try_getenv

# Cached session to avoid spamming playlostark.com
# Btw no need to spam them since server statuses aren't updated
# in real time
session: CachedSession = CachedSession(
    "dlas_cache",
    expire_after=timedelta(minutes=try_getenv("CACHE_LIFETIME", float)),
    allowable_methods=["GET"],
    allowable_codes=[200],
    stale_if_error=True
)


@dataclass
class Server:
    """Describes a server"""

    name: str
    status: str


@dataclass
class ServerRegion:
    """Describes a region"""

    name: str
    servers: List[Server]


@dataclass
class ScrapperResult:
    """Describes the result of the scrapper"""

    regions: List[ServerRegion]
    last_updated: str


@lru_cache
def get_servers_statuses(ttl_hash: Optional[int] = None) -> ScrapperResult:
    """Get all server statuses"""

    del ttl_hash

    # Fetch the page and parse it
    page: Response = session.get(
        "https://www.playlostark.com/en-gb/support/server-status")
    soup: BeautifulSoup = BeautifulSoup(page.content, features="html.parser")

    # Then, extract everything we need and we're done
    server_regions: List[ServerRegion] = __extract_server_regions(soup)
    last_updated: str = __extract_last_updated_date(soup)
    return ScrapperResult(server_regions, last_updated)


def __extract_server_regions(root: BeautifulSoup) -> List[ServerRegion]:
    """Extracts all regions from a parsed html page"""

    server_regions: List[ServerRegion] = []
    region_tags: List[Tag] = root.find_all(
        "a", class_="ags-ServerStatus-content-tabs-tabHeading")

    for group in region_tags:
        name: str = group.text.strip()

        # Datas are stored with a `data-index` (e.g: Central Europe has a data index of 2, so all
        # servers are going to be wrapped in a div with the same `data-index`, that's how we can
        # find which server belongs to which region)
        # This technique is future proof too. Well, at least if they don't change everything.
        data_index: str = group.attrs.get("data-index")
        servers: List[Server] = __extract_servers(root, data_index)

        server_regions.append(ServerRegion(name, servers))

    return server_regions


def __extract_servers(root: BeautifulSoup, data_index: str) -> List[Server]:
    """Extracts all servers from a parsed html page, giving a specific data index"""

    servers: List[Server] = []

    # As explained in `__extract_server_regions`, datas are stored with a `data-index`. So all servers
    # with a data-index of N belong to the region with the data-index N
    # Btw, only the wrapper has this attribute, so we first get it, then just fetch its children
    server_tags_wrapper: Tag = root.find(
        "div", class_="ags-ServerStatus-content-responses-response", attrs={"data-index": data_index})
    server_tags: List[Tag] = server_tags_wrapper.find_all(
        "div", class_="ags-ServerStatus-content-responses-response-server")

    for server_tag in server_tags:
        servers.append(__extract_server_data(server_tag))

    return servers


def __extract_server_data(server_tag: Tag) -> Server:
    """Extracts server data from a server div (in the html)"""

    # Get name
    name_container: Tag = server_tag.find(
        "div", class_="ags-ServerStatus-content-responses-response-server-name")
    name: str = name_container.text.strip()

    status_container: Tag = server_tag.find(
        "div", class_="ags-ServerStatus-content-responses-response-server-status")
    # Looks like `ags-ServerStatus-content-responses-response-server-status--XXXXX`
    status: str = status_container.attrs.get("class")[1].split("--")[1]

    return Server(name, status)


def __extract_last_updated_date(root: BeautifulSoup) -> str:
    """Extracts the text that says when the server statuses were updated"""

    last_updated: str = root.find(
        "div", class_="ags-ServerStatus-content-lastUpdated").text
    return last_updated.strip().replace("&#39;", "'")
