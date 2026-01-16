#!/bin/bash

echo "========================================"
echo "Flight Management System - Startup"
echo "========================================"
echo

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo

# Check if requirements are installed
echo "Checking dependencies..."
if ! pip show flask > /dev/null 2>&1; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
    echo
else
    echo "Dependencies already installed."
    echo
fi

# Check for .env file
if [ ! -f ".env" ]; then
    echo "WARNING: .env file not found!"
    echo "Please create a .env file based on .env.example"
    echo
    exit 1
fi

# Start the application
echo "Starting Flight Service..."
echo "Press Ctrl+C to stop the server"
echo
python run.py
