#!/bin/bash

# Check if Python 3.8.10 or greater is installed
required_version="3.8.10"
current_version=$(python3 -c "import sys; print(sys.version.split()[0])")

if [ "$(printf '%s\n' "$required_version" "$current_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "Python version $current_version is not compatible. Installing Python $required_version..."
    sudo apt-get install "python$required_version"
fi


# Update the package list
apt-get update

# Install pip
yes Y | apt-get install python3-pip

# Install requirements from requirements.txt
pip install -r requirements.txt -v
