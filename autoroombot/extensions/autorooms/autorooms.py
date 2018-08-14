import discord
from discord.ext import commands
from datetime import datetime, timedelta
import os
import asyncio

from .antispam import AutoRoomAntiSpam

AUTOROOM_STR = "⌛"
GAMEROOM_STR = "🎮"
CLONEDROOM_STR = "♻"


class AutoRooms:
    """
    zeroconfig autorooms
    """
    def __init__(self, bot):
        self.bot = bot