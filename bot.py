import discord, asyncpg
from discord.ext import commands
import utils.utility as utility
intents = discord.Intents.default()  # literally what are intents? something that VP showed me..
intents.members, intents.reactions, intents.presences, intents.typing = True, True, True, True
bot = commands.Bot(command_prefix='>', intents=intents, case_insensitive=True, owner_id=310863530591256577)
bot.remove_command('help')
utility.jsons(bot)

extensions = (
    'cogs.IT',
    'cogs.listeners'
)


async def create_db_pool():
    bot.pg = await asyncpg.create_pool(database="postgres", user="postgres", password=" ")


@bot.command(aliases=['h'])
async def help(ctx, command: str=None):
    """<command>:::::Seriously?"""
    command = command or None
    if not command:
        embeds = await utility.generator(ctx.author, bot)
        del embeds[-1]
        await ctx.message.delete()
        for embed in embeds:
            embed.set_footer(text=f'Page {embeds.index(embed) + 1}/{len(embeds)}')
        message = await ctx.send(embed=embeds[0])
        for emoji in ['\N{LEFTWARDS BLACK ARROW}', '\N{BLACK RIGHTWARDS ARROW}', '\N{CROSS MARK}']:
            await message.add_reaction(emoji)
        bot.help_data[message.id] = {}
        bot.help_data[message.id]["embed_list"], bot.help_data[message.id]["index"], bot.help_data[message.id]["author_id"] = embeds, 0, ctx.author.id
        utility.save(bot)
    else:
        await utility.search(bot, ctx, command)

if __name__ == '__main__':
    for extension in extensions:
        try:
            bot.load_extension(extension)
        except Exception as error:
            print(f'`{extension}` cannot be loaded. [{error}]')

bot.loop.run_until_complete(create_db_pool())
bot.run(bot.token["TOKEN"])
