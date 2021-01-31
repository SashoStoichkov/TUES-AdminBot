import os

import discord
from discord.utils import get
from discord.ext import commands

from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='.', intents=intents)

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

    # TODO: Think of kick dm
    # await dm.send(f'Hello @{member.name}')
    # await dm.send('You have been kicked from the server. Have a nice life :)')

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
        await kick_and_dm(student)

async def update(guild, ctx):
    await ctx.send('Админ -> Бивш Админ')
    await update_admins(guild)

    await ctx.send('Казваме ДОВИЖДАНЕ на 12ти клас! :wave:')
    await update_alumni(guild)

    await ctx.send('Добре дошли на следващото ниво!')
    await update_students(guild)

@bot.event
async def on_ready():
    guild = get(bot.guilds, name=GUILD)

    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})\n'
        f'*** Bot is ready ***'
    )

@bot.command(name='test')
async def test(ctx):
    await ctx.send('Test from TUES BOT!')

@bot.command(name='update')
async def roles(ctx):
    guild = get(bot.guilds, name=GUILD)

    await ctx.send('Starting Update!')
    await update(guild, ctx)
    await ctx.send('Update finished!')

bot.run(TOKEN, bot=True)
