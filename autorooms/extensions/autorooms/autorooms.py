import asyncio
import contextlib
from datetime import datetime, timedelta

import discord

# from .antispam import AutoRoomAntiSpam

AUTOROOM_STR = "⌛"
GAMEROOM_STR = "🎮"
CLONEDROOM_STR = "♻"


class AutoRooms:
    """
    zeroconfig autorooms
    """

    def __init__(self, bot):
        self.bot = bot

    async def on_voice_state_update(self, member, v_before, v_after):

        if v_before.channel == v_after.channel:
            return

        with contextlib.suppress(Exception):
            for channel in v_before.channel.guild.voice_channels:
                if channel.name.startswith(CLONEDROOM_STR) and not channel.members:
                    if channel.created_at + timedelta(seconds=3) < datetime.utcnow():
                        await channel.delete(reason="Empty Autoroom")

        if v_after.channel is not None:
            if v_after.channel.name.startswith(AUTOROOM_STR):
                await self.make_auto_room(member, v_after.channel)
            if v_after.channel.name.startswith(GAMEROOM_STR):
                await self.make_game_room(member, v_after.channel)

    async def make_auto_room(self, member, chan):

        category = chan.category

        editargs = {"bitrate": chan.bitrate, "user_limit": chan.user_limit}
        overwrites = {}
        for perm in chan.overwrites:
            overwrites.update({perm[0]: perm[1]})

        chan_name = "{0}: {1}".format(CLONEDROOM_STR, chan.name).replace(
            AUTOROOM_STR, ""
        )

        z = await chan.guild.create_voice_channel(
            chan_name, category=category, overwrites=overwrites
        )
        await member.move_to(z, reason="autoroom")
        await asyncio.sleep(0.5)
        await z.edit(**editargs)

    async def make_game_room(self, member, chan):
        try:
            chan_name = "{0}: {1.activity.name}".format(CLONEDROOM_STR, member)
        except (AttributeError,):
            return
        category = chan.category

        editargs = {"bitrate": chan.bitrate, "user_limit": chan.user_limit}
        overwrites = {}
        for perm in chan.overwrites:
            overwrites.update({perm[0]: perm[1]})

        z = await chan.guild.create_voice_channel(
            chan_name, category=category, overwrites=overwrites
        )
        await member.move_to(z, reason="autoroom")
        await asyncio.sleep(0.5)
        await z.edit(**editargs)


def setup(bot):
    bot.add_cog(AutoRooms(bot))
