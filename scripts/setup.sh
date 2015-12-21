#!/bin/bash

echo "Updating system..."
apt-get -y update
apt-get -y upgrade

echo "Installing dependencies..."
apt-get -y install python-pip

echo "Installing pip dependencies..."
pip install -r scripts/requirements.txt