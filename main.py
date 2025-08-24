from config.settings import get_settings, get_intents
from app.initial_events import register_events
import discord

settings = get_settings()
intents = get_intents()
client = discord.Client(intents=intents)

register_events(client)

client.run(settings.token)
