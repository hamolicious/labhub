import os
from functools import partial
from os import environ
from typing import Optional

from github import Github
from github.Auth import Token
from github.ContentFile import ContentFile

from .base_repo import Directory, File, Repository


class GitHubRepo(Repository):
    def __init__(
        self,
        project_path: str,
        token: str,
        ref: str = "main",
    ) -> None:
        super().__init__(token, "https://github.com", ref)

        self.__root_dir: Optional[Directory] = None

        self._project_path = project_path
        auth = Token(token)
        self._gh = Github(auth=auth)
        self._repo = self._gh.get_repo(project_path)

    @property
    def _root_dir(self) -> Directory:
        if self.__root_dir is None:
            self.__root_dir = self._walk_tree("/", self.ref)

        return self.__root_dir

    def _get_raw_files(
        self, remote_directory: str, ref: str = "main"
    ) -> list[ContentFile]:
        try:
            files = self._repo.get_contents(remote_directory, ref=ref)
            if isinstance(files, ContentFile):
                return [files]
            return files
        except Exception:
            ...
            # if e.args == ("404 Tree Not Found",):
            #     print(f"ref '{ref}' could not be found")
            #     quit()
            # else:
            #     raise e

        return []

    def _walk_tree(self, directory_path: str, ref: str = "main") -> Directory:
        def _get_contents(file: ContentFile) -> bytes:
            print("fuck")
            return file.decoded_content

        directory = Directory(os.path.basename(directory_path), directory_path, [])
        files = self._get_raw_files(directory_path, ref)

        for file_info in files:
            if file_info.type == "file":
                directory.add_file(
                    File(
                        file_info.name,
                        file_info.path,
                        data_closure=partial(_get_contents, file_info),
                    )
                )
            else:
                directory.add_file(self._walk_tree(file_info.path, ref=ref))

        return directory

    def ls(self, path: str = "") -> list[Directory | File]:
        return self._root_dir.contents
