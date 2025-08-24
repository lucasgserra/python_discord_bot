import os
from dataclasses import dataclass
from dotenv import load_dotenv
import discord

load_dotenv()


@dataclass(frozen=True)
class Settings:
    token: str


def get_owner_id() -> int:
    owner_id = os.getenv("OWNER_ID")
    if not owner_id:
        raise RuntimeError("owner ID not defined")
    return int(owner_id)


def get_settings() -> Settings:
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        raise RuntimeError("discord token not defined")
    return Settings(token=token)


def get_intents() -> discord.Intents:
    intents = discord.Intents.default()
    intents.members = True
    intents.guilds = True
    return intents
