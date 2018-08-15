[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)[![Tip Jar](https://img.shields.io/badge/Paypal-Donate-blue.svg)](https://www.paypal.me/mikeshardmind)

**WARNING**
Do not use this bot if you have any channels beginning with the '♻' character and care about those channels, the bot uses this character to denote temporary channels.

# How to

If you'd like, you can just [invite my bot](https://discordapp.com/oauth2/authorize?client_id=365420182522429440&scope=bot&permissions=285232144)

If you would prefer to host your own, keep reading.


## autorooms

This pins a specific version of discord.py, so put it in a venv if needed to prevent conflicts.
```
python3.6 -m pip install --process-dependency-links discord-autorooms
AUTOROOMTOKEN='your discord bot token here' discord-autorooms
```

## auto restarting

systemd and upstart examples are in the /service-files folder

They do require some modification.

If you'd rather a script set this up for you (This script is not guaranteed to work.)

```
chmod 755 autorooms-setup.sh
sudo ./autorooms-setup.sh
```

Docker image soon (tm)
