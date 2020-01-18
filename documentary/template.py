import re

from documentary.details.preprocess_details import load_details
from documentary.files import map_file, fragment_fallback, fragment
from documentary.format_comment import print_method, format_preg_method


def document_file(documentary: str,
                  template: str,
                  output: str,
                  declaration: str,
                  decorations: str,
                  definitions: str,
                  fragments: str,
                  include_template_tag: bool) -> bool:
    printer = Printer(
        load_details(declaration, decorations, definitions),
        lambda method, param: fragment_fallback(fragments, method + '.param.' + param, 'param.' + param, documentary),
        lambda method: fragment(fragments, 'method.' + method),
        include_template_tag
    )
    return map_file(
        template,
        output,
        mapper=lambda content: populate_template_placeholder(content, map_template=printer.print))


class Printer:
    def __init__(self, method_details: dict, param_mapper: callable, method_mapper: callable, template_tag: bool):
        self.method_details = method_details
        self.param_mapper = param_mapper
        self.method_mapper = method_mapper
        self.template_tag = template_tag

    def print(self, method_name: str, indent: int):
        return print_method(
            self.method_details[method_name],
            lambda x: format_preg_method(x) if x in self.method_details else x,
            lambda param: self.param_mapper(method_name, param),
            lambda: self.method_mapper(method_name),
            self.template_tag,
            indent)


def populate_template_placeholder(content: str, map_template: callable) -> str:
    def repl(match):
        if match['method']:
            return map_template(match['method'], len(match[1]))
        return match[0]

    return re.sub(r"^([^#\n]+)(?<!/)/\*\*[\s*]*{@documentary:(?P<method>\w+)}.*?\*/",
                  repl,
                  content,
                  flags=re.MULTILINE | re.DOTALL)
