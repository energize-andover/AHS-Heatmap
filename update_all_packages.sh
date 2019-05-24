#! /bin/bash
pip list --outdated --format=freeze | grep -v '^\-e' | cut -d = -f 1  | xargs -n1 pip install -U

# Prompt
read -p "Would you like to update requirements.txt? (Y/N)" -n 1 -r
echo # move to new line
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    exit 1
fi

pip freeze > requirements.txt
