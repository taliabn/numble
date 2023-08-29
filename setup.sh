#!/bin/bash
# This script is used to initialize the development environment

if ! command -v python3.11 &> /dev/null; then
	echo "python3.11 could not be found"
	return 1
fi

echo "Creating python3.11 virtual environment"
python3.11 -m venv ./.venv
if [ -d ".venv/Scripts" ]
then
    source .venv/Scripts/activate # windows
else
    source .venv/bin/activate # mac/linux
fi
pip install -r requirements.txt
echo "Setting up precommit hooks"
pre-commit install --hook-type commit-msg --hook-type pre-commit
pre-commit run --all-files
echo "Importing environment variables"
set -o allexport
source .env
set +o allexport
exit 0
