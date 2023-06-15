#!/usr/bin/env bash

set -a
source api/spotify_wrapper/spotify-wrapper-config.env
set +a


python manage.py runserver 8080
