from os import environ

from repo_viewer import GitHubRepo

github_token = environ.get("GITHUB_TOKEN")
assert github_token is not None

gh = GitHubRepo("hamolicious/test-repo", github_token)

print(gh.ls())
