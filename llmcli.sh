#!/bin/bash
create_and_activate_venv() {
    python3 -m venv env
    source env/bin/activate
    if [ -f requirements.txt ]; then
        pip install -r requirements.txt
    else
        echo "requirements.txt not found. Please provide a requirements.txt file and try again."
        exit 1
    fi
}
if ! python3 --version >/dev/null 2>&1; then
    echo "Python3 is not installed. Please install Python3 and try again."
    exit 1
fi
if [ -d "env" ]; then
    source env/bin/activate
else
    create_and_activate_venv
fi

python3 main.py
