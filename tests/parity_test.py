from os import environ

from repo_viewer import GitHubRepo, GitLabRepo
from repo_viewer.src.files import File

github_token = environ.get("GITHUB_TOKEN")
assert github_token is not None
print(github_token)

gitlab_token = environ.get("GITLAB_TOKEN")
assert gitlab_token is not None

gh = GitHubRepo("hamolicious/test-repo", github_token)
gl = GitLabRepo(53, gitlab_token, host="https://gitlab.slayhouse.net")


def test_ls_parity() -> None:
    files_gh = gh.ls()
    files_gl = gl.ls()

    fa = list(map(lambda f: f.name, files_gl))
    fb = list(map(lambda f: f.name, files_gh))
    assert fa == fb

    fa = list(map(lambda f: str(f.path), files_gl))
    fb = list(map(lambda f: str(f.path), files_gh))
    assert fa == fb


def test_file_parity() -> None:
    files_gh: list[File] = [f for f in gh.ls() if isinstance(f, File)]
    files_gl: list[File] = [f for f in gh.ls() if isinstance(f, File)]

    fa = list(map(lambda f: f.data, files_gl))
    fb = list(map(lambda f: f.data, files_gh))

    assert fa == fb
