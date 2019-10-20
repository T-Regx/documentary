import json
import re

from src.merge_utils import merge_dictionaries
from src.utils import first


def load_details(declaration: str, decorations: str, definitions: str) -> dict:
    with open(definitions) as definitions_file:
        with open(declaration) as declaration_file:
            with open(decorations) as decorations_file:
                return build_details(
                    json.load(definitions_file),
                    json.load(declaration_file),
                    json.load(decorations_file))


def build_details(summaries: dict = None, params: dict = None, links: dict = None) -> dict:
    summaries = __populate_consts(__put_name(__inherit(summaries if summaries else {})))
    params = __polyfill_params(__unravel_params(__inherit(params if params else {})))
    links = __decorations_move_manual_to_link(
        __decorations_process_groups(__decorations_append_global_decorations(links if links else {})))

    return merge_dictionaries([params, links, summaries], False)


def __polyfill_params(declaration: dict) -> dict:
    for method in declaration.values():
        if "param" not in method:
            method['param'] = {}
    return declaration


def __decorations_append_global_decorations(decoration: dict) -> dict:
    if '*' in decoration:
        asterisk = decoration['*']
        for method in decoration['methods'].values():
            method['see'].extend(asterisk['see'])
            method['link'].extend(asterisk['link'])

    return decoration


def __decorations_move_manual_to_link(declaration: dict) -> dict:
    for method in declaration.values():
        if "manual" in method:
            if method['manual']['php']:
                method['link'].append(method['manual']['php'])
            if method['manual']['t-regx']:
                method['link'].append(method['manual']['t-regx'])
            del method['manual']
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
    return __process_groups(decorations.get('methods', {}).copy(), decorations.get('groups', {}))


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
        return __unravel_param_dict(name, param)
    if type(param) is str:
        return __param(_type=param)
    if type(param) is list:
        return __unravel_param_list(name, param)
    raise ParameterTypeException("unexpected param type %s" % type(name))


def __unravel_param_dict(name: str, param):
    if 'flags' in param and param['flags'] is not None:
        if 'type' in param and param['type'] is not 'int':
            raise ParameterTypeException("Possibly conflicted 'flags' declaration in parameter '%s'" % name)
        if any(item for item in param['flags'] if not __is_valid_flag(item)):
            raise ParameterTypeException('Malformed flag')
        return __param('int', optional=True, ref=True, flags=param['flags'])
    if 'type' not in param:
        raise ParameterTypeException('No type parameter')
    if not __is_valid_type(param['type']):
        raise ParameterTypeException('Invalid parameter type value: %s' % param['type'])
    return __param(_type=param['type'],
                   optional=param.get('optional', False),
                   ref=param.get('ref', False),
                   flags=param.get('flags', None))


def __unravel_param_list(name: str, param: list) -> dict:
    d = {"optional": False, "ref": False, "flags": None}
    if "optional" in param:
        d['optional'] = True
        param.remove('optional')
    if "&ref" in param:
        d['ref'] = True
        param.remove('&ref')
    if name == 'flags' and not _any_types(param):
        if len(param) == 0:
            raise ParameterTypeException("Parameter 'flags' is empty")
        d['type'] = 'int'
        d['optional'] = True
        d['flags'] = param
        return d
    if len(param) == 0:
        raise ParameterTypeException('No type parameter')
    if _only_types(param):
        d['type'] = param[0] if len(param) == 1 else param
        return d
    raise ParameterTypeException("unexpected param type %s: %s" % (name, json.dumps(param)))


def __param(_type: str, optional: bool = False, ref: bool = False, flags: list = None):
    return {'type': _type, 'optional': optional, 'ref': ref, 'flags': flags}


def _only_types(param: list) -> bool:
    return not any(item for item in param if not __is_valid_type(item))


def _any_types(param: list) -> bool:
    return any(item for item in param if __is_valid_type(item))


def __is_valid_type(param_type: str) -> bool:
    return param_type in ['string', 'string[]', 'int', 'array', 'array[]']


def __is_valid_flag(flag: str) -> bool:
    return bool(re.match(r"^[A-Z]+(_[A-Z]+){0,4}$", flag))


class ParameterTypeException(Exception):
    pass
