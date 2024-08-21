git push origin master
git pull origin master

sudo systemctl restart flask_app
sudo systemctl status flask_app

sudo systemctl stop flask_app
sudo systemctl start flask_app