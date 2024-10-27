# labhub

Seamlessly work with with Github, Gitlab and self-hosted Gitlab repositories using one interface.

> Currently supports read-only operations.

## Install

```bash
pip install labhub
```

## Useage

```python
# import repos and types
from labhub  import GitHubRepo, GitLabRepo, Directory, File

# Create repo objects
gh = GitHubRepo("hamolicious/test-repo", github_token, ref=ref)
gl = GitLabRepo(53, gitlab_token, host="https://gitlab.selfhosted.byme", ref=ref)

# list files in repo
files: list[Directory | File] = gh.ls(path)

# file operations
f_or_d = gh.ls()[0]
f_or_d.name # base name 'README.md'
f_or_d.path # file and path 'a/b/c'

f.get_data() # bytes
d.contents # list[File | Directory]
```

