import os

import discord
from discord.utils import get

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)

def get_members_with_role(guild, role):
    members = []

    admin = get(guild.roles, name='Баш Админ')
    aztues = get(guild.roles, name='АЗТУЕС')

    for member in guild.members:
        if admin in member.roles or aztues in member.roles:
            pass
        elif role in member.roles:
            members.append(member)

    return members

async def remove_all_roles(member):
    await member.edit(roles=[])

async def update_roles(guild, old_role, new_role):
    members = get_members_with_role(guild, old_role)

    if members:
        for member in members:
            await member.remove_roles(old_role)
            await member.add_roles(new_role)

            print(
                f'{member.name} updated roles from "{old_role.name}" to "{new_role.name}"'
            )
    else:
        print('No members to update!')

async def update_admins(guild):
    role_admin = get(guild.roles, name='Админ')
    role_past_admin = get(guild.roles, name='Бивш Админ')

    admins = get_members_with_role(guild, role_admin)
    for admin in admins:
        await remove_all_roles(admin)
        await member.add_roles(role_past_admin)

async def update_students(guild):
    old_roles = []
    old_roles.append(get(guild.roles, name='8ми клас'))
    old_roles.append(get(guild.roles, name='9ти клас'))
    old_roles.append(get(guild.roles, name='10ти клас'))
    old_roles.append(get(guild.roles, name='11ти клас'))

    new_roles = old_roles
    new_roles.remove(get(guild.roles, name='8ми клас'))
    new_roles.append(get(guild.roles, name='12ти клас'))

    for old_role in old_roles:
        for new_role in new_roles:
            await update_roles(guild, old_role, new_role)

async def update_alumni(guild):
    role_12 = get(guild.roles, name='12ти клас')

    alumni = get_members_with_role(guild, role_12)
    for student in alumni:
        await remove_all_roles(student)
        await student.kick(reason='TUES IS OVER.')

async def update(guild):
    await update_admins(guild)
    await update_alumni(guild)
    await update_students(guild)

@client.event
async def on_ready():
    guild = get(client.guilds, name=GUILD)

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

    # await update(guild)

client.run(TOKEN)
