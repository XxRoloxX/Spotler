#!/usr/bin/env bash

set -a
source spotler/api/spotify-wrapper-config.env
set +a


python request_localhost.py $1