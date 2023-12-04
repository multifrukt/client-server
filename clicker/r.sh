#!/bin/bash
set -x

docker run \
    --rm \
    -e "URL_TO_CLICK=http://webfront/" \
    -e "RETRY_ON_SUCCESS_INTERVAL=1" \
    -e "RETRY_ON_FAILURE_INTERVAL=1" \
    clicker
