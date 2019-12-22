from .code_parts import replace_code_parts


def print_method(details: dict,
                 format_method: callable,
                 param_mapper: callable,
                 include_template_tag: bool,
                 indent: int) -> str:
    return replace_code_parts(__format_comment([
        *(['{@template:%s}' % details['name'], ''] if include_template_tag else []),
        __norm(details['definition']),
        *__suffix_new_line(_flat_map_new_lines(_format_params(details['param'], param_mapper))),
        *__suffix_new_line(_format_return(details['return'], details['return-type'])),
        *__suffix_new_line([*_format_throws()] if details.get('throws', True) else []),
        *__suffix_new_line(['@see ' + format_method(see) for see in details['see']]),
        *__suffix_new_line(['@link ' + format_method(see) for see in details['link']]),
    ], indent), lambda x: x in details['param'].keys())


def _flat_map_new_lines(strings) -> list:
    return [y for x in strings for y in x]


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
    raise Exception("Invalid param type")


def __suffix_new_line(parameters_: list) -> list:
    if len(parameters_) == 0:
        return []
    parameters_.insert(0, "")
    return parameters_


def _format_return(values, types):
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
    if type(return_value) is dict:
        if len(return_value) == 2:
            return [
                "returns " + ", ".join('<b>%s</b> %s' % (t, x['when']) for t, x in return_value.items()),
                "<ul>",
                *(' <li>%s %s</li>' % (x['return'], x['when']) for x in return_value.values()),
                "</ul>"
            ]
        raise Exception("Can't print multiple return types greater than 2")
    if type(return_value) is str:
        return [return_value]
    raise Exception("invalid type %s" % type(return_value))


def __valid_return(values, types):
    if type(values) is dict:
        if type(types) is list:
            return [*values.keys()] == types
    return type(values) is str and type(types) is str


def _format_throws() -> list:
    return [
        '@throws MalformedPatternException',
        '@throws RuntimeSafeRegexException',
        '@throws SuspectedReturnSafeRegexException',
        '@throws CompileSafeRegexException',
    ]


def __norm(text: str) -> str:
    return __with_suffix(text.strip(), ".")


def format_preg_method(name: str) -> str:
    return __with_suffix("preg::" + name, "()")


def __with_suffix(text: str, suffix: str) -> str:
    return text if text.endswith(suffix) else text + suffix


def __format_comment(lines: list, indent) -> str:
    pad = indent * ' '
    return pad + ("\n" + pad).join(["/**", *((" * " + line).rstrip(' ') for line in lines), " */"])
