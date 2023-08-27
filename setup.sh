#!/bin/bash
# This script is used to initialize the development environment

if ! command -v python3.11 &> /dev/null; then
	echo "python3.11 could not be found"
	return 1
fi

echo "Creating python3.11 virtual environment"
python3.11 m venv ./.venv
source ./.venv/Scripts/activate
pip install -r requirements.txt
echo "Setting up precommit hooks"
pre-commit install --hook-type commit-msg --hook-type pre-commit
pre-commit run --all-files

# C:\Users\talia\AppData\Local\Microsoft\WindowsApps\python3.11.exe
