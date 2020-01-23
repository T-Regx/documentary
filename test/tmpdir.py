import os
from shutil import rmtree
from tempfile import mkdtemp
from typing import Union


def directory():
    return _TemporaryDirectory()


class _TemporaryDirectory:
    def __enter__(self):
        self.test_dir = mkdtemp()
        return _Handle(self.test_dir)

    def __exit__(self, exc_type, exc_val, exc_tb):
        rmtree(self.test_dir)


class _Handle:
    def __init__(self, test_dir: str):
        self.test_dir = test_dir

    def store(self, filenames: Union[list, str], content: str):
        if type(filenames) is str:
            filenames = [filenames]
        if len(filenames) > 1:
            folder, _ = os.path.split(self.join(*filenames))
            os.makedirs(folder)
        with open(self.join(*filenames), 'w') as file:
            file.write(content)

    def dir(self, filenames: Union[list, str]):
        if type(filenames) is str:
            filenames = [filenames]
        os.makedirs(self.join(*filenames))

    def join(self, *filenames: str):
        return os.path.join(self.test_dir, *filenames)

    def open(self, *filenames: str) -> str:
        join = self.join(*filenames)
        with open(join, 'r') as file:
            return file.read()

    def clean(self, *filenames: str) -> list:
        return [self._clean_single(filename) for filename in filenames]

    def _clean_single(self, filename: str) -> str:
        return filename[len(self.test_dir):] if filename.startswith(self.test_dir) else filename
