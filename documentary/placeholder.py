import re


def populate(template: str, replacement: callable) -> str:
    def repl(match):
        if '//' in match[1]:
            return match[0]
        if match['method']:
            replace = replacement(match['method'], len(match[1]), match['placeholder'])
            if type(replace) is str:
                return replace
            if replace is not None:
                raise TypeError('Invalid replacement type')
        return match[0]

    return sub(template, repl)


def sub(string: str, repl: callable) -> str:
    pattern = r"^([^#\n]+)(?<!/)/\*\*[\s*]*(?P<placeholder>{documentary:(?P<method>\w+)}).*?\*/"
    return re.sub(pattern, repl, string, flags=re.MULTILINE | re.DOTALL)
