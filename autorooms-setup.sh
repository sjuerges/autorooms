#!/bin/bash
echo "This script will setup the autoroombot in a python virtual environment with autorestart"
if [ $# != 1 ]; then
   echo "Usage $0 TOKEN"
fi

if [ -f "$(pwd)/autorooms.py" ]; then
  true
else
  echo "this script must be run from the same directory as autorooms.py" 1>&2
  exit 1
fi

if [ $EUID -ne 0 ]; then
  echo "The script will relaunch and prompt for sudo to continue" 1>&2
  sudo "$0" "$@"
  exit $?
fi

if [ -n "$(command -v yum)" ]; then
  yum install python3.6
elif [ -n "$(command -v apt-get)" ]; then
  apt-get install python3.6
elif [ -n "$(command -v apt)" ]; then
  apt install python3.6
else
  echo "Unsupported OS" 1>&2
  exit 1
fi

python3.6 -m venv venv
venv/bin/python3.6 -m pip install -U -r autorooms-requirements.txt

if [[ `/sbin/init --version` =~ upstart ]]; then
  echo "start on runlevel [2345]" > /etc/init/discord-autorooms.conf
  echo "stop on runlevel [016]" >> /etc/init/discord-autorooms.conf
  echo "\nrespawn" >> /etc/init/discord-autorooms.conf
  echo "chdir $(pwd)" >> /etc/init/discord-autorooms.conf
  echo "setuid $(whoami)" >> /etc/init/discord-autorooms.conf
  echo "setgid $(id -gn "$(whoami)")" >> /etc/init/discord-autorooms.conf
  echo "env AUTOROOMTOKEN=$1" >> /etc/init/discord-autorooms.conf
  echo "exec $(pwd)/venv/bin/python3.6 autorooms.py" >> /etc/init/discord-autorooms.conf
  echo "Created upstart job named: discord-autorooms"
  start discord-autorooms
elif [[ `systemctl` =~ -\.mount ]]; then
  echo "AUTOROOMTOKEN='$1'" > autorooms.env
  echo "[Unit]" > /etc/systemd/system/discord-autorooms.service
  echo "Description=Discord-AutoRooms" >> /etc/systemd/system/discord-autorooms.service
  echo "After=multi-user.target" >> /etc/systemd/system/discord-autorooms.service
  echo "[Service]" >> /etc/systemd/system/discord-autorooms.service
  echo "EnvironmentFile=-$(pwd)/autorooms.env" >> /etc/systemd/system/discord-autorooms.service
  echo "WorkingDirectory=$(pwd)" >> /etc/systemd/system/discord-autorooms.service
  echo "User=$(whoami)" >> /etc/systemd/system/discord-autorooms.service
  echo "Group=$(id -gn "$(whoami)")" >> /etc/systemd/system/discord-autorooms.service
  echo "ExecStart=$(pwd)/venv/bin/python3.6 $(pwd)/autorooms.py" >> /etc/systemd/system/discord-autorooms.service
  echo "Type=idle" >> /etc/systemd/system/discord-autorooms.service
  echo "Restart=always" >> /etc/systemd/system/discord-autorooms.service
  echo "RestartSec=15" >> /etc/systemd/system/discord-autorooms.service
  echo "\n[Install]" >> /etc/systemd/system/discord-autorooms.service
  echo "WantedBy=multi-user.target" >> /etc/systemd/system/discord-autorooms.service
  systemctl start discord-autorooms.service
  systemctl enable discord-autorooms.service
  echo "Created and enabled systemd unit discord-autorooms.service"
else
  echo "This script only works for setting up autorooms on systems using upstart or systemd" 1>&2
  exit 1
fi
