import re


def populate(content: str, replacement: callable) -> str:
    def repl(match):
        if '//' in match[1]:
            return match[0]
        if match['method']:
            return replacement(match['method'], len(match[1]))
        return match[0]

    return sub(content, repl)


def sub(string: str, repl: callable) -> str:
    pattern = r"^([^#\n]+)(?<!/)/\*\*[\s*]*{@documentary:(?P<method>\w+)}.*?\*/"
    return re.sub(pattern, repl, string, flags=re.MULTILINE | re.DOTALL)
