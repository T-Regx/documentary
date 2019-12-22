from os import path, getcwd

from documentary.args import parse_args
from documentary.template import document_file


def document(template_path: str, documentary_path: str) -> None:
    d, basename = path.split(template_path)

    document_file(
        template=template_path,
        output=template_path,
        declaration=path.join(documentary_path, basename + '.documentation', 'declaration.json'),
        decorations=path.join(documentary_path, basename + '.documentation', 'decorations.json'),
        definitions=path.join(documentary_path, basename + '.documentation', 'definitions.json'),
        fragments=(path.join(documentary_path, basename + '.documentation', 'fragments')),
        include_template_tag=True,
    )
    print("Documented file {}".format(template_path))


def main():
    args = parse_args()

    documentary_path = path.join(getcwd(), 'documentary')
    template_path = path.join(getcwd(), args.template)

    if not path.exists(documentary_path):
        print('To generate a documentation, navigate to a directory with "documentary" folder')
        return

    if not path.exists(template_path):
        print("Tried to documentation file {}, but it doesn't exist".format(template_path))
        return

    document(template_path, documentary_path)


if __name__ == '__main__':
    main()
