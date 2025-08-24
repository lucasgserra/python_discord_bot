import discord
from discord import Member
from config.settings import get_owner_id
from app.setup import create_roles
from app.safe_dm import safe_dm
from datetime import datetime
def register_events(client: discord.Client)->None:

    @client.event
    async def on_ready():
        print(f'bot logado como: {client.user}')
        owner_id = get_owner_id()
        if len(client.guilds) == 0:
            print("aviso: bot nao esta em nenhum servidor. encerrando servicos")
            await client.close()
            return
    
        else:
            await client.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game("a vida fora"))

        for guild in client.guilds:
            if guild.owner_id != owner_id:
                #await guild.leave()
                print(f"saindo da guilda {guild.name} pois nao sou o dono dela")
            else:
                await create_roles(guild)
                jogador = discord.utils.get(guild.roles, name="Jogador")
                adm = discord.utils.get(guild.roles, name="Administrador")
                for member in guild.members:
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
                                print(f"sem permissao para adicionar {jogador.name} a {member.name}")
                            except discord.HTTPException as e:
                                print(f"falha ao adicionar role para {member.name}: {e}")
        

    @client.event
    async def on_member_join(member: Member):
        if member.bot:
            return
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
                    timestamp=datetime.now()
                )
                embed.set_footer(text="Divirta-se e boa sorte!")
                sent = await safe_dm(member, embed=embed)
                if not sent:
                    print(f"não foi possível enviar DM para {member.name}. DMs podem estar desativadas.")
                print(f"{member.name} adicionado como {jogador.name}")
            except discord.Forbidden:
                print(f"sem permissao para adicionar {jogador.name} a {member.name}")
            except discord.HTTPException as e:
                print(f"falha ao adicionar role para {member.name}: {e}")