import discord, asyncio, io, textwrap, traceback, re, copy
from discord.ext import commands
from typing import Union
from contextlib import redirect_stdout
from utils.utility import save
from discord.utils import get
whitelist = []


class IT(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_result = None
        self.sessions = set()

    def cleanup_code(self, content):
        """Automatically removes code blocks from the code."""
        if content.startswith('```') and content.endswith('```'):
            return '\n'.join(content.split('\n')[1:-1])
        return content.strip('` \n')

    def get_syntax_error(self, e):
        if e.text is None:
            return f'```py\n{e.__class__.__name__}: {e}\n```'
        return f'```py\n{e.text}{"^":>{e.offset}}\n{e.__class__.__name__}: {e}```'

    @commands.command(hidden=True, name='eval')
    async def _eval(self, ctx, *, body: str):
        """::::admin:Evaluates a block of code.\nClient reference: `bot`\nContext reference: `ctx`\nLast in Memory: `_`"""
        if ctx.author.id == 310863530591256577 or ctx.author.id in whitelist:
            env = {
                'bot': self.bot,
                'ctx': ctx,
                'channel': ctx.channel,
                'author': ctx.author,
                'guild': ctx.guild,
                'message': ctx.message,
                '_': self._last_result
            }
            env.update(globals())
            body = self.cleanup_code(body)
            stdout = io.StringIO()
            to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'
            try:
                exec(to_compile, env)
            except Exception as e:
                return await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')
            func = env['func']
            try:
                with redirect_stdout(stdout):
                    ret = await func()
            except Exception as e:
                value = stdout.getvalue()
                await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
            else:
                value = stdout.getvalue()
                try:
                    await ctx.message.add_reaction('\u2705')
                except:
                    pass

                if ret is None:
                    if value:
                        await ctx.send(f'```py\n{value}\n```')
                else:
                    self._last_result = ret
                    await ctx.send(f'```py\n{value}{ret}\n```')
        else:
            await ctx.message.add_reaction(emoji='❌')
            await ctx.send('You\'re fucking nuts if you think you\'re going to successfully execute that command here.')

    @commands.command(hidden=True)
    @commands.has_permissions(administrator=True)
    async def sudo(self, ctx, who: Union[discord.Member, discord.User], *, command: str):
        """<user>:<command>:::admin:Run a command as another user."""
        if (re.compile(r'\b({0})\b'.format('off'), flags=re.IGNORECASE).search(command)) or (re.compile(r'\b({0})\b'.format('on'), flags=re.IGNORECASE).search(command)):
            await ctx.send('You can\'t `~sudo` another user to use `~off` or `~on`!')
        else:
            msg = copy.copy(ctx.message)
            msg.author = who
            msg.content = ctx.prefix + command
            new_ctx = await self.bot.get_context(msg)
            await self.bot.invoke(new_ctx)

    @commands.command(aliases=['reset'])
    @commands.has_permissions(administrator=True)
    async def reutils(self, ctx):
        """::::admin:Resets `bot.help_data`, `bot.blacklist`, and `bot.whitelist`."""
        self.bot.utils["blacklist"] = []
        save(self.bot)

    @commands.command(aliases=['mute'])
    @commands.has_permissions(administrator=True)
    async def off(self, ctx, member: discord.Member):
        """<member>::::admin:Appends member to bot.blacklist"""
        if not member.id == ctx.author.id:
            if not member.id in self.bot.blacklist:
                self.bot.blacklist.append(member.id)
                save(self.bot)
        else:
            await ctx.send(f"You cannot **`{self.bot.command_prefix}off`** yourself!")

    @commands.command(aliases=['unmute'])
    @commands.has_permissions(administrator=True)
    async def on(self, ctx, member: discord.Member):
        """<member>::::admin:Removes member from bot.blacklist"""
        if not member.id == ctx.author.id:
            if member.id in self.bot.blacklist:
                self.bot.blacklist.remove(member.id)
                save(self.bot)
        else:
            await ctx.send(f"You cannot **`{self.bot.command_prefix}on`** yourself!")

    @commands.command(aliases=['ack'])
    @commands.is_owner()
    async def acknowledge(self, ctx, member: discord.Member):
        """<@user>::::admin:Acknowledge all eval directives from given user.\nAliases: `~ack`"""
        if ctx.author.id != member.id:
            try:
                whitelist.append(member.id)
            except:
                pass
            await ctx.send(f'Acknowledged. Overridden permissions for user `{member.display_name}`.')
        else:
            async with ctx.channel.typing():
                await ctx.send('Acknowledged. Initiating recursion sequence...')
                await asyncio.sleep(10)

    @commands.command(aliases=['unack'])
    @commands.is_owner()
    async def reject(self, ctx, member: discord.Member):
        """<@user>::::admin:Rejects all eval directives from given user. This is enabled by default.\nAliases: `~unack`"""
        if ctx.author.id != member.id:
            try:
                whitelist.remove(member.id)
            except:
                pass
            await ctx.send(f'Acknowledged. Overridden permissions for user `{member.display_name}`.')
        else:
            async with ctx.channel.typing():
                await ctx.send('Acknowledged. Initiating recursion sequence...')
                await asyncio.sleep(10)

def setup(bot):
    bot.add_cog(IT(bot))