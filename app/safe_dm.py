import discord
from discord import Member

async def safe_dm(member: Member, *, content: str | None = None, embed: discord.Embed | None = None):
    try:
        await member.send(content=content, embed=embed, allowed_mentions=discord.AllowedMentions.none())
        return True
    except discord.Forbidden:
        return False
    except discord.HTTPException:
        return False