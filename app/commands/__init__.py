from discord import app_commands
from app.commands import listar_cartas


def setup_commands(tree: app_commands.CommandTree, guild_id: int | None = None) -> None:
    print("[commands.__init__] setup_commands chamado. guild_id=", guild_id)
    listar_cartas.setup(tree, guild_id=guild_id)
