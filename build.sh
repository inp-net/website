#!/usr/bin/env sh
poetry run python projects/clone.py https://git.inpt.fr/api/graphql net7 $@
if [[ ! -f ortfodb ]]; then
    curl -fsSL https://github.com/ortfo/db/releases/download/v0.1.0/ortfodb -o ortfodb
fi
chmod +x ortfodb
./ortfodb projects --scattered build to database.json --config ortfodb.yaml
poetry run python build_projects_page.py
