import discord
from discord.utils import get
from discord.ext import commands

from discord_slash import SlashCommand
from discord_slash.utils import manage_commands

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from tues_admin import utils, update

bot = commands.Bot(command_prefix='.', intents=discord.Intents.all())
slash = SlashCommand(bot, sync_commands=True)

# ----------------------------------------------------------------

async def roles_update():
    guild = get(bot.guilds, name=utils.GUILD)
    bot_log = get(guild.channels, name='bot-log')

    await bot_log.send('Starting Update!')

    await update.update_admins(guild, bot_log)

    await bot_log.send('Казваме ДОВИЖДАНЕ на 12ти клас! :wave:')
    await update.update_alumni(guild)

    await update.update_students(guild, bot_log)
    await bot_log.send('Добре дошли на следващото ниво! :arrow_double_up:')

    await bot_log.send('Update finished!')

# ----------------------------------------------------------------

@bot.event
async def on_ready():
    guild = get(bot.guilds, name=utils.GUILD)

    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})\n'
        f'*** Bot is up-and-running ***'
    )

    scheduler = AsyncIOScheduler()
    scheduler.add_job(roles_update, CronTrigger.from_crontab('0 8 15 SEP *')) # 10:00
    scheduler.start()

@slash.slash(
  name="setup",
  description="Получаване на роли и nickname",
  options=[
    manage_commands.create_option(
        name = "ClassNumber",
        description = "Кой клас си? 8-12",
        option_type = 3,
        required = True
    ),
    manage_commands.create_option(
        name = "ClassLetter",
        description = "Паралелка А-Г (главни букви на кирилица)",
        option_type = 3,
        required = True
    ),
    manage_commands.create_option(
        name = "Name",
        description = "Име и фамилия на кирилица",
        option_type = 3,
        required = True
    )
  ],
  guild_ids=[797018153406300160]
)
async def _setup(ctx, number: str, letter: str, name: str):
    if number not in ['8', '9', '10', '11', '12'] or letter not in ['А', 'Б', 'В', 'Г']:
        await ctx.send('Опитай пак!')
    else:
        await ctx.respond()

        member = ctx.author
        guild = ctx.message.guild

        roles = {
            '8': get(guild.roles, name='8ми клас'),
            '9': get(guild.roles, name='9ти клас'),
            '10': get(guild.roles, name='10ти клас'),
            '11': get(guild.roles, name='11ти клас'),
            '12': get(guild.roles, name='12ти клас'),
        }

        all_role = get(guild.roles, name='Отговорници')

        await member.add_roles(all_role, roles[number])
        await member.edit(nick=f'{name} ({number}{letter})')

if __name__ == '__main__':
    bot.run(utils.TOKEN, bot=True)
