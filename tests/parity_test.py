from os import environ

from repo_viewer import GitHubRepo, GitLabRepo
from repo_viewer.src.files import File


def create_gh_gl(ref: str = "main"):
    github_token = environ.get("GITHUB_TOKEN")
    assert github_token is not None

    gitlab_token = environ.get("GITLAB_TOKEN")
    assert gitlab_token is not None

    gh = GitHubRepo("hamolicious/test-repo", github_token, ref=ref)
    gl = GitLabRepo(53, gitlab_token, host="https://gitlab.slayhouse.net", ref=ref)
    return gh, gl


gh, gl = create_gh_gl()


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
    files_gl: list[File] = [f for f in gl.ls() if isinstance(f, File)]

    fa = list(map(lambda f: f.get_data(), files_gl))
    fb = list(map(lambda f: f.get_data(), files_gh))

    assert fa == fb


# TODO: implement lazy loading
def x_test_file_contents_loaded_lazily() -> None:
    print("start")
    files_gh: list[File] = [f for f in gh.ls() if isinstance(f, File)]
    files_gl: list[File] = [f for f in gl.ls() if isinstance(f, File)]

    assert files_gh[0]._data is None
    assert files_gl[0]._data is None

    files_gh[0].get_data()
    files_gl[0].get_data()

    assert files_gh[0]._data is not None
    assert files_gl[0]._data is not None


def test_ref_parity() -> None:
    """
    Make sure that both retrieve the same files on a non-main branch
    and that they both retrieve the same files on the main branch

    finally, check that the files between the 2 branches are not the same (sanity check)
    """
    gl, gh = create_gh_gl(ref="other-branch")

    files_gh: list[File] = [f for f in gh.ls() if isinstance(f, File)]
    files_gl: list[File] = [f for f in gl.ls() if isinstance(f, File)]

    fa1 = list(map(lambda f: f.name, files_gl))
    fb1 = list(map(lambda f: f.name, files_gh))
    assert fa1 == fb1

    gl, gh = create_gh_gl(ref="main")

    files_gh = [f for f in gh.ls() if isinstance(f, File)]
    files_gl = [f for f in gl.ls() if isinstance(f, File)]

    fa2 = list(map(lambda f: f.name, files_gl))
    fb2 = list(map(lambda f: f.name, files_gh))
    assert fa1 == fb1

    assert fa1 != fa2
    assert fb1 != fb2
