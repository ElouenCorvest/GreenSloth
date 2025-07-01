#!/bin/bash

if [ ${1:-public} = public ]
then
    npm run build
else
    if [ -d "./public" ]; then
        read -p "This will remove the 'public' directory found here. Are you sure? [y/n] -> " -n 1 -r
        echo    # (optional) move to a new line
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            rm -rf public
        fi
    fi
    npm run build -- --outDir $1
fi