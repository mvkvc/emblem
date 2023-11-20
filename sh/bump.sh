#! /bin/bash

poetry run nbdev_bump_version
poetry run bump-my-version bump --current-version $(poetry version | cut -d' ' -f2) minor --config-file ./pyproject.toml
