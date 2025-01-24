#!/bin/bash

# set python version to build venv from
PYTHON="python3.12"

$PYTHON -m venv --symlinks --clear venv || exit 1
. ./venv/bin/activate || exit 1
python -m pip install -r requirements.txt

./download_imdb_data.sh
