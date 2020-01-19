from .details.preprocess_details import load_details
from .files import map_file
from .placeholder import populate
from .template import render_template


def document_file(documentary: str,
                  filename: str,
                  output: str,
                  definitions: str,
                  declaration: str,
                  decorations: str,
                  fragments: str,
                  include_template_tag: bool) -> bool:
    details = load_details(definitions, declaration, decorations)

    def repl(method_name: str, indent: int) -> str:
        return render_template(details, method_name, indent, documentary, fragments, include_template_tag)

    def mapper(content: str) -> str:
        return populate(content, repl)

    return map_file(filename, output, mapper)
