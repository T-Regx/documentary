from .markup import replace_template_strings
from .utils import interlace


def print_method(details: dict,
                 format_method: callable,
                 param_mapper: callable,
                 definition_fallback: callable,
                 include_template_tag: bool,
                 indent: int) -> str:
    sections = render_comment_as_parts(details, format_method, include_template_tag, param_mapper, definition_fallback)

    return replace_template_strings(
        string=__comment_as_lines(__join_sections(sections), indent),
        tag=lambda x: 'i' if x in details['param'] else 'b')


def render_comment_as_parts(details: dict,
                            format_method: callable,
                            include_template_tag: bool,
                            param_mapper: callable,
                            definition_fallback: callable) -> list:
    return [
        ['{{@documentary:{}}}'.format(details['name'])] if include_template_tag else [],
        [__norm(details['definition'])] if details['definition'] is not None else definition_fallback().splitlines(),
        [line for lines in _format_params(details['param'], param_mapper) for line in lines],
        _format_return(details['return'], details['return-type']),
        _format_throws(details['throws']),
        ['@see ' + format_method(see) for see in details['see']],
        ['@link ' + link for link in details['link']],
    ]


def __join_sections(parts: list) -> list:
    return [line for lines in interlace([part for part in parts if any(part)], ['']) for line in lines]


def _format_params(params: dict, param_summary: callable):
    return [_format_param(name, d, param_summary) for name, d in params.items()]


def _format_param(name: str, param, param_summary: callable):
    summary_lines = param_summary(name).splitlines()
    signature = __format_param_signature(name, param)
    if len(summary_lines) == 0:
        return [signature]
    summary_lines[0] = signature + ' ' + summary_lines[0]
    return summary_lines


def __format_param_signature(name, d):
    param_type = __join_array(d['type'])
    is_ref = d.get('ref', False)
    ref = "&" if is_ref else ""
    modifiers = ''
    if is_ref and d.get('optional', False):
        modifiers = ' [optional, reference]'
    elif is_ref:
        modifiers = ' [reference]'
    elif d.get('optional', False):
        modifiers = ' [optional]'
    return "@param " + param_type + ' ' + ref + '$' + name + modifiers


def __join_array(param) -> str:
    if type(param) is str:
        return param
    if type(param) is list:
        return "|".join(param)
    if isinstance(param, dict):
        return param['values'] + '[]'
    raise Exception("Invalid param type")


def _format_return(values, types):
    if values is None and types is None:
        return []
    if not __valid_return(values, types):
        raise Exception("Mismatched declaration and definition return types")
    v = __format_return_value(values)
    return [
        '@return ' + __format_return_type(types) + ' ' + v.pop(0),
        *v
    ]


def __format_return_type(return_type) -> str:
    if type(return_type) is list:
        return "|".join(return_type)
    if type(return_type) is str:
        return return_type
    raise Exception("invalid type %s" % type(return_type))


def __format_return_value(return_value) -> list:
    if isinstance(return_value, dict):
        if len(return_value) == 2:
            return [
                "returns " + ", ".join(f'<b>{t}</b> {x["when"]}' for t, x in return_value.items()),
                "<ul>",
                *(' <li>%s %s</li>' % (x['return'], x['when']) for x in return_value.values()),
                "</ul>"
            ]
        raise Exception("Can't print multiple return types greater than 2")
    if type(return_value) is str:
        return [return_value]
    raise Exception(f"invalid type {type(return_value)}")


def __valid_return(values, types):
    if isinstance(values, dict):
        if type(types) is list:
            return [*values.keys()] == types
    return type(values) is str and type(types) is str


def _format_throws(exceptions: list) -> list:
    return [f'@throws {exception}' for exception in exceptions]


def __norm(text: str) -> str:
    if len(text.strip()):
        return __with_suffix(text.strip(), ".")
    return ""


def format_preg_method(name: str) -> str:
    return __with_suffix("preg::" + name, "()")


def __with_suffix(text: str, suffix: str) -> str:
    return text if text.endswith(suffix) else text + suffix


def __comment_as_lines(lines: list, indent) -> str:
    return "\n".join(__indented_comment(lines, indent))


def __indented_comment(lines: list, indent: int) -> list:
    return [indent * ' ' + line for line in __unindented_comment(lines)]


def __unindented_comment(lines: list) -> list:
    return [
        "/**",
        *((" * " + line).rstrip(' ') for line in lines),
        " */"
    ]
