#!/bin/bash
# This script runs the market basket analysis.
# It changes to the script's directory to ensure paths are correct.
cd "$(dirname "$0")"
python3 analysis.py >> analysis.log 2>&1
