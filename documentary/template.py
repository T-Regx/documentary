from .files import fragment_fallback, fragment
from .format_comment import print_method, format_preg_method


def render_template(details: dict, method_name: str, indent: int, documentary: str, fragments: str,
                    include_template_tag: bool) -> str:
    return print_method(
        details=details[method_name],
        format_method=lambda x: format_preg_method(x) if x in details else x,
        param_mapper=lambda p: fragment_fallback(fragments, f"{method_name}.param.{p}", f'param.{p}', documentary),
        definition_fallback=lambda: fragment(fragments, f'method.{method_name}', default=lambda: ''),
        include_template_tag=include_template_tag,
        indent=indent)
