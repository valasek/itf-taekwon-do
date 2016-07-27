#!/usr/bin/env sh
# Script to run app in debug mode
export FLASK_DEBUG=1
export FLASK_CONFIGURATION=dev
export FLASK_APP=itf.py
flask run --host=0.0.0.0
