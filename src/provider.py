import asyncio
from functools import lru_cache

import aiosqlite
from datetime import datetime, date

from helper import get_ttl_hash, log
from scrapper import ScrapperResult, scrap_servers_statuses


class DataProvider:
    def __init__(self, db_name: str, cache_lifetime: int) -> None:
        self.db_name = db_name
        self.cache_lifetime = cache_lifetime

        self._loop = asyncio.get_event_loop()

        self._db: aiosqlite.Connection | None = None

        self._uptime_updater = None
        self.__schedule_update()

        self._loop.run_until_complete(self.__init_db())

    async def get_db_connection(self) -> aiosqlite.Connection:
        if self._db is None:
            return await self.__init_db()

        return self._db

    async def __init_db(self) -> aiosqlite.Connection:
        self._db = await aiosqlite.connect(self.db_name)

        async with self._db.cursor() as cursor:
            await cursor.execute("CREATE TABLE IF NOT EXISTS uptime (name varchar(20), time integer, status varchar(12))")
        await self._db.commit()

        log("Database connected")

        return self._db

    @lru_cache
    def get_servers_statuses(self, ttl_hash: int = None) -> ScrapperResult:
        if ttl_hash is None:
            return self.get_servers_statuses(get_ttl_hash(self.cache_lifetime))

        return scrap_servers_statuses()

    @lru_cache
    async def get_servers_uptime(self, ttl_hash: int = None) -> None:
        if ttl_hash is None:
            self.get_servers_uptime(self, get_ttl_hash(self.cache_lifetime))
            return

        raise NotImplementedError()

    def __schedule_update(self) -> None:
        # TODO: for now, called each n seconds -> minutes
        # NOTE: this is just for testing ofc
        self._uptime_updater = self._loop.call_later(
            self.cache_lifetime,
            self._loop.create_task,
            self.__update_servers_uptime())

    async def __update_servers_uptime(self) -> None:
        db: aiosqlite.Connection = await self.get_db_connection()
        data: ScrapperResult = self.get_servers_statuses()

        date = datetime.strptime(
            data.last_updated.upper(), "LAST UPDATED: %d %B %Y %H:%M:%S O'CLOCK PST")
        unix_timestamp: int = int(date.timestamp())

        for region in data.regions:
            for server in region.servers:
                await db.execute("INSERT INTO uptime (name, time, status) VALUES (?, ?, ?)", (server.name, unix_timestamp, server.status))

        await db.commit()

        self.__schedule_update()
