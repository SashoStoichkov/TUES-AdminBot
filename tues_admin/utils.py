import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

from discord.utils import get

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

async def kick_and_dm(member):
    dm = await member.create_dm()

    await dm.send(f':wave: Здравей, {member.mention}')
    await dm.send(':tada: Честито завършване!')
    await dm.send(':star2: С пожелание за успехи, както в професионален, така и в личен план!')

    await member.kick(reason='TUES IS OVER.')

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
