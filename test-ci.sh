#!/bin/bash -e

GCLOUD_KEY_FILE=ci-key.json GCLOUD_PROJECT_ID=nearbyhouseprices node server.js &
SERVER_PID=$!

cleanup () {
    if ps -p $SERVER_PID > /dev/null; then
        kill -9 $SERVER_PID
    fi
}

trap cleanup EXIT ERR INT TERM

cd test
./node_modules/.bin/jest
