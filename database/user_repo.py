from database.mongo import get_db
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


async def get_user(discord_id: int):
    db = get_db()
    return await db.usuarios.find_one({"discord_id": discord_id})


async def remove_user_db(discord_id: int):
    db = get_db()
    result = await db.usuarios.delete_one({"discord_id": discord_id})
    return result.deleted_count > 0
