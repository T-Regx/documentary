import os


def map_file(template: str, output: str, mapper: callable) -> None:
    with open(template, "r") as file:
        content = file.read()

    _create_directory_for_file(output)
    new_content = mapper(content)
    with open(output, "w+") as file:
        file.write(new_content)


def _create_directory_for_file(path: str):
    d = file_directory(path)
    if not os.path.exists(d):
        os.makedirs(d)


def file_directory(path):
    return os.path.dirname(os.path.abspath(path))


def fragment_fallback(path: str, filename: str, second_filename: str = None) -> str:
    return __fragment_or(
        path,
        filename,
        lambda: __fragment_or(path, second_filename, lambda: '') if second_filename else '')


def fragment(path: str, filename: str) -> str:
    def missing_fragment():
        raise MissingFragmentException(filename)

    return __fragment_or(path, filename, missing_fragment)


def __fragment_or(path: str, filename: str, default: callable) -> str:
    try:
        with open(os.path.join(path, filename + ".html"), "r") as file:
            return file.read()
    except FileNotFoundError:
        return default()


class MissingFragmentException(Exception):
    pass
