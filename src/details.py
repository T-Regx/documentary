import json
import re

from src.merge_utils import __merge_dictionaries
from src.utils import first


def load_details(declaration: str, decorations: str, definitions: str) -> dict:
    with open(declaration) as declaration_file:
        with open(decorations) as decorations_file:
            with open(definitions) as definitions_file:
                params = __polyfill_params(__unravel_params(__inherit(json.load(declaration_file))))
                links = __decorations_move_manual_to_link(__decorations_process_groups(json.load(decorations_file)))
                summaries = __populate_consts(__put_name(__inherit(json.load(definitions_file))))
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


def __put_name(methods: dict) -> dict:
    for name, detail in methods.items():
        detail['name'] = name
    return methods


def __unravel_params(methods: dict) -> dict:
    for method in methods.values():
        if 'param' in method:
            for name, param in method['param'].items():
                method['param'][name] = __unravel_param(name, param)
    return methods


def __populate_consts(methods: dict) -> dict:
    for method in methods.values():
        if 'const' in method:
            if 'return' not in method or type(method['return']) is not dict:
                raise Exception("Invalid usage of key 'const'")
            for case in method['return'].values():
                case['return'] = re.sub(':([a-z]+)', lambda match: method['const'][match[1]], case['return'])
    return methods


def __unravel_param(name: str, param) -> dict:
    if type(param) is dict:
        return {"type": param['type'],
                "optional": param.get('optional', False),
                "ref": param.get('ref', False),
                "flags": param.get('flags', [])}
    if type(param) is str:
        return {"type": param,
                "optional": False,
                "ref": False,
                "flags": []}
    if type(param) is list:
        d = {"optional": False, "ref": False, "flags": []}
        if "optional" in param:
            d['optional'] = True
            param.remove('optional')
        if "&ref" in param:
            d['ref'] = True
            param.remove('&ref')
        if name == 'flags' and not _any_types(param):
            d['type'] = 'int'
            d['optional'] = True
            d['flags'] = param
            return d
        if len(param) == 1:
            d['type'] = param[0]
            return d
        if _only_types(param):
            d['type'] = param
            return d
    raise Exception("unexpected param type %s: %s" % (name, json.dumps(param)))


def _only_types(param: dict) -> bool:
    valid_types = ['string', 'string[]', 'int', 'array[]']
    return not any(item for item in param if item not in valid_types)


def _any_types(param: dict) -> bool:
    valid_types = ['string', 'string[]', 'int', 'array[]']
    return any(item for item in param if item in valid_types)
