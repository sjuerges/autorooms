import os

import discord
from discord.ext import commands

AUTOROOM_STR = "⌛"
GAMEROOM_STR = "🎮"
CLONEDROOM_STR = "♻"


class Info:
    """
    Various info
    """

    @commands.command()
    async def setup(self, ctx):
        """
        Instructions for use
        """
        content = (
            f"Hey, I see you may need help using this."
            f"\nThis bot creates clones of existing channels that are temporary, "
            f"with the same permissions and category as the original."
            f"\nTo create autorooms, have the first character in the source room "
            f"be either"
            f"\n`{AUTOROOM_STR}` : for standard cloning"
            f"\nor\n"
            f"`{GAMEROOM_STR}` : for room names based on game name "
            f"as detected by discord"
            f"\n\nDon't use `{CLONEDROOM_STR}` in your channel names, "
            f"the bot uses this to detect temporary channels it makes"
        )
        embed = discord.Embed(description=content, color=discord.Color.dark_purple())
        try:
            await ctx.author.send(embed=embed)
        except discord.Forbidden:
            await ctx.send(content="Couldn't DM you...", embed=embed)

    @commands.command()
    async def join(self, ctx):
        """
        get my invite link
        """
        if not ctx.bot.invite_link:
            data = await ctx.bot.application_info()
            perms = discord.Permissions(permissions=16796688)
            ctx.bot.invite_link = discord.utils.oauth_url(data.id, permissions=perms)
        await ctx.send(f"Click here to add me to your server: <{ctx.bot.invite_link}>")

    @commands.command()
    async def info(self, ctx):
        """
        basic info about the bot
        """
        author_repo = "https://github.com/mikeshardmind"
        bot_repo = author_repo + "/autorooms"
        dpy_repo = "https://github.com/Rapptz/discord.py"
        python_url = "https://www.python.org/"
        dpy_version = "[{}]({})".format(discord.__version__, dpy_repo)
        py_version = "[{}.{}.{}]({})".format(*os.sys.version_info[:3], python_url)

        about = (
            f"This is a free and [open source bot]({bot_repo}) made by "
            f"[Sinbad#0001]({author_repo}) to automagically "
            f"make channels on the fly without giving manage channels to everyone."
            f"\nIt is written in [python]({python_url}), "
            f"and uses [discord.py]({dpy_repo})"
            f"\n\nbug reports can be submitted [here]({bot_repo}/issues)"
        )

        embed = discord.Embed(colour=discord.Colour.dark_purple())
        embed.add_field(name="Python", value=py_version)
        embed.add_field(name="discord.py", value=dpy_version)
        embed.add_field(name="Users",  value=len(ctx.bot.users))
        embed.add_field(name="Servers", value=len(ctx.bot.guilds))
        embed.add_field(name="About me", value=about, inline=False)

        await ctx.send(embed=embed)

    @commands.command()
    async def support(self, ctx):
        """
        Support ongoing development and hosting.
        """
        patreon = "https://www.patreon.com/mikeshardmind"
        author_repo = "https://github.com/mikeshardmind"
        bot_repo = author_repo + "/autorooms"
        dpy_repo = "https://github.com/Rapptz/discord.py"
        python_url = "https://www.python.org/"
        dpy_version = "[{}]({})".format(discord.__version__, dpy_repo)
        py_version = "[{}.{}.{}]({})".format(*os.sys.version_info[:3], python_url)

        details = (
            f"Thanks for taking an interest in supporting this. "
            f"I made this in spare time, for my own needs, but I am glad "
            f"other people find it useful.\n\nOne of the best ways you can help me"
            f" is to submit bug reports if you find anything not behaving as "
            f"intended (click [here]({bot_repo}/issues)) "
            f"\n\nIf you would like to support me more directly, "
            f"I have a [Patreon page]({patreon})."
        )

        embed = discord.Embed(colour=discord.Colour.dark_purple())
        embed.add_field(name="Python", value=py_version)
        embed.add_field(name="discord.py", value=dpy_version)
        embed.add_field(name="About me", value=details, inline=False)

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Info())
