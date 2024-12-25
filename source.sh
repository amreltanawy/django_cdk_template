#!/bin/bash

# The sole purpose of this script is to make the command
#
#     source .venv/bin/activate
#
# work consistently across platforms (Linux, Mac OS X, and Windows).
# On Unix-like systems, this directly sources the activation script.
# 
# Now we have a consistent command across all platforms.

# Check if the virtual environment exists
if [ -f ".venv/bin/activate" ]; then
    # Source the activation script
    . .venv/bin/activate
else
    echo "Error: Virtual environment not found in .venv/bin/activate"
    exit 1
fi 