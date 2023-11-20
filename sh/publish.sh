#! /bin/bash

./sh/build.sh
./sh/bump.sh
poetry build
poetry run python -m twine upload --repository pypi dist/*
