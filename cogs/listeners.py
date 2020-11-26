import discord
from discord.ext import tasks, commands
from discord.utils import get
from binascii import hexlify
status = '「勇敢な..！」'


class Listeners(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.clear_help_data.start()

    @tasks.loop(seconds=1800.0)
    async def clear_help_data(self):
        self.bot.help_data = {}

    @commands.Cog.listener()
    async def on_ready(self):
        # await self.bot.change_presence(activity=discord.Streaming(name=status, url='https://twitch.tv/Rivvnik'))
        print('┌────────────────────────────────────┐')
        print(f'       Logged in as {self.bot.user.name}')
        print(f'    Client ID: {self.bot.user.id}')
        print(f'  Status set to Streaming {status}')
        print('└────────────────────────────────────┘')

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        try:
            # await ctx.message.add_reaction(emoji='❌')
            await ctx.message.add_reaction(get(self.bot.emojis, name='clap'))
        except:
            pass
        if isinstance(error, commands.NotOwner):
            await ctx.send('You are not my father.')
        elif isinstance(error, commands.CheckFailure):
            await ctx.send('Sorry. You do not have the permissions necessary to execute this command.')
        elif isinstance(error, commands.CommandNotFound):
            await ctx.send('Sorry; I was unable to find that command. Check your syntax.')
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Sorry. It looks like you\'re missing an argument or two. Or three. Check your syntax.')
        elif isinstance(error, commands.NoPrivateMessage):
            await ctx.send('Sorry. This command has not been constructed for use within private channels.')
        else:
            await ctx.send(f'Alright! Okay. I have no idea what the fuck you just said.\n`{error}`')

    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        try:
            await ctx.message.add_reaction(emoji='✅')
        except:
            pass

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        user = self.bot.get_user(payload.user_id)
        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        if not user.bot:
            if payload.message_id in self.bot.help_data:
                if user.id == self.bot.help_data[payload.message_id]["author_id"]:
                    if str(payload.emoji) == '\N{LEFTWARDS BLACK ARROW}':
                        if self.bot.help_data[payload.message_id]["index"] > 0:
                            self.bot.help_data[payload.message_id]["index"] -= 1
                            await message.edit(embed=self.bot.help_data[payload.message_id]["embed_list"][self.bot.help_data[payload.message_id]["index"]])
                        await message.remove_reaction(emoji=payload.emoji, member=user)
                    elif str(payload.emoji) == '\N{BLACK RIGHTWARDS ARROW}':
                        if self.bot.help_data[payload.message_id]["index"] <= (len(self.bot.help_data[payload.message_id]["embed_list"]) - 2):
                            self.bot.help_data[payload.message_id]["index"] += 1
                            await message.edit(embed=self.bot.help_data[payload.message_id]["embed_list"][self.bot.help_data[payload.message_id]["index"]])
                        await message.remove_reaction(emoji=payload.emoji, member=user)
                    elif str(payload.emoji) == '\N{CROSS MARK}':
                        nemb = discord.Embed(color=int(f'0x{hexlify(str(id).encode())[9:15].decode()}', 16), description=f'`{str(self.bot.command_prefix)}help` or `{str(self.bot.command_prefix)}h` to reopen.').set_author(name=f'Help machine closed.', icon_url=self.bot.user.avatar_url)
                        await message.edit(embed=nemb)
                        await message.clear_reactions()
                        del self.bot.help_data[payload.message_id]


def setup(bot):
    bot.add_cog(Listeners(bot))