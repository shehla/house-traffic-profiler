#!/bin/bash

sudo apt-get update
sudo apt-get install python-virtualenv -y
sudo apt-get install git -y
sudo pip install Flask
sudo pip install yahoo-finance

sudo sh -c 'echo "deb https://pkg.tox.chat/debian nightly release" | sudo tee /etc/apt/sources.list.d/tox.list'
wget -qO - https://pkg.tox.chat/debian/pkg.gpg.key | sudo apt-key add -
sudo apt-get install apt-transport-https -y
sudo apt-get update
sudo apt-get install qtox-unity -y
sudo apt-get install python-numpy python-scipy python-matplotlib ipython ipython-notebook python-pandas python-sympy python-nose -y

echo "Before user change User name is:"
echo $USER
echo "Before user change Home dir is:"
echo $HOME
(crontab -l ; echo '*/10 * * * * python /root/work/cool_predictions/cool_predictions/check_and_generate_best_stocks.py > /root/work/cool_predictions/cron_best_stocks.log') | crontab -
mkdir /root/work && cd /root/work && git clone https://shehla:Qur12345@bitbucket.org/shehla/cool_predictions.git

echo "User name is:"
echo $USER
echo "Home dir is:"
echo $HOME

