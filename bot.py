from discord.ext import commands
import asyncpg
import os
import json
from utils.embuilder import generator

bot = commands.Bot(command_prefix='~', case_insensitive=True, owner_id=310863530591256577)
bot.help_data = {}
bot.remove_command('help')
bot.path = os.path.join(os.path.split(os.path.abspath(__file__))[0], 'utils/utils.json')
with open(bot.path, 'r') as f:
    bot.utils = json.load(f)
extensions = (
    'cogs.IT',
    'cogs.utility'
)


async def create_db_pool():
    bot.pg = await asyncpg.create_pool(database="postgres", user="postgres", password=" ")


@bot.command(aliases=['h'])
async def help(ctx):
    """:::::Seriously?"""
    embeds = await generator(ctx.author, bot)
    await ctx.message.delete()
    for embed in embeds:
        embed.set_footer(text=f'Page {embeds.index(embed) + 1}/{len(embeds)}')
    message = await ctx.send(embed=embeds[0])
    for emoji in ['\N{LEFTWARDS BLACK ARROW}', '\N{BLACK RIGHTWARDS ARROW}', '\N{CROSS MARK}']:
        await message.add_reaction(emoji)
    bot.help_data[message.id] = {}
    bot.help_data[message.id]["embed_list"], bot.help_data[message.id]["index"], bot.help_data[message.id]["author_id"] = embeds, 0, ctx.author.id

if __name__ == '__main__':
    for extension in extensions:
        try:
            bot.load_extension(extension)
        except Exception as error:
            print(f'`{extension}` cannot be loaded. [{error}]')

bot.loop.run_until_complete(create_db_pool())
bot.run(bot.utils["TOKEN"])
