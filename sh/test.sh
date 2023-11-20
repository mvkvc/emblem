#! /bin/bash

echo "export"
nbdev_export
echo "install"
pip install -e '.[dev]'
echo "test"
nbdev_test
