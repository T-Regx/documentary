from .files import fragment_fallback, fragment
from .format_comment import format_comment, format_preg_method
from .placeholder import populate


def bootstrap(details: dict, documentary: str, fragments: str, include_template_tag: bool) -> callable:
    def repl(method_name: str, indent: int, placeholder: str):
        if method_name not in details:
            return None
        return details_as_comment(details, method_name, indent, documentary, fragments, include_template_tag)

    return lambda template: populate(template, repl)


def details_as_comment(details: dict, method_name: str, indent: int, documentary: str, fragments: str, include_template_tag: bool) -> str:
    return format_comment(
        details=details[method_name],
        format_method=lambda x: format_preg_method(x) if x in details else x,
        param_mapper=lambda p: fragment_fallback(fragments, f"{method_name}.param.{p}", f'param.{p}', documentary),
        definition_fallback=lambda: fragment(fragments, f'method.{method_name}', default=lambda: ''),
        include_template_tag=include_template_tag,
        indent=indent)
