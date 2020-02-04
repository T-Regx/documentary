from argparse import Namespace
from os import path


def resolve_paths(cwd: str, args: Namespace) -> tuple:
    root_path = cwd
    documentary_path = path.join(root_path, 'documentary')
    documentation_path = path.join(root_path, 'documentary', args.template)
    template_path = path.join(root_path, args.template)

    if not path.exists(documentary_path):
        raise Exception('To generate a documentation, navigate to a directory with "documentary" folder')

    if not path.exists(template_path):
        raise Exception(f'Tried to documentation file "{template_path}", but it doesn\'t exist')

    if not path.exists(documentation_path):
        raise Exception(f'Directory "{path.normpath(args.template)}" is missing in documentary folder')

    return documentary_path, root_path, args.template, root_path
