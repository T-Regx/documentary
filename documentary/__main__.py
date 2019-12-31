from os import path, getcwd

from documentary.args import parse_args
from documentary.template import document_file


def document(template_path: str, documentary_path: str) -> None:
    documented = document_file(
        template=template_path,
        output=template_path,
        declaration=path.join(documentary_path, 'declaration.json'),
        decorations=path.join(documentary_path, 'decorations.json'),
        definitions=path.join(documentary_path, 'definitions.json'),
        fragments=(path.join(documentary_path, 'fragments')),
        include_template_tag=True,
    )
    print(('Documented file "{}"' if documented else 'File "{}" remains unchanged').format(template_path))


def main():
    args = parse_args()

    documentary_path = path.join(getcwd(), 'documentary')
    method_path = path.join(getcwd(), 'documentary', args.template + '.documentation')
    template_path = path.join(getcwd(), args.template)

    if not path.exists(documentary_path):
        print('To generate a documentation, navigate to a directory with "documentary" folder')
        return

    if not path.exists(method_path):
        print('File "{}" is missing in documentary folder'.format(path.normpath(args.template)))
        return

    if not path.exists(template_path):
        print('Tried to documentation file "{}", but it doesn\'t exist'.format(template_path))
        return

    document(template_path, method_path)


if __name__ == '__main__':
    main()
