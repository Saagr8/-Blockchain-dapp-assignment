
#!/bin/bash

# Hotel Booking DApp - Start Script

echo "================================"
echo "    HOTEL BOOKING BLOCKCHAIN"
echo "================================"

# Go to the main project directory
cd "$(dirname "$0")/.."

# Check if Python virtual environment exists
if [ ! -f ".venv/Scripts/python.exe" ]; then
    echo "Error: Python virtual environment not found."
    exit 1
fi

echo "Starting Hotel Booking Application..."

# Run the Python application
.venv/Scripts/python.exe python/app.py
