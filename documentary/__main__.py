from os import path, getcwd

from documentary.args import parse_args
from documentary.document import document_file


def document(documentary_path: str, template_path: str, class_path: str) -> None:
    documented = document_file(
        documentary=documentary_path,
        template=template_path,
        output=template_path,
        definitions=path.join(class_path, 'definitions.json'),
        declaration=path.join(class_path, 'declaration.json'),
        decorations=path.join(class_path, 'decorations.json'),
        fragments=(path.join(class_path, 'fragments')),
        include_template_tag=True,
    )
    print(('Documented file "{}"' if documented else 'File "{}" remains unchanged').format(template_path))


def main():
    args = parse_args()

    documentary_path = path.join(getcwd(), 'documentary')
    class_path = path.join(getcwd(), 'documentary', args.template)
    template_path = path.join(getcwd(), args.template)

    if not path.exists(documentary_path):
        print('To generate a documentation, navigate to a directory with "documentary" folder')
        return

    if not path.exists(class_path):
        print('Directory "{}" is missing in documentary folder'.format(path.normpath(args.template)))
        return

    if not path.exists(template_path):
        print('Tried to documentation file "{}", but it doesn\'t exist'.format(template_path))
        return

    document(documentary_path, template_path, class_path)


if __name__ == '__main__':
    main()
