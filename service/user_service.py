from database.user_repo import create_user, get_user, remove_user_db, get_user_cards
from app.send_log_chat import send_message
import discord
from typing import List, Union
from models import Card


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

async def get_cards(discord_id: int) -> str:
    cards: List[Card] = await get_user_cards(discord_id)
    if not cards:
        return "Você não possui cartas cadastradas."
    nomes = ", ".join(getattr(c, "nome", c.get("nome", "?")) for c in cards)
    return f"Suas cartas: {nomes}"