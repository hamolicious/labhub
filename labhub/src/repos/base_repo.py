from pathlib import Path
from typing import Optional

from ..files import Directory, File


class Repository:
    def __init__(self, token: str, host: str, ref: str = "main") -> None:
        self.host = host
        self.ref = ref
        self._token = token
        self.__root_dir: Optional[Directory] = None

    def _walk_tree(self, directory_path: str, ref: str = "main") -> Directory:
        raise NotImplementedError()

    @property
    def _root_dir(self) -> Directory:
        if self.__root_dir is None:
            self.__root_dir = self._walk_tree("", ref=self.ref)

        return self.__root_dir

    def ls(self, path: Path | str = "") -> list[Directory | File]:
        if self._root_dir is None:
            raise RuntimeError("Contents was not loaded")

        components = str(path).split("/")
        curr_dir: Directory = self._root_dir
        for component in components:
            for file in curr_dir.contents:
                if component == file.name and isinstance(file, Directory):
                    curr_dir = file

        return curr_dir.contents
