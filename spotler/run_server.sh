#!/usr/bin/env bash

#Source your CLIEND_ID and CLIEND_SECRET from .env file

# set -a
# source api/spotify_wrapper/spotify-wrapper-config.env
# set +a


python manage.py runserver 0.0.0.0:8080
