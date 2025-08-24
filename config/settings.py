import os
from dataclasses import dataclass
from dotenv import load_dotenv
import discord

load_dotenv()

@dataclass(frozen=True)
class Settings:
    token: str

def get_settings() -> Settings:
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        raise RuntimeError("Discord token not defined")
    return Settings(token=token)

def get_intents() -> discord.Intents:
    intents = discord.Intents.default()
    return intents