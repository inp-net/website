#!/usr/bin/env sh
python projects/clone.py https://git.inpt.fr/api/graphql net7 $@
ortfodb projects --scattered build to database.json --config ortfodb.yaml
