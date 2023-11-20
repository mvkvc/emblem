#! /bin/bash

echo "export"
poetry run nbdev_export
echo "readme"
poetry run nbdev_readme
echo "clean"
poetry run nbdev_clean
echo "install"
poetry run pip install -e '.[dev]'
