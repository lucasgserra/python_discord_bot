from mongo import get_db
import uuid


async def create_user(nome: str):
    db = get_db()
    user_id = str(uuid.uuid4())

    await db.usuarios.insert_one(
        {
            "_id": user_id,
            "nome": nome,
            "cartas": [],
            "xp": 0,
        }
    )
    return user_id


async def get_user(nome: str):
    db = get_db()
    return await db.usuarios.find_one({"nome": nome})
