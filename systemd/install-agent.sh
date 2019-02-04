#!/usr/bin/env bash

mkdir -p /opt/dashboard
cd /opt/dashboard
curl -L -o agent.py https://raw.githubusercontent.com/chiwanpark/dashboard/master/dashboard/agent.py
curl -L -o agent.service https://raw.githubusercontent.com/chiwanpark/dashboard/master/systemd/agent.service
curl -L -o agent.timer https://raw.githubusercontent.com/chiwanpark/dashboard/master/systemd/agent.timer

mv agent.service /etc/systemd/system/agent.service
mv agent.timer /etc/systemd/system/agent.timer
systemctl daemon-reload
