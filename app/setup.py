import discord

async def create_roles(guild: discord.Guild):
    roles = [
        ("Administrador", discord.Permissions(administrator=True), discord.Colour.red(), True),
        ("Especialista", discord.Permissions(), discord.Colour.yellow(), True),
        ("Aventureiro", discord.Permissions(), discord.Colour.light_gray(), True),
        ("Iniciante", discord.Permissions(), discord.Colour.dark_gray(), True),
        ("Jogador", discord.Permissions(send_messages=True,read_messages=True,read_message_history=True), discord.Colour.dark_grey(), False),
    ]

    for role_name, permissions, colour, hoist in roles:
        if discord.utils.get(guild.roles, name=role_name):
            print(f"grupo '{role_name}' já criado")
            continue
        role = await guild.create_role(name=role_name, permissions=permissions, colour=colour, hoist=hoist)
        print(f"grupo {role.name} criado")
