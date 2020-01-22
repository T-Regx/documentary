from os import path


def resource(filename: str) -> str:
    return path.join(path.dirname(__file__), 'resources', filename)
