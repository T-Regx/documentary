from .details.preprocess_details import load_details
from .files import map_file, fragment_fallback, fragment
from .format_comment import print_method, format_preg_method
from .placeholder import populate


def document_file(documentary: str,
                  template: str,
                  output: str,
                  declaration: str,
                  decorations: str,
                  definitions: str,
                  fragments: str,
                  include_template_tag: bool) -> bool:
    details = load_details(declaration, decorations, definitions)

    def _render_comment(method_name: str, indent: int):
        return print_method(
            details=details[method_name],
            format_method=lambda x: format_preg_method(x) if x in details else x,
            param_mapper=lambda p: fragment_fallback(fragments, f"{method_name}.param.{p}", f'param.{p}', documentary),
            definition_fallback=lambda: fragment(fragments, f'method.{method_name}'),
            include_template_tag=include_template_tag,
            indent=indent)

    return map_file(
        template,
        output,
        mapper=lambda content: populate(content, replacement=_render_comment))
