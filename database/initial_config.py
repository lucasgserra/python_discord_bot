from discord import Client, PermissionOverwrite
import discord


async def start(client: Client) -> None:

    guilds = client.guilds

    for guild in guilds:
        overwrites = {guild.default_role: PermissionOverwrite(view_channel=False)}
        logs_db_channel = discord.utils.get(guild.text_channels, name="logs-db")

        if logs_db_channel is None:
            await guild.create_text_channel("logs-db", overwrites=overwrites)
        else:
            await logs_db_channel.edit(overwrites=overwrites)

        await logs_db_channel.send("Canal de logs do banco de dados criado ou atualizado")
