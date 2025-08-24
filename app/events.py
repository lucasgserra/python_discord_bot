import discord

def register_events(client: discord.Client)->None:

    @client.event
    async def on_ready():
        print(f'we have logged in as {client.user}')