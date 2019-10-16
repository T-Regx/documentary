import re


def replace_code_parts(string: str, is_param: callable):
    def repl(match) -> str:
        value = match[1]
        tag = 'i' if is_param(value) else 'b'
        return "<%s>%s</%s>" % (tag, value, tag)

    return re.sub(r"`([^`\s]{1,25})`", repl, string)
