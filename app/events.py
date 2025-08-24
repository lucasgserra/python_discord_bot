import discord

def register_events(client: discord.Client)->None:

    @client.event
    async def on_ready():
        print(f'we have logged in as {client.user}')
        if len(client.guilds) == 0:
            print("warning: the bot is not in any guilds")
            await client.close()
            return;
        else:
            await client.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game("with Pyhton"))
    