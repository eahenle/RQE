#! /bin/bash

python -m venv --symlinks --clear --upgrade-deps venv

. ./venv/bin/activate

python -m pip install -r requirements.txt
