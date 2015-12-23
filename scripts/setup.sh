#!/bin/bash

echo "Updating system..."
sudo apt-get -y update
sudo apt-get -y upgrade

echo "Installing dependencies..."
sudo apt-get -y install python-pip libmysqlclient-dev

echo "Installing pip dependencies..."
sudo pip install -r scripts/requirements.txt

echo 'PATH=$PATH:/vagrant' >> /etc/profile