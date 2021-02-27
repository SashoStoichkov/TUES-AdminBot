from . import utils

from discord.utils import get

async def update_admins(guild, bot_log):
    role_admin = get(guild.roles, name='Админ')
    role_past_admin = get(guild.roles, name='Бивш Админ')

    await bot_log.send('Благодарим на Админите:')

    for admin in utils.get_members_with_role(guild, role_admin):
        await bot_log.send(f'{admin.mention}')

        await utils.remove_all_roles(admin)
        await admin.add_roles(role_past_admin)

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
        await utils.update_roles(guild, old_role, new_role)
        await bot_log.send(f'{old_role.mention}, добре дошли в {new_role.mention}')

async def update_alumni(guild):
    role_12 = get(guild.roles, name='12ти клас')

    for student in utils.get_members_with_role(guild, role_12):
        await utils.remove_all_roles(student)
        await utils.kick_and_dm(student)
