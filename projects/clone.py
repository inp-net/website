#!/usr/bin/env python
import re
import subprocess

import requests

pad_length = len("       Finished")


def gql(endpoint: str, query: str, variables: dict) -> dict:
    response = requests.post(
        endpoint,
        json={"query": query, "variables": variables},
    )
    return response.json()


def clone_repo(url: str, to: str) -> str:
    try:
        subprocess.run(
            ["git", "clone", "--depth", "1", url, to], capture_output=True, check=True
        )
    except subprocess.CalledProcessError as e:
        print(e.stderr.decode())


def update_repo(path: str) -> str:
    try:
        subprocess.run(
            ["git", "reset", "--hard", "HEAD"],
            cwd=path,
            capture_output=True,
            check=True,
        )
        subprocess.run(["git", "pull"], cwd=path, capture_output=True, check=True)
    except subprocess.CalledProcessError as e:
        print(e.stderr.decode())


def gql_unroll_paginated(
    endpoint: str, query: str, variables: dict, get_next_cursor: callable
) -> list:
    result = []
    while True:
        response = gql(endpoint, query, variables)
        result.extend(response["data"]["projects"]["nodes"])
        if not response["data"]["projects"]["pageInfo"]["hasNextPage"]:
            break
        variables["cursor"] = get_next_cursor(response)
    return result


if __name__ == "__main__":
    import sys
    from pathlib import Path

    here = Path(__file__).parent

    if len(sys.argv) < 3:
        print(f"Usage: {Path(sys.argv[0]).name} <endpoint> <topic>...")
        sys.exit(1)

    endpoint = sys.argv[1]
    topics = sys.argv[2:]

    query = """
    query repos($topics: [String!], $cursor: String, $descriptionPaths: [String!]!) {
      projects(topics: $topics, first: 100, after: $cursor) {
        pageInfo {
          hasNextPage
          endCursor
        }
        nodes {
          path
          httpUrlToRepo
          repository {
            blobs(paths: $descriptionPaths) {
              nodes {
                path
              }
            }
          }
        }
      }
    }
    """

    description_paths = []
    for line in Path(here / "../ortfodb.yaml").read_text().splitlines():
        if (
            match := re.compile(r"scattered mode folder: (.*)").match(line)
        ) is not None:
            description_paths.append(Path(match.group(1)) / "description.md")

    print(
        f"{'Searching':>{pad_length}} repositories with {', '.join(map(str, description_paths))} and topics {', '.join(map(str, topics))}"
    )

    repositories = gql_unroll_paginated(
        endpoint,
        query,
        {
            "topics": topics,
            "descriptionPaths": [str(p) for p in description_paths],
        },
        get_next_cursor=lambda response: response["data"]["projects"]["pageInfo"][
            "endCursor"
        ],
    )

    for repo in repositories:
        path = repo["path"]
        if "/" in path:
            print(f"{'Skipped':>{pad_length}} {path} (subgroups are not supported)")
            continue
        full_path = here / path
        if repo["repository"]["blobs"]["nodes"]:
            if Path(full_path).exists():
                print(f"{'Updating':>{pad_length}} {path}")
                update_repo(full_path)
            else:
                print(f"{'Cloning':>{pad_length}} {path}")
                clone_repo(repo["httpUrlToRepo"], full_path)
