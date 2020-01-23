import os
from os import path
from pathlib import Path


def discover_templates(folder: str, root: str, documentary: str) -> list:
    absolute = path.join(root, folder)
    if path.isfile(absolute):
        return [folder]
    if path.isdir(absolute):
        return relative_paths(template_files(folder, root, documentary), documentary)
    raise FileNotFoundError(f"File/folder '{folder}' does not exist")


def relative_paths(filenames: list, root: str) -> list:
    return [strip(f, root) for f in filenames]


def template_files(folder: str, root: str, documentary: str) -> list:
    result = []
    for filename in folders(folder, documentary):
        if path.isfile(path.join(root, strip(filename, documentary))):
            result.append(filename)
    return result


def folders(folder: str, documentary: str) -> list:
    parent = path.join(documentary, folder)
    try:
        return [parent, *deep_scandir(parent)]
    except FileNotFoundError:
        raise TemplatesDiscoveryException(f"File/folder '{folder}' is not documented")


def deep_scandir(root):
    result = [f.path for f in os.scandir(root) if f.is_dir()]
    for root in list(result):
        result.extend(deep_scandir(root))
    return result


def strip(string: str, prefix: str) -> str:
    parent = Path(prefix)
    son = Path(string)
    if parent in son.parents:
        return str(son.relative_to(parent))
    return str(son)


class TemplatesDiscoveryException(Exception):
    pass