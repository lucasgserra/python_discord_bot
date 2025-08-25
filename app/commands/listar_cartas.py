import discord
from discord import app_commands
from service import user_service

print("[listar_cartas] módulo carregado de:", __file__)


def setup(tree: app_commands.CommandTree, guild_id: int | None = None) -> None:
    if guild_id:

        @tree.command(
            name="cartas",
            description="Veja suas cartas já adquiridas",
            guild=discord.Object(id=guild_id),
        )
        async def ping(interaction: discord.Interaction):
            response = await user_service.get_cards(interaction.user.id)
            await interaction.response.send_message(response, ephemeral=True)

    else:

        @tree.command(name="cartas", description="Veja suas cartas já adquiridas")
        async def ping(interaction: discord.Interaction):
            response = await user_service.get_cards(interaction.user.id)
            await interaction.response.send_message(response, ephemeral=True)
