from database.mongo import get_db


async def ensure_indexes():
    db = get_db()
    await db.usuarios.create_index("discord_id", unique=True)
    await db.cartas.create_index("nome")
