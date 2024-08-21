#!/bin/bash
cd /root/flask_dokku_manager
git pull origin master
systemctl restart flask_app
