#!/usr/bin/env bash

set -a
source api/spotify-wrapper-config.env
set +a


python manage.py runserver 3000