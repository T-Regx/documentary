import os
from typing import Union

from .files import fragment_fallback, fragment
from .format_comment import format_comment, format_preg_method, format_sections_comment
from .placeholder import populate


def bootstrap(details: dict, class_details: dict, documentary: str, fragments: str, include_template_tag: bool) -> callable:
    def repl(method_name: str, indent: int, placeholder: str):
        if method_name == ':class':
            return class_comment(class_details, placeholder, indent, documentary)
        if method_name not in details:
            return None
        return details_as_comment(details, method_name, indent, documentary, fragments, placeholder if include_template_tag else None)

    return lambda template: populate(template, repl)


def class_comment(class_details: dict, placeholder: str, indent: int, documentary: str) -> str:
    snippet_path = os.path.join(documentary, 'project', 'snippet')
    snippets = [load_snippet(snippet_path, snippet) for snippet in class_details['snippets']]
    return format_sections_comment([[placeholder], *snippets], indent=indent)


def load_snippet(snippet_folder: str, snippet_name: str) -> list:
    with open(os.path.join(snippet_folder, snippet_name + '.html')) as file:
        return file.read().strip().split("\n")


def details_as_comment(details: dict, method_name: str, indent: int, documentary: str, fragments: str, include_template_tag: Union[str, None]) -> str:
    return format_comment(
        details=details[method_name],
        format_method=lambda x: format_preg_method(x) if x in details else x,
        param_mapper=lambda p: fragment_fallback(fragments, f"{method_name}.param.{p}", f'param.{p}', documentary),
        definition_fallback=lambda: fragment(fragments, f'method.{method_name}', default=lambda: ''),
        template_tag=include_template_tag,
        indent=indent)
