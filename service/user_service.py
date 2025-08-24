from database.user_repo import create_user, get_user


async def ensure_user_exists(nome: str):
    user = await get_user(nome)
    if not user:
        await create_user(nome)
    return user
