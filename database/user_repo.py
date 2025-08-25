from database.mongo import get_db
from models import Card, User
from typing import List
import uuid


async def create_user(discord_id: int):
    db = get_db()
    user_id = str(uuid.uuid4())

    await db.usuarios.insert_one(
        {
            "_id": user_id,
            "discord_id": discord_id,
            "cartas": [],
            "xp": 0,
        }
    )
    return user_id


async def get_user(discord_id: int) -> User | None:
    db = get_db()
    return await db.usuarios.find_one({"discord_id": discord_id})


async def remove_user_db(discord_id: int):
    db = get_db()
    result = await db.usuarios.delete_one({"discord_id": discord_id})
    return result.deleted_count > 0


### card manager


async def add_card_to_user(discord_id: int, card_id: str) -> bool:
    db = get_db()
    result = await db.usuarios.update_one(
        {"discord_id": discord_id},
        {"$addToSet": {"cartas": card_id}},
    )
    return result.modified_count == 1


async def add_cards_to_user(discord_id: int, card_ids: list[str]) -> int:
    if not card_ids:
        return 0
    db = get_db()
    result = await db.usuarios.update_one(
        {"discord_id": discord_id},
        {"$addToSet": {"cartas": {"$each": card_ids}}},
    )
    return result.modified_count


async def remove_card_from_user(discord_id: int, card_id: str) -> bool:
    db = get_db()
    result = await db.usuarios.update_one(
        {"discord_id": discord_id},
        {"$pull": {"cartas": card_id}},
    )
    return result.modified_count == 1


async def user_has_card(discord_id: int, card_id: str) -> bool:
    db = get_db()
    doc = await db.usuarios.find_one(
        {"discord_id": discord_id, "cartas": card_id},
        {"_id": 1},
    )
    return doc is not None

async def get_user_cards(discord_id: int) -> List[Card]:
    db = get_db()
    user = await db.usuarios.find_one({"discord_id": discord_id}, {"cartas": 1})
    if not user or not user.get("cartas"):
        return []
    card_ids = user["cartas"]
    cursor = db.cartas.find({"_id": {"$in": card_ids}})
    return [Card(**doc) async for doc in cursor]