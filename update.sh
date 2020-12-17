#!/bin/sh

UPSTREAM=${1:-'@{u}'}
LOCAL=$(git rev-parse @)
REMOTE=$(git rev-parse "$UPSTREAM")

echo "Checking for updates..."
git fetch

if [ $LOCAL != $REMOTE ]
then
    echo "Update available, pulling..."
    git pull
else [ $LOCAL = $REMOTE ]
    echo "No updates available."
fi
