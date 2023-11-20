#! /bin/bash

poetry export -f requirements.txt > ./requirements.txt
poetry export --with=dev -f requirements.txt > ./requirements.dev.txt
