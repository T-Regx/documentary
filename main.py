from args import parse_args
from template import document_file


def document(filename: str):
    document_file(
        template=filename,
        output=filename,
        declaration='resources/src/preg.declaration.json',
        decorations='resources/src/preg.decorations.json',
        definitions='resources/src/preg.definitions.json',
        fragments='resources/src/fragments/',
        include_template_tag=True,
    )
    print("Documented file {}".format(filename))


if __name__ == '__main__':
    args = parse_args()

    document(args.template)
