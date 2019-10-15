import re

from details import load_details
from files import map_file
from format import print_method, format_preg_method


def document_file(template: str,
                  output: str,
                  declaration: str,
                  decorations: str,
                  definitions: str,
                  include_template_tag: bool) -> None:
    printer = Printer(load_details(declaration, decorations, definitions))
    map_file(template,
             output,
             lambda content: put_into_template(content, lambda m, i: printer.print(m, include_template_tag, i)))


class Printer:
    def __init__(self, methods):
        self.method_details = methods

    def print(self, method_name: str, template_tag: bool, indent: int):
        return print_method(
            self.method_details[method_name],
            lambda x: format_preg_method(x) if x in self.method_details else x,
            template_tag,
            indent)


def put_into_template(content: str, map_template: callable) -> str:
    def repl(match):
        if match['method']:
            return map_template(match['method'], len(match[1]))
        return match[0]

    return re.sub(r"^([^#\n]+)(?<!/)/\*\*[\s*]*{@template:(?P<method>\w+)}.*?\*/",
                  repl,
                  content,
                  flags=re.MULTILINE | re.DOTALL)
