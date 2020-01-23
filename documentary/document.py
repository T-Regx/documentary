from os import path

from .details.preprocess_details import load_details
from .files import map_file
from .template import bootstrap


def document(documentary_path: str, documentation_path: str, template_path: str, output_path: str) -> None:
    details = load_details(
        path.join(documentation_path, 'definition.json'),
        path.join(documentation_path, 'declaration.json'),
        path.join(documentation_path, 'decoration.json'))

    documented = map_file(template_path, output_path, bootstrap(details, documentary_path, path.join(documentation_path, 'fragments'), True))

    print(('Documented file "{}"' if documented else 'File "{}" remains unchanged').format(template_path))
