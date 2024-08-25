#!/usr/bin/env bash
set -euxo pipefail

poetry run python projects/clone.py https://git.inpt.fr/api/graphql "sur net7.dev" $@
if [[ ! -f ortfodb ]]; then
    curl -fsSL https://github.com/ortfo/db/releases/download/v0.3.1/ortfodb-gblic2.36 -o ortfodb
fi
chmod +x ortfodb
./ortfodb projects --scattered build to database.json --config ortfodb.yaml
poetry run python build_projects_page.py
