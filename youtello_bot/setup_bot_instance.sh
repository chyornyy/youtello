#!/bin/bash

sudo apt update
sudo apt install python3-pip -y
sudo apt install python3.10-venv -y
git clone https://github.com/chyornyy/youtello.git 
cd youtello
pip3 install -r requirements.txt
pip3 install psycopg2-binary
nano .env

cd
sudo bash -c 'echo "[Unit]
Description=bot daemon
After=network.target

[Service]
User=admin
WorkingDirectory=/home/admin/youtello/
ExecStart=python3 /home/admin/youtello/main.py
[Install]
WantedBy=multi-user.target > /etc/systemd/system/bot.service'
sudo systemctl start bot
sudo systemctl status bot 
sudo systemctl enable bot.service