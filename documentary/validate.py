import re

from schema import Schema, Or, Optional, And, Use


def definitions(detail: dict) -> dict:
    return definitions_schema().validate(detail)


def declarations(detail: dict) -> dict:
    return declarations_schema().validate(detail)


def decorations(detail: dict) -> dict:
    return decorations_schema().validate(detail)


def definitions_schema() -> Schema:
    return Schema(Or({}, {
        str: {
            Optional("inherit"): str,
            Optional("definition"): str,
            Optional("return"): Or(str, {}, {
                str: {
                    "when": str,
                    "return": str
                },
            }),
            Optional("const"): Or({}, {str: str})
        },
    }))


def _valid_param_array_declaration(declaration: list) -> bool:
    decl = list(declaration)
    if 'optional' in decl:
        decl.remove('optional')
    if '&ref' in decl:
        decl.remove('&ref')
    if len(decl) and all(_valid_param_type(_type) for _type in decl):
        return True
    raise TypeError()


def declarations_schema() -> Schema:
    return Schema(Or({}, {
        str: {
            Optional("inherit"): str,
            Optional("param"): Or(
                {},
                {
                    str: Or(
                        str,
                        And(list, Use(_valid_param_array_declaration)),
                        {},
                        {
                            'bit-sum': And(len, [And(str, __valid_flag)])
                        },
                        {
                            'type': Or(
                                _valid_param_type,
                                {
                                    'type': 'array',
                                    'keys': And(str, _valid_param_type),
                                    'values': And(str, _valid_param_type),
                                }
                            ),
                            Optional('optional'): bool,
                            Optional('ref'): bool
                        }
                    )
                },
            ),
            Optional("template"): {str: Or(_valid_param_type, [_valid_param_type])},
            Optional("return-type"): Or(str, [str])
        },
    }))


def _valid_param_type(_type: str) -> bool:
    return bool(re.match(r"^(int|string|bool(ean)?|array|callable)(\[\])?$", _type))


def __valid_flag(flag: str) -> bool:
    return bool(re.match(r"^([A-Z][A-Z0-9]+)(_[A-Z0-9]+)*$", flag))


def decorations_schema() -> Schema:
    return Schema(Or({}, {
        Optional("methods"): Or({}, {
            str: Or({}, {
                Optional("see"): [str],
                Optional("link"): [str],
                Optional("manual"): Or({}, {str: Or(str, None)}),
                Optional("throws"): [str]
            }),
        }),
        Optional("groups"): Or({}, {
            Optional("see"): [
                And([str], lambda x: len(x) > 1)
            ],
            Optional("throws"): [
                {
                    "methods": [str],
                    "exceptions": [str]
                }
            ]
        }),
        Optional("*"): Or({}, {
            Optional("see"): [str],
            Optional("link"): [str],
            Optional("throws"): [str]
        })
    }))
