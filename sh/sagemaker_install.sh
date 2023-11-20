#!/bin/bash

set -eux

REQS="./emblem/requirements.dev.txt"

if [ -f "$REQS" ]; then
    pip install -r "$REQS"
else
    echo "No requirements file found at $REQS"
fi
