from os import path

from args import parse_args
from template import document_file


def document(filename: str) -> None:
    d, basename = path.split(filename)

    document_file(
        template=filename,
        output=filename,
        declaration=path.join(d, basename + '.declaration.json'),
        decorations=path.join(d, basename + '.decorations.json'),
        definitions=path.join(d, basename + '.definitions.json'),
        fragments=(path.join(d, 'fragments')),
        include_template_tag=True,
    )
    print("Documented file {}".format(filename))


if __name__ == '__main__':
    args = parse_args()

    document(args.template)