import template


def main() -> None:
    filename = 'resources/src/preg.php'

    template.document_file(
        template=filename,
        output=filename,
        declaration='resources/src/preg.declaration.json',
        decorations='resources/src/preg.decorations.json',
        definitions='resources/src/preg.definitions.json',
        include_template_tag=True
    )

    print("Documented file {}".format(filename))


if __name__ == '__main__':
    main()
