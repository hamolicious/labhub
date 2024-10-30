from __future__ import annotations

from pathlib import Path
from typing import Callable, Optional


class File:
    def __init__(self, name: str, path: Path | str, data_closure: Callable[[], bytes]):
        self.name: str = name
        self.path: Path = Path(path)

        self.data_closure: Callable[[], bytes] = data_closure
        self._data: Optional[bytes] = None

    def get_data(self) -> bytes:
        if self._data is None:
            self._data = self.data_closure()
        return self._data

    def __repr__(self):
        return self.name


class Directory:
    def __init__(self, name: str, path: Path | str, contents: list[File | Directory]):
        self.name: str = name
        self.path = path
        self._contents: list[File | Directory] = contents

    @property
    def contents(self) -> list[File | Directory]:
        self._contents.sort(key=lambda f: f.name)
        return self._contents

    def add_file(self, file: File | Directory) -> None:
        self._contents.append(file)

    def __repr__(self):
        return f"{self.name}/"
