from os import path

from .details.preprocess_details import load_details
from .files import map_file
from .folder import discover_templates
from .template import bootstrap


def document_many(documentary_path: str, root_path: str, templates_path: str, output_path: str) -> None:
    for template in discover_templates(templates_path, root_path, documentary_path):
        document(documentary_path,
                 path.join(documentary_path, template),
                 path.join(root_path, template),
                 path.join(output_path, template))


def document(documentary_path: str, documentation_path: str, template_path: str, output_path: str) -> None:
    details, class_details = load_details(
        path.join(documentation_path, 'definition.json'),
        path.join(documentation_path, 'declaration.json'),
        path.join(documentation_path, 'decoration.json'))

    documented = map_file(template_path, output_path, bootstrap(details, class_details, documentary_path, path.join(documentation_path, 'fragments'), True))

    print(('Documented file "{}"' if documented else 'File "{}" remains unchanged').format(template_path))
