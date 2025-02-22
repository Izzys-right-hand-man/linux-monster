#!/bin/bash

# Function to display usage
usage() {
    echo "Usage: $0 [-f requirements.txt] [-p package1 package2 ...]"
    echo "Options:"
    echo "  -f FILE       Install packages listed in a requirements.txt file."
    echo "  -p PACKAGES   Install packages directly (space-separated list)."
    exit 1
}

# Check if Python is installed
if ! command -v python3 &>/dev/null; then
    echo "Python3 is not installed. Please install Python3 first."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &>/dev/null; then
    echo "pip is not installed. Installing pip..."
    python3 -m ensurepip --upgrade || {
        echo "Failed to install pip. Exiting."
        exit 1
    }
fi

# Parse arguments
while getopts "f:p:" opt; do
    case $opt in
    f)
        FILE=$OPTARG
        if [[ -f "$FILE" ]]; then
            echo "Installing packages from $FILE..."
            pip3 install -r "$FILE"
        else
            echo "Error: File $FILE not found."
            exit 1
        fi
        ;;
    p)
        PACKAGES=$OPTARG
        echo "Installing packages: $PACKAGES..."
        pip3 install $PACKAGES
        ;;
    *)
        usage
        ;;
    esac
done

# If no arguments were provided
if [ $OPTIND -eq 1 ]; then
    usage
fi

echo "Installation complete."