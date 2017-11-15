# required:
# python3.5+
# discord.py
# recommended:
# uvloop

import discord
import argparse
import asyncio
from discord.ext import commands
from watcher import LogWatcher
try:
    import uvloop
except ImportError:
    pass
else:
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

parser = argparse.ArgumentParser(description='Discord Bot for Log Monitoring')

parser.add_argument("--prefix", action="append", default=[],
                    help="set a bot prefix. can be used multiple times. ")
parser.add_argument("--token", help="the bot token", default=None)

args = vars(parser.parse_args())


class LogMon:

    def __init__(self, bot):
        self.bot = bot

    async def __local_check(self, ctx):
        return ctx.author.id == self.owner.id

    @commands.command()
    async def stopwatching(self, ctx):
        """
        stops watching for log files
        """
        if self.task is None:
            return await ctx.send('I wasn\'t watching anything')

        self.task.cancel()
        await ctx.send('Canceling task...')

    @commands.command()
    async def watchdirectoryfor(self, ctx, filepath: str, *, searchterm: str):
        """
        takes a directory path, and search term

        watches for a .log file containing the search term
        """

        if self.task:
            if not self.task.canceled():
                ctx.send('You are already waiting for a result.')

        if len(searchterm) == 0:
            await ctx.show_help()
        self.searchterm = searchterm
        self.task = self.bot.loop.create_task(self.watch(filepath))

    async def watch(self, filepath):

        def callback(filename, lines):
            for line in lines:
                if self.searchterm in line:
                    self.bot.loop.create_task(self.notify(line))

        watcher = LogWatcher("/var/log/", callback)
        while 1:
            watcher.loop(blocking=False)
            asyncio.sleep(0.1)

    async def notify(self, line):

        msg = ("Hey, you asked me to notify you of this...\n"
               "```\n{}```"
               "\nStill running.... (cancel watch with command)").format(line)

        await self.owner.send(msg)


def _prefix(bot, msg):
    return commands.when_mentioned_or(*args['prefix'])(bot, msg)


class MyContext(commands.Context):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    async def show_help(self, command=None):
        cmd = self.bot.get_command('help')
        command = command or self.command.qualified_name
        await self.invoke(cmd, command=command)


class LogBot(commands.Bot):

    def __init__(self, bot):
        super().__init__(
            command_prefix=_prefix,
            description="A minimal log monitoring bot by Sinbad#0413",
            pm_help=None)

    async def on_ready(self):
        self.appinfo = await self.bot.application_info()
        self.owner = self.appinfo.owner
        oauth = discord.utils.oauth_url(self.appinfo.id)
        print(f'\n\nLogged in')
        print(f'\nBot Invite Link: {oauth}')
        print(f'\nDiscord.py Version: {discord.__version__}\n')
        self.load_extension('LogMon')

    async def on_message(self, message):
        """let us avoid turtles all the way down"""
        if message.author.bot:
            return
        await self.process_commands(message)

    async def process_commands(self, message):
        ctx = await self.get_context(message, cls=MyContext)
        if ctx.command is None:
            return

        async with ctx.acquire():
            await self.invoke(ctx)

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.UserInputError):
            await ctx.show_help()

    def run(self, token):
        super().run(token, reconnect=True)


def main():
    bot = LogBot()
    bot.run(args['token'])


if __name__ == '__main__':
    main()
