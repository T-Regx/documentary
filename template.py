import re

from details import load_details
from files import map_file
from format import print_method, format_preg_method


def document_file(template: str, output: str, declaration: str, decorations: str, definitions: str) -> None:
    printer = Printer(load_details(declaration, decorations, definitions))
    map_file(template, output, lambda content: put_into_template(content, lambda m, i: printer.print(m, i)))


class Printer:
    def __init__(self, methods):
        self.method_details = methods

    def print(self, method_name: str, indent: int):
        return print_method(
            self.method_details[method_name],
            lambda x: format_preg_method(x) if x in self.method_details else x,
            indent)


def put_into_template(content: str, map_template: callable) -> str:
    def repl(match):
        return map_template(match['method'], len(match[1]))

    return re.sub(r"^([^#\n\r]*?)(?<=[^/])/\*\*.*?(?:{@template:(?P<method>\w+)}).*?\*/",
                  repl,
                  content,
                  flags=re.MULTILINE | re.DOTALL)
