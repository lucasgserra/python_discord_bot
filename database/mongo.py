from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from config.settings import get_mongo_url

_client: AsyncIOMotorClient | None = None
_db: AsyncIOMotorDatabase | None = None


def get_client() -> AsyncIOMotorClient:
    global _client
    if _client is None:
        _client = AsyncIOMotorClient(get_mongo_url(), maxPoolSize=50, serverSelectionTimeoutMS=5000)
    return _client


def get_db(name: str = "users") -> AsyncIOMotorDatabase:
    global _db
    if _db is None:
        _db = get_client()[name]
    return _db


async def close_client() -> None:
    global _client
    if _client is not None:
        _client.close()
        _client = None
