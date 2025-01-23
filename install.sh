#! /bin/bash

python -m venv --symlinks --clear venv

. ./venv/bin/activate

python -m pip install -r requirements.txt
