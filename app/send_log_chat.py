import discord


async def send_message(message: str, guild: discord.Guild):
    log_channel = discord.utils.get(guild.text_channels, name="logs-db")
    if log_channel:
        await log_channel.send(message)
