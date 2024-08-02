#!/bin/bash

rm db.sqlite3
rm -rf ./movieapi/migrations
python3 manage.py migrate
python3 manage.py makemigrations movieapi
python3 manage.py migrate movieapi
python3 manage.py loaddata users
python3 manage.py loaddata tokens
python3 manage.py loaddata genres
python3 manage.py loaddata movies
python3 manage.py loaddata usermovies
python3 manage.py loaddata likedmovies



