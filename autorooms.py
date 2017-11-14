import discord
from discord.ext import commands
from datetime import datetime, timedelta
import os
import asyncio
assert discord


auto_room_indicator = '⌛'
game_room_indicator = '🎮'
clone_indicator = '♻'


def whatsmyprefix(bot, msg):
    return commands.when_mentioned_or(*['>>'])(bot, msg)


bot = commands.Bot(command_prefix=whatsmyprefix,
                   description="A minimal config autoroom bot by Sinbad#0413")


@bot.event
async def on_ready():
    await bot.change_presence(
        game=discord.Game(name='\'>>setup\' for instructions', type=0))


@bot.command()
async def setup(ctx):
    """
    Instructions
    """
    content = f"""
    Hey, I see you may ned help using this.
    This bot creates clones of existing channels that are temporary, with the
    same permissions and category as the original.

    To create autorooms, have the first character in the source room be either

    `{auto_room_indicator}` : for standard cloning
    or
    `{game_room_indicator}` : for room names based on game detected by discord

    Don't use {clone_indicator} in your channel names, the bot uses these
    to detect temporary channels it makes
    """
    embed = discord.Embed(
        description=content, color=discord.Color.dark_purple())

    await ctx.author.send(embed=embed)


@bot.command()
async def info(ctx):
    """
    basic info about the bot
    """
    author_repo = 'https://github.com/mikeshardmind'
    bot_repo = author_repo + '/singlepurposediscordbots'
    dpy_repo = "https://github.com/Rapptz/discord.py"
    python_url = "https://www.python.org/"
    dpy_version = "[{}]({})".format(discord.__version__, dpy_repo)
    py_version = "[{}.{}.{}]({})".format(*os.sys.version_info[:3], python_url)

    about = (
        f"This is a free and open source bot made by "
        f"[Sinbad#0413]({author_repo}) to automatically "
        f"make channels on the fly without giving manage channels to everyone."
        f"\nIt is written in [python]({python_url}), "
        f"and uses [discord.py]({dpy_repo})")

    embed = discord.Embed(colour=discord.Colour.dark_purple())
    embed.add_field(name="Python", value=py_version)
    embed.add_field(name="discord.py", value=dpy_version)
    embed.add_field(name="About me", value=about, inline=False)
    embed.set_footer(
        text=f'[bug reports can be submitted here]({bot_repo})')

    await ctx.send(embed=embed)


@bot.event
async def on_voice_state_update(member, v_before, v_after):

    if v_before.channel == v_after.channel:
        return

    if v_before.channel is not None:
        channel = v_before.channel
        if channel.name.startswith(clone_indicator):
            if len(channel.members) == 0:
                if channel.created_at + timedelta(seconds=3) \
                        < datetime.utcnow():
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

    editargs = {'bitrate': chan.bitrate, 'user_limit': chan.user_limit}
    overwrites = {}
    for perm in chan.overwrites:
        overwrites.update({perm[0]: perm[1]})

    chanz = "".join([c for c in chan.name if c != auto_room_indicator])
    chan_name = "{0}: {1}".format(clone_indicator, chanz)

    z = await chan.guild.create_voice_channel(
        chan_name, category=category, overwrites=overwrites)
    await member.move_to(z, reason="autoroom")
    await asyncio.sleep(0.5)
    await z.edit(**editargs)


async def _make_game_room(member, chan):
    if member.game is None:
        return
    category = chan.category

    editargs = {'bitrate': chan.bitrate, 'user_limit': chan.user_limit}
    for perm in chan.overwrites:
        overwrites = {}
        overwrites.update({perm[0]: perm[1]})

    chan_name = "{0}: {1.game.name}".format(clone_indicator, member)

    z = await chan.guild.create_voice_channel(
        chan_name, category=category, overwrites=overwrites)
    await member.move_to(z, reason="autoroom")
    await asyncio.sleep(0.5)
    await z.edit(**editargs)

bot.run(os.environ.get('AUTOROOMTOKEN'))
