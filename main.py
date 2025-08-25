from config.settings import get_settings, get_intents, get_main_guild_id
from app.initial_events import register_events
import discord

settings = get_settings()
intents = get_intents()
client = discord.Client(intents=intents)
GUILD_ID = get_main_guild_id()


register_events(client)

client.run(settings.token)
