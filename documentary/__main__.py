from documentary.args import parse_args
from documentary.document import document_many
from documentary.paths import resolve_paths


def main():
    documentary_path, root_path, template, output_path = resolve_paths(parse_args())
    document_many(documentary_path, root_path, template, output_path)


if __name__ == '__main__':
    main()
