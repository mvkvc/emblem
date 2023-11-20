#! /bin/bash

echo "black"
poetry run nbqa black --check nbs/
echo "mypy"
poetry run nbqa mypy nbs/
