import json

from merge_utils import __merge_dictionaries
from utils import first


def load_details(declaration: str, decorations: str, definitions: str) -> dict:
    with open(declaration) as declaration_file:
        with open(decorations) as decorations_file:
            with open(definitions) as definitions_file:
                params = __polyfill_params(__inherit(json.load(declaration_file)))
                links = __decorations_move_manual_to_link(__decorations_process_groups(json.load(decorations_file)))
                summaries = __inherit(json.load(definitions_file))
                return __merge_dictionaries([params, links, summaries], False)


def __polyfill_params(declaration: dict) -> dict:
    for method in declaration.values():
        if "param" not in method:
            method['param'] = {}
    return declaration


def __decorations_move_manual_to_link(declaration: dict) -> dict:
    for method in declaration.values():
        if "manual" in method:
            if method['manual']['php']:
                method['link'].append(method['manual']['php'])
            if method['manual']['t-regx']:
                method['link'].append(method['manual']['t-regx'])
            del method['manual']
        method['see'].append('pattern()')
        method['see'].append('Pattern::of()')
    return declaration


def __inherit(declarations: dict) -> dict:
    for method, declaration in declarations.items():
        if "inherit" in declaration:
            inherit_from = declaration["inherit"]
            if "inherit" in declarations[inherit_from]:
                raise Exception("recursive inheritance not implemented")
            declarations[method] = declarations[inherit_from].copy()
    return declarations


def __decorations_process_groups(decorations: dict) -> dict:
    return __process_groups(decorations['methods'].copy(), decorations['groups'])


def __process_groups(methods: dict, groups: list) -> dict:
    for group in groups:
        invalid_method = first(group, lambda x: x not in methods)
        if invalid_method:
            raise Exception("Invalid method '%s'" % invalid_method)
        for method, decoration in methods.items():
            if method in group:
                decoration['see'].extend([x for x in group if x != method])
    return methods
