#!/usr/bin/env python
import subprocess

import requests


def gql(endpoint: str, query: str, variables: dict) -> dict:
    response = requests.post(
        endpoint,
        json={"query": query, "variables": variables},
    )
    return response.json()

def clone_repo(url: str, to: str) -> str:
    subprocess.run(["git", "clone", "--depth", "1", url, to])
    print("-" * 80)

def update_repo(path: str) -> str:
    subprocess.run(["git", "reset", "--hard", "HEAD"], cwd=path)
    subprocess.run(["git", "pull"], cwd=path)
    print("-" * 80)

def gql_unroll_paginated(endpoint: str, query: str, variables: dict, get_next_cursor: callable) -> list:
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

    repositories = gql_unroll_paginated(endpoint, query, {
        "topics": topics,
        "descriptionPaths": [".ortfo/description.md"],
    }, get_next_cursor=lambda response: response["data"]["projects"]["pageInfo"]["endCursor"])

    for repo in repositories:
        path = repo["path"]
        if '/' in path:
            print(f"{path}: Projects in subgroups are not supported, skipping")
            continue
        full_path = here / path
        if repo["repository"]["blobs"]["nodes"]:
            if Path(full_path).exists():
                print(f"{path}: Already cloned, updating...")
                update_repo(full_path)
            else:
                print(f"{path}: Cloning...")
                clone_repo(repo["httpUrlToRepo"], full_path)
