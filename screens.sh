#!/bin/bash

PY_FILES="
xy
line
test_line
"
FILES="
rectree*
"

if [[ -z $STY ]]; then
    echo "Doesn't look like we're inside a screen session."
    exit 1
fi

for file in $PY_FILES; do
    py_files+="$file.py "
done

for file in $py_files $FILES; do
    screen -S $STY -X screen -t ${file/.py/} vim $file
done
