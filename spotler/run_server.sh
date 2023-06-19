#!/usr/bin/env bash

set -a
source api/spotify_wrapper/spotify-wrapper-config.env
set +a


python manage.py runserver 0.0.0.0:8080
