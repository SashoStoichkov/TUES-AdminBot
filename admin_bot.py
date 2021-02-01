import os

import discord
from discord.utils import get
from discord.ext import commands

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

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
    await dm.send(f'Здравей, {member.mention}')
    await dm.send('You have been kicked from the server. Have a nice life :)')

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

async def update_admins(guild, bot_log):
    role_admin = get(guild.roles, name='Админ')
    role_past_admin = get(guild.roles, name='Бивш Админ')

    await bot_log.send('Благодарим на Админите:')

    for admin in get_members_with_role(guild, role_admin):
        await bot_log.send(f'{admin.mention}')

        await remove_all_roles(admin)
        await member.add_roles(role_past_admin)

    await bot_log.send(f'Добре дошли в клуба {role_past_admin.mention}')

async def update_students(guild, bot_log):
    role_08 = get(guild.roles, name='8ми клас')
    role_09 = get(guild.roles, name='9ти клас')
    role_10 = get(guild.roles, name='10ти клас')
    role_11 = get(guild.roles, name='11ти клас')
    role_12 = get(guild.roles, name='12ти клас')

    roles = {
        role_11: role_12,
        role_10: role_11,
        role_09: role_10,
        role_08: role_09
    }

    for old_role, new_role in roles.items():
        await bot_log.send(f'{old_role.mention}, добре дошли в {new_role.mention}')
        await update_roles(guild, old_role, new_role)

async def update_alumni(guild):
    role_12 = get(guild.roles, name='12ти клас')

    for student in get_members_with_role(guild, role_12):
        await remove_all_roles(student)
        await kick_and_dm(student)

# ----------------------------------------------------------------

async def roles_update():
    guild = get(bot.guilds, name=GUILD)
    bot_log = get(guild.channels, name='bot-log')

    await bot_log.send('Starting Update!')

    await update_admins(guild, bot_log)

    await bot_log.send('Казваме ДОВИЖДАНЕ на 12ти клас! :wave:')
    await update_alumni(guild)

    await update_students(guild, bot_log)
    await bot_log.send('Добре дошли на следващото ниво! :arrow_double_up:')

    await bot_log.send('Update finished!')

# ----------------------------------------------------------------

async def test():
    guild = get(bot.guilds, name=GUILD)
    bot_log = get(guild.channels, name='bot-log')

    await bot_log.send('Test on specific date!')
    await bot_log.send('Today should be 01.02.2021 12:00')

@bot.event
async def on_ready():
    guild = get(bot.guilds, name=GUILD)

    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})\n'
        f'*** Bot is ready ***'
    )

    scheduler = AsyncIOScheduler()
    scheduler.add_job(test, CronTrigger.from_crontab('30 8 1 FEB *')) # 10:30
    # scheduler.add_job(roles_update, CronTrigger.from_crontab('0 12 15 SEP *'))
    scheduler.start()

if __name__ == '__main__':
    bot.run(TOKEN, bot=True)
