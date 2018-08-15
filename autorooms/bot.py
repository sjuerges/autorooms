import logging

import discord
from discord.ext import commands
from discord.voice_client import VoiceClient

VoiceClient.warn_nacl = False


class ARBot(commands.AutoShardedBot):
    """
    Autorooms bot
    """

    def __init__(self, *args, initial_exts: tuple = None, **kwargs):
        self.uptime = None
        self.initial_extensions = initial_exts or (
            "autorooms.extensions.autorooms",
            "autorooms.extensions.info",
        )
        self.invite_link = None
        super().__init__(*args, command_prefix=commands.when_mentioned, **kwargs)

    async def on_ready(self):
        if self.uptime is not None:
            return

        for extension in self.initial_extensions:
            try:
                self.load_extension(extension)
            except discord.ClientException as e:
                logging.exception(e)

        await self.change_presence(
            status=discord.Status.online,
            activity=discord.Game(name='mention me with "help" for help'),
        )
        data = await self.application_info()
        perms = discord.Permissions(permissions=16796688)
        self.invite_link = discord.utils.oauth_url(data.id, permissions=perms)
        print(f"Use this link to add the bot to your server: {self.invite_link}")
