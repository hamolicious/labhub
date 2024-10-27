import os
from functools import partial
from pathlib import Path
from typing import Optional

from gitlab import Gitlab, exceptions

from .base_repo import Directory, File, Repository


class GitLabRepo(Repository):
    def __init__(
        self,
        project_id: int,
        token: str,
        host: str = "https://gitlab.com",
        ref: str = "main",
    ) -> None:
        super().__init__(token, host, ref)

        self._project_id = project_id
        self._gl = Gitlab(host, token)
        self._project = self._gl.projects.get(self._project_id)

    def _get_raw_files(
        self, remote_directory: str, ref: str = "main"
    ) -> list[dict[str, str]]:
        try:
            files = self._project.repository_tree(path=remote_directory, ref=ref)
        except exceptions.GitlabError as e:
            if e.args == ("404 Tree Not Found",):
                print(f"ref '{ref}' could not be found")
                quit()
            else:
                raise e
        return list(files)

    def _walk_tree(self, directory_path: str, ref: str = "main") -> Directory:
        def _get_contents(path: str, ref: str) -> bytes:
            f = self._project.files.get(path, ref=ref)
            return f.decode()

        directory = Directory(os.path.basename(directory_path), directory_path, [])
        files = self._get_raw_files(directory_path, ref)

        for file_info in files:
            name = str(file_info.get("name"))
            path = str(file_info.get("path"))

            if file_info.get("type") == "blob":
                directory.add_file(
                    File(
                        name,
                        path,
                        partial(_get_contents, path, ref),
                    )
                )
            else:
                directory.add_file(self._walk_tree(path, ref=ref))

        return directory
