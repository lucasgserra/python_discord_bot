import discord
from discord import Member
from config.settings import get_owner_id
from app.setup import create_roles
from app.safe_dm import safe_dm
from database.initial_config import start
from database.indexes import ensure_indexes
from datetime import datetime
from database.mongo import get_db, close_client
from service.user_service import ensure_user_exists, remove_user
from config.settings import get_main_guild_id
from discord import app_commands
from app.commands import setup_commands
from service import user_service

GUILD_ID = get_main_guild_id()

def register_events(client: discord.Client) -> None:
    tree = app_commands.CommandTree(client)
    setup_commands(tree, guild_id=get_main_guild_id())

    @client.event
    async def on_ready():
        await get_db().command("ping")
        await ensure_indexes()

        if GUILD_ID:
            guild = discord.Object(id=GUILD_ID)
            await tree.sync(guild=guild)
            print(f"slash commands sincronizados para a guild {GUILD_ID}")
        else:
            try:
                await tree.sync()
                print("slash commands sincronizados globalmente")
            except Exception as e:
                print("falha ao sincronizar slash commands:", e)

            await client.change_presence(
                status=discord.Status.do_not_disturb, activity=discord.Game("a vida fora")
            )

        print(f"bot logado como: {client.user}")
        owner_id = get_owner_id()
        if len(client.guilds) == 0:
            print("aviso: bot nao esta em nenhum servidor. encerrando servicos")
            await client.close()
            return
        for guild in client.guilds:
            if guild.owner_id != owner_id:
                await guild.leave()
                print(f"saindo da guilda {guild.name} pois nao sou o dono dela")
            else:

                await create_roles(guild)
                await start(client)
                jogador = discord.utils.get(guild.roles, name="Jogador")
                adm = discord.utils.get(guild.roles, name="Administrador")
                for member in guild.members:
                    exists_user = await user_service.get_user(member.id)
                    if not exists_user:
                        await ensure_user_exists(member.id, guild)

                    if member.bot:
                        continue
                    if member.id == owner_id:
                        await member.add_roles(adm)
                    else:
                        if jogador not in member.roles:
                            try:
                                await member.add_roles(jogador)
                                print(f"{member.name} adicionado como {jogador.name}")
                            except discord.Forbidden:
                                print(
                                    f"sem permissao para adicionar {jogador.name} a {member.name}"
                                )
                            except discord.HTTPException as e:
                                print(f"falha ao adicionar role para {member.name}: {e}")

    @client.event
    async def on_close():
        await close_client()

    @client.event
    async def on_member_remove(member: Member):
        if member.bot:
            return
        await remove_user(member.id, member.guild)

    @client.event
    async def on_member_join(member: Member):
        if member.bot:
            return
        await ensure_user_exists(member.id, member.guild)
        jogador = discord.utils.get(member.guild.roles, name="Jogador")
        if jogador:
            try:
                await member.add_roles(jogador)

                embed = discord.Embed(
                    title=f"Bem-vindo(a) {member.name}! 👋",
                    description=(
                        "Vamos iniciar sua jornada!\n\n"
                        "**Como funciona:**\n"
                        "• Sistema de **lutas por turnos**\n"
                        "• Você **adquire personagens**, **evolui** e **sobe de nível**\n"
                        "• Você possui **XP**, **moedas** e **gemas** para comprar personagens e itens\n"
                    ),
                    color=discord.Color.blurple(),
                    timestamp=datetime.now(),
                )
                embed.set_footer(text="Divirta-se e boa sorte!")
                sent = await safe_dm(member, embed=embed)
                if not sent:
                    print(
                        f"não foi possível enviar DM para {member.name}. DMs podem estar desativadas."
                    )
                print(f"{member.name} adicionado como {jogador.name}")
            except discord.Forbidden:
                print(f"sem permissao para adicionar {jogador.name} a {member.name}")
            except discord.HTTPException as e:
                print(f"falha ao adicionar role para {member.name}: {e}")
