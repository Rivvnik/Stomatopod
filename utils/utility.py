from discord import Member, Embed
import os, json


def jsons(bot):
    bot.token_path, bot.utils_path = os.path.join(os.path.split(os.path.abspath(__file__))[0], 'token.json'), os.path.join(os.path.split(os.path.abspath(__file__))[0], 'utils.json')
    with open(bot.token_path, 'r') as x: bot.token = json.load(x)
    with open(bot.utils_path, 'r') as f: bot.utils = json.load(f)
    bot.utils["help_data"] = {}
    bot.help_data, bot.blacklist = bot.utils["help_data"], bot.utils["blacklist"]
    save(bot)


def save(bot):
    with open(bot.utils_path, 'w') as f: json.dump(bot.utils, f)


async def search(bot, ctx, command):
    try:
        await ctx.send(bot.get_command(command))
    except Exception as e:
        await ctx.send(e)
    return


async def generator(member: Member, bot):
    embeds = []
    mybed = Embed(color=0x6000ff)
    for command in bot.commands:
        arguments = str()
        desc = str()
        help_string = str(command.help).split(':', 5)
        perm = help_string[4]
        if perm == 'owner' and member.id != 310863530591256577:
            continue
        elif perm == 'mod' and not member.guild_permissions.manage_messages:
            continue
        elif perm == 'admin' and not member.guild_permissions.ban_members:
            continue
        if command.cog_name is None:
            mybed.set_author(name='The Help Card', url='https://en.wikipedia.org/wiki/Tetrahydrocannabinol', icon_url=bot.user.avatar_url)
            mybed.description = 'For all to use.'
            for arg in help_string[:4]:
                arguments = arguments + f'{arg} '
            desc = desc + f'{help_string[5]}'
            desc = '{}\nAliases: `{}`, and `{}`.'.format(desc, ", ".join(command.aliases[:-1]), command.aliases[-1]) if len(command.aliases) > 1 else '{}\nAlias: `{}{}`'.format(desc, str(bot.command_prefix), command.aliases[0]) if len(command.aliases) == 1 else desc
            mybed.add_field(name=f'**{command.name}**', value=f'`{str(bot.command_prefix)}{command.name} {arguments.strip()}`\n{desc}', inline=False)
    embeds.append(mybed)

    for cog in bot.cogs:
        if not cog == 'Utility':
            embed = Embed(color=0x6000ff, description='For all to use.')
            if cog == 'IT':
                embed.set_author(name='The Help Card - Tech Support', icon_url=bot.user.avatar_url)
                embed.description = 'Only Administrators may see and use these commands.'
            for command in bot.get_cog(cog).get_commands():
                arguments = str()
                desc = str()
                help_string = str(command.help).split(':', 6)
                perm = help_string[4]
                if perm == 'owner' and member.id != 310863530591256577:
                    continue
                elif perm == 'mod' and not member.guild_permissions.manage_messages:
                    continue
                elif perm == 'admin' and not member.guild_permissions.ban_members:
                    continue

                for arg in help_string[:4]:
                    arguments = arguments + f'{arg} '
                desc = desc + f'{help_string[5]}'
                desc = '{}\nAliases: `{}`, and `{}`.'.format(desc, ", ".join(command.aliases[:-1]), command.aliases[-1]) if len(command.aliases) > 1 else '{}\nAlias: `{}{}`'.format(desc, str(bot.command_prefix), command.aliases[0]) if len(command.aliases) == 1 else desc
                embed.add_field(name=f'**{command.name}**', value=f'`{str(bot.command_prefix)}{command.name} {arguments.strip()}`\n{desc}', inline=False)
            embeds.append(embed)
    return embeds