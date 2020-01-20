from .details.preprocess_details import load_details
from .files import map_file
from .placeholder import populate
from .template import render_template


def document_file(documentary: str,
                  template: str,
                  output: str,
                  declaration: str,
                  decorations: str,
                  definitions: str,
                  fragments: str,
                  include_template_tag: bool) -> bool:
    details = load_details(declaration, decorations, definitions)

    def repl(method_name: str, indent: int) -> str:
        return render_template(details, method_name, indent, documentary, fragments, include_template_tag)

    def mapper(content: str) -> str:
        return populate(content, repl)

    return map_file(template, output, mapper)
