#!/bin/bash

if [ ${1:-out} = out ]
then
    npm run build
else
    if [ -d "./out" ]; then
        read -p "This will remove the 'out' directory found here. Are you sure? [y/n] -> " -n 1 -r
        echo    # (optional) move to a new line
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            rm -rf out
        fi
    fi
    npm run build -- --outDir $1
fi