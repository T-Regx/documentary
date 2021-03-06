import re


def replace_template_strings(string: str, tag: callable) -> str:
    def repl(match) -> str:
        return markup(tag(match[1]), match[1])

    return re.sub(r"`([^`\n\r]+)`", repl, string)


def markup(tag: str, value: str) -> str:
    return f"<{tag}>{value}</{tag}>"
