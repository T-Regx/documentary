import template


def main() -> None:
    output = 'resources/output/result.php'

    template.document_file(
        template='resources/src/preg.template',
        declaration='resources/src/preg.declaration.json',
        decorations='resources/src/preg.decorations.json',
        definitions='resources/src/preg.definitions.json',
        output=output,
    )

    print("Documented file {}".format(output))


if __name__ == '__main__':
    main()
