#!/bin/bash

sudo apt update
pip3 install psycopg2-binary
git clone https://github.com/chyornyy/youtello.git 
cd youtello
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
nano .env

cd
sudo bash -c 'echo "[Unit]
Description=bot daemon
After=network.target

[Service]
User=admin
WorkingDirectory=/home/admin/youtello/
ExecStart=sudo /home/admin/youtello/python3 main.py
[Install]
WantedBy=multi-user.target" > /etc/systemd/system/bot.service'