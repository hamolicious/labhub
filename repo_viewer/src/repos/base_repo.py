from ..files import Directory, File


class Repository:
    def __init__(self, token: str, host: str, ref: str = "main") -> None:
        self.host = host
        self.ref = ref
        self._token = token

    def ls(self, path: str = "/") -> list[Directory | File]:
        raise NotImplementedError()
