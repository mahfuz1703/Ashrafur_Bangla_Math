#!/bin/bash


echo "Building the project"
python3 -m pip install -r requirements.txt


echo "Migrating database"
python3 manage.py makemigrations --noinput
python3 manage.py migrate --noinput

