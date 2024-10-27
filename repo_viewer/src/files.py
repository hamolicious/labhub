from __future__ import annotations

from pathlib import Path


class File:
    def __init__(self, name: str, path: Path | str, data: bytes):
        self.name: str = name
        self.path: Path = Path(path)

        self.data: bytes = data

    def write(self, target_dir: Path, ignore_own_path: bool = False) -> None:
        path = target_dir / self.path

        if ignore_own_path:
            path = target_dir

        with open(path, "wb") as f:
            f.write(self.data)

    def __repr__(self):
        return self.name


class Directory:
    def __init__(self, name: str, path: Path | str, contents: list[File | Directory]):
        self.name: str = name
        self.path = path
        self.contents: list[File | Directory] = contents

    def add_file(self, file: File | Directory) -> None:
        self.contents.append(file)

    def __repr__(self):
        return f"{self.name}/"
