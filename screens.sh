#!/bin/bash

if [[ -z $STY ]]; then
    echo "Doesn't look like we're inside a screen session."
    exit 1
fi

EXCLUDES=\
"setup.py
__init__.py
ext
line.py
test_line.py"

PY_FILES=$(find . -iname \*.py)

for file in $(echo "$PY_FILES" | grep -v -f <(echo "$EXCLUDES")); do
    screen_name=$(basename $file)
    screen -S $STY -X screen -t ${screen_name/.py/} vim $file
done
