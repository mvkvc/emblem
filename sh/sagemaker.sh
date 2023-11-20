#!/bin/bash

set -eux

GITUSERNAME="Marko Vukovic"
GITEMAIL="mvkvc.git@gmail.com"

git config --global user.name "${GITUSERNAME}"
git config --global user.email "${GITEMAIL}"
git config pull.rebase false

REQS="$HOME/emblem/requirements.dev.txt"

if [ -f "$REQS" ]; then
    pip install -r "$REQS"
else
    echo "No requirements file found at $REQS"
fi
