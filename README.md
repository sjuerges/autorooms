# discordbots
One stand alone discord bot, possibly more later

# autorooms.py

```
python3.6 -m venv venv
source venv/bin/activate
pip install -U git+https://github.com/Rapptz/discord.py@rewrite#egg=discord.py[voice]
AUTOROOMTOKEN='your discord bot token here' python autorooms.py
```

## auto restarting

systemd and upstart examples are in the /service-files folder

They do require some modification.

If you'd rather a script set this up for you

```
chmod 755 autorooms-setup.sh
sudo ./autorooms-setup.sh
```
