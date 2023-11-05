#!/bin/bash

# Update system packages
echo "Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install Python, pip, and other necessary tools
echo "Installing Python, pip, and other necessary tools..."
sudo apt install -y python3 python3-pip git

# Clone your API repository (replace with your repo's URL)
echo "Cloning API repository..."
git clone https://github.com/shojaei-mohammad/LynxAPI.git
cd LynxAPI

# Install Python dependencies
echo "Installing Python dependencies..."
pip3 install -r requirements.txt



echo "Setup completed!"
