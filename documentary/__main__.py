from os import path, getcwd

from documentary.args import parse_args
from documentary.document import document


def main():
    args = parse_args()

    documentary_path = path.join(getcwd(), 'documentary')
    documentation_path = path.join(getcwd(), 'documentary', args.template)
    template_path = path.join(getcwd(), args.template)

    if not path.exists(documentary_path):
        print('To generate a documentation, navigate to a directory with "documentary" folder')
        return

    if not path.exists(template_path):
        print(f'Tried to documentation file "{template_path}", but it doesn\'t exist')
        return

    if not path.exists(documentation_path):
        print(f'Directory "{path.normpath(args.template)}" is missing in documentary folder')
        return

    document(documentary_path, documentation_path, template_path, output_path=template_path)


if __name__ == '__main__':
    main()
