import aiosqlite
from typing import AsyncGenerator
from .config import get_settings

settings = get_settings()

async def get_db() -> AsyncGenerator[aiosqlite.Connection, None]:
    conn = await aiosqlite.connect(settings.database_url)
    try:
        yield conn
    finally:
        await conn.close()

async def init_db() -> None:
    async with get_db() as conn:
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS incidents (
                id TEXT PRIMARY KEY,
                timestamp TEXT NOT NULL,
                source TEXT NOT NULL,
                severity TEXT NOT NULL,
                description TEXT NOT NULL,
                resolved BOOLEAN NOT NULL DEFAULT FALSE,
                affected_services TEXT NOT NULL
            )
        ''')
        await conn.commit()