from database.mongo import get_db
from models import Carta


async def get_carta(card_id: str):
    db = get_db()
    return await db.cartas.find_one({"_id": card_id})


async def list_cartas(filter_: dict | None = None, limit: int = 50):
    db = get_db()
    cursor = db.carta.find(filter_ or {}).limit(limit)
    return [doc async for doc in cursor]


async def upsert_card(card: Carta):
    db = get_db()
    _id = card["_id"]
    await db.cartas.update_one({"_id": _id}, {"$set": card}, upsert=True)
    return _id
