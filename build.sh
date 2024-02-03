#!/usr/bin/env sh
poetry run python projects/clone.py https://git.inpt.fr/api/graphql net7 $@
ortfodb projects --scattered build to database.json --config ortfodb.yaml
poetry run python build_projects_page.py
