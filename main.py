import discord
import os
from dotenv import load_dotenv

load_dotenv()

token = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'bot has started was {client.user}')

client.run(token)