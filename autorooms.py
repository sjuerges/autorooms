import discord
from discord.ext import commands
from datetime import datetime, timedelta
import os
import asyncio

assert discord


auto_room_indicator = "⌛"
game_room_indicator = "🎮"
clone_indicator = "♻"


def whatsmyprefix(bot, msg):
    return commands.when_mentioned_or(*[">>"])(bot, msg)


bot = commands.AutoShardedBot(
    command_prefix=whatsmyprefix,
    description="A minimal config autoroom bot by Sinbad#0001",
)


@bot.event
async def on_ready():
    status = bot.guilds[0].me.status if len(bot.guilds) > 0 else discord.Status.online
    await bot.change_presence(
        status=status, activity=discord.Game(name="'>>setup' for instructions")
    )
    data = await bot.application_info()
    perms = discord.Permissions(permissions=16796688)
    oauth_url = discord.utils.oauth_url(data.id, permissions=perms)
    print(f"Use this link to add the bot to your server: {oauth_url}")


@bot.command
async def setup(ctx):
    """
    Instructions
    """
    content = (
        f"Hey, I see you may need help using this."
        f"\nThis bot creates clones of existing channels that are temporary, "
        f"with the same permissions and category as the original."
        f"\nTo create autorooms, have the first character in the source room "
        f"be either"
        f"\n`{auto_room_indicator}` : for standard cloning"
        f"\nor\n"
        f"`{game_room_indicator}` : for room names based on game name "
        f"as detected by discord"
        f"\n\nDon't use `{clone_indicator}` in your channel names, "
        f"the bot uses this to detect temporary channels it makes"
    )
    embed = discord.Embed(description=content, color=discord.Color.dark_purple())

    await ctx.author.send(embed=embed)


@bot.command
async def join(ctx):
    """
    get my invite link
    """
    data = await bot.application_info()
    perms = discord.Permissions(permissions=16796688)
    oauth_url = discord.utils.oauth_url(data.id, permissions=perms)
    await ctx.send(f"Click here to add me to your server: {oauth_url}")


@bot.command
async def info(ctx):
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
    embed.add_field(name="About me", value=about, inline=False)

    await ctx.send(embed=embed)


@bot.command
async def support(ctx):
    """
    How to support this bot's ongoing development and hosting.
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


@bot.event
async def on_voice_state_update(member, v_before, v_after):

    if v_before.channel == v_after.channel:
        return

    if v_before.channel is not None:
        for channel in v_before.channel.guild.voice_channels:
            if channel.name.startswith(clone_indicator):
                if len(channel.members) == 0:
                    if channel.created_at + timedelta(seconds=3) < datetime.utcnow():
                        try:
                            await channel.delete(reason="Empty Autoroom")
                        except Exception:
                            pass

    if v_after.channel is not None:
        if v_after.channel.name.startswith(auto_room_indicator):
            await _make_auto_room(member, v_after.channel)
        if v_after.channel.name.startswith(game_room_indicator):
            await _make_game_room(member, v_after.channel)


async def _make_auto_room(member, chan):

    category = chan.category

    editargs = {"bitrate": chan.bitrate, "user_limit": chan.user_limit}
    overwrites = {}
    for perm in chan.overwrites:
        overwrites.update({perm[0]: perm[1]})

    chanz = "".join([c for c in chan.name if c != auto_room_indicator])
    chan_name = "{0}: {1}".format(clone_indicator, chanz)

    z = await chan.guild.create_voice_channel(
        chan_name, category=category, overwrites=overwrites
    )
    await member.move_to(z, reason="autoroom")
    await asyncio.sleep(0.5)
    await z.edit(**editargs)


async def _make_game_room(member, chan):
    try:
        chan_name = "{0}: {1.activity.name}".format(clone_indicator, member)
    except:
        return
    category = chan.category

    editargs = {"bitrate": chan.bitrate, "user_limit": chan.user_limit}
    for perm in chan.overwrites:
        overwrites = {}
        overwrites.update({perm[0]: perm[1]})

    z = await chan.guild.create_voice_channel(
        chan_name, category=category, overwrites=overwrites
    )
    await member.move_to(z, reason="autoroom")
    await asyncio.sleep(0.5)
    await z.edit(**editargs)


bot.run(os.environ.get("AUTOROOMTOKEN"))
