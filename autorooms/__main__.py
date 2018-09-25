#!/usr/bin/env python
import os
import asyncio
from .bot import ARBot

try:
    import uvloop
except ImportError:
    pass
else:
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def main():
    bot = ARBot()
    TOKEN = os.environ.get("AUTOROOMTOKEN")
    try:
        bot.run(TOKEN)
    except KeyboardInterrupt:
        print("Closing session...")
    finally:
        bot.close()


if __name__ == "__main__":
    main()
