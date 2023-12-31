#!/bin/bash
set -euo pipefail

# Sync the files.
rsync -rh --delete --exclude '.venv/' --exclude '__pycache__' --progress ./* radiopi:/opt/radiopi/
