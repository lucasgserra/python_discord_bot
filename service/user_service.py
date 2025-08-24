from database.user_repo import create_user, get_user, remove_user_db
from app.send_log_chat import send_message
import discord


async def ensure_user_exists(discord_id: int, guild: discord.Guild):
    user = await get_user(discord_id)
    if not user:
        await create_user(discord_id)
        await send_message(
            message=f"Novo usuario cadastrado no banco de dados! {discord_id}", guild=guild
        )
    return user


async def remove_user(discord_id: int, guild: discord.Guild):
    user = await get_user(discord_id)
    if user:
        await remove_user_db(discord_id)
        await send_message(message=f"Usuario removido do banco de dados! {discord_id}", guild=guild)
