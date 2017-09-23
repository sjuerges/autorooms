import discord
from discord.ext import commands
from datetime import datetime, timedelta
import os
import asyncio
assert discord


auto_room_indicator = '⌛'
game_room_indicator = '🎮'
clone_indicator = '♻'

bot = commands.Bot(command_prefix='HAL9000> ', description=None)


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

    editargs = {'bitrate': chan.bitrate,
                'user_limit': chan.user_limit}

    if category is not None:
        editargs.update({'category': category, 'sync_permissions': True})

    chanz = "".join([c for c in chan.name if c != auto_room_indicator])
    chan_name = "{0}: {1}".format(clone_indicator, chanz)

    z = await chan.guild.create_voice_channel(chan_name)
    await asyncio.sleep(0.5)
    await z.edit(**editargs)

    await member.move_to(z, reason="autoroom")


async def _make_game_room(member, chan):
    if member.game is None:
        return
    category = chan.category

    editargs = {'bitrate': chan.bitrate, 'user_limit': chan.user_limit}

    if category is not None:
        editargs.update({'category': category, 'sync_permissions': True})

    chan_name = "{0}: {1.game.name}".format(clone_indicator, member)

    z = await chan.guild.create_voice_channel(chan_name)
    await asyncio.sleep(0.5)
    await z.edit(**editargs)
    await member.move_to(z, reason="autoroom")


bot.run(os.environ.get('TOKEN'))
