import re

from documentary.details import load_details
from documentary.files import map_file, fragment_fallback, fragment
from documentary.format import print_method, format_preg_method


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
    )
    return map_file(template,
                    output,
                    lambda content: put_into_template(content, lambda m, i: printer.print(m, include_template_tag, i)))


class Printer:
    def __init__(self, methods, param_mapper: callable, method_mapper: callable):
        self.method_details = methods
        self.param_mapper = param_mapper
        self.method_mapper = method_mapper

    def print(self, method_name: str, template_tag: bool, indent: int):
        return print_method(
            self.method_details[method_name],
            lambda x: format_preg_method(x) if x in self.method_details else x,
            lambda param: self.param_mapper(method_name, param),
            lambda: self.method_mapper(method_name),
            template_tag,
            indent)


def put_into_template(content: str, map_template: callable) -> str:
    def repl(match):
        if match['method']:
            return map_template(match['method'], len(match[1]))
        return match[0]

    return re.sub(r"^([^#\n]+)(?<!/)/\*\*[\s*]*{@documentary:(?P<method>\w+)}.*?\*/",
                  repl,
                  content,
                  flags=re.MULTILINE | re.DOTALL)
