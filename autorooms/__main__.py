#!/usr/bin/env python
import os
from .bot import ARBot


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
