from .details.preprocess_details import load_details
from .files import map_file
from .template import bootstrap


def document_file(documentary: str,
                  filename: str,
                  output: str,
                  definitions: str,
                  declaration: str,
                  decorations: str,
                  fragments: str,
                  include_template_tag: bool) -> bool:
    details = load_details(definitions, declaration, decorations)
    return map_file(filename, output, bootstrap(details, documentary, fragments, include_template_tag))
