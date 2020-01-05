from schema import Schema, Or, Optional, And


def definitions(detail: dict) -> dict:
    return definitions_schema().validate(detail)


def declarations(detail: dict) -> dict:
    return declarations_schema().validate(detail)


def decorations(detail: dict) -> dict:
    return decorations_schema().validate(detail)


def definitions_schema() -> Schema:
    return Schema(Or({}, {
        str: {
            Optional("definition"): str,
            Optional("return"): str
        },
    }))


def declarations_schema() -> Schema:
    return Schema(Or({}, {
        str: {
            Optional("param"): Or({}, {
                str: Or(str, list),
            }),
            Optional("return-type"): str
        },
    }))


def decorations_schema() -> Schema:
    return Schema(Or({}, {
        Optional("methods"): Or({}, {
            str: Or({}, {
                Optional("see"): [str],
                Optional("link"): [str],
                Optional("manual"): Or({}, {str: str}),
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
