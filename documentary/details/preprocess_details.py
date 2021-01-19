import json
import re
from collections import OrderedDict
from typing import Tuple

from documentary import validate
from documentary.merge_utils import merge_dictionaries
from documentary.utils import first


def load_details(definitions: str, declaration: str, decorations: str) -> Tuple[dict, dict]:
    decoration = _load_file_or_default(decorations)
    details = build_details(_load_file_or_default(definitions), _load_file_or_default(declaration), decoration)
    return details, decoration.get('class', {}) if decoration else {}


def _load_file_or_default(filename: str, default=None) -> dict:
    try:
        with open(filename) as file:
            return json.load(file, object_pairs_hook=lambda pair: OrderedDict(pair))
    except FileNotFoundError:
        return default


def build_details(summaries: dict = None, params: dict = None, links: dict = None) -> dict:
    validate.definitions(summaries) if summaries else {}
    validate.declarations(params) if params else {}
    validate.decorations(links) if links else {}

    dictionaries = merge_dictionaries(
        [build_params(params or {}), build_links(links or {}), build_summaries(summaries or {})], allow_override=False)
    return polyfill_methods(dictionaries)


def polyfill_methods(details: dict) -> dict:
    for method, detail in details.items():
        details[method] = {
            "definition": detail.get('definition', None),
            "param": detail.get('param', {}),
            "return": detail.get('return', None),
            "return-type": detail.get('return-type', None),
            'template': detail.get('template', {}),
            "throws": detail.get('throws', []),
            "see": detail.get('see', []),
            "link": detail.get('link', []),
        }
    return details


def build_summaries(summaries: dict) -> dict:
    return __populate_consts(__inherit(summaries))


def build_params(params: dict) -> dict:
    return __unravel_params(__inherit(params))


def build_links(links: dict) -> dict:
    link = __decorations_append_global_decorations(links)
    link = __decorations_process_see_groups(link)
    link = __decorations_process_throws_groups(link)
    return __decorations_move_manual_to_link(link['methods'])


def __decorations_append_global_decorations(decoration: dict) -> dict:
    if '*' in decoration:
        asterisk = decoration['*']
        for method in decoration['methods'].values():
            __put_or_extend(method, 'see', asterisk['see'])
            __put_or_extend(method, 'link', asterisk['link'])
            __put_or_extend(method, 'throws', asterisk['throws'])
    return decoration


def __put_or_extend(method: dict, key: hash, values: list) -> None:
    if key not in method:
        method[key] = []
    method[key].extend(values)


def __decorations_move_manual_to_link(declaration: dict) -> dict:
    for method in declaration.values():
        if "manual" in method:
            method['link'].extend(filter(None, method['manual'].values()))
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


def __decorations_process_see_groups(decorations: dict) -> dict:
    return {
        **decorations,
        'methods': __process_see_groups(
            decorations.get('methods', {}).copy(),
            decorations.get('groups', {}).get('see', []))
    }


def __decorations_process_throws_groups(decorations: dict) -> dict:
    return {
        **decorations,
        'methods': __process_throws_groups(
            decorations.get('methods', {}).copy(),
            decorations.get('groups', {}).get('throws', []))
    }


def __process_see_groups(methods: dict, groups: list) -> dict:
    for group in groups:
        invalid_method = first(group, lambda x: x not in methods)
        if invalid_method:
            raise Exception(f"Method '{invalid_method}' used in 'groups.see' is not declared")
        for method, decoration in methods.items():
            if method in group:
                decoration['see'].extend([x for x in group if x != method])
    return methods


def __process_throws_groups(methods: dict, groups: list) -> dict:
    for group in groups:
        invalid_method = first(group['methods'], lambda x: x not in methods)
        if invalid_method:
            raise Exception(f"Method '{invalid_method}' used in 'groups.throws' is not declared")
        for method in group['methods']:
            methods[method]['throws'].extend(group['exceptions'])
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
            if 'return' not in method or not isinstance(method['return'], dict):
                raise Exception("Invalid usage of key 'const'")
            for case in method['return'].values():
                case['return'] = re.sub(':([a-z]+)', lambda match: method['const'][match[1]], case['return'])
    return methods


def __unravel_param(name: str, param) -> dict:
    if isinstance(param, dict):
        return __unravel_param_dict(name, param)
    if type(param) is str:
        return __param(_type=param)
    if type(param) is list:
        return __unravel_param_list(name, param)
    raise ParameterTypeException(f"unexpected param type {type(name)}")


def __unravel_param_dict(name: str, param):
    # TODO: Refactor this or extract
    if 'bit-sum' in param and param['bit-sum'] is not None:
        if 'type' in param and param['type'] is not 'int':
            raise ParameterTypeException(f"Possibly conflicted 'flags' declaration in parameter '{name}'")
        if any(item for item in param['bit-sum'] if not __is_valid_flag(item)):
            raise ParameterTypeException('Malformed flag')
        return __param('int', optional=True, ref=False, flags=param['bit-sum'])
    if 'type' not in param:
        raise ParameterTypeException('No type parameter')
    if not __is_valid_type(param['type']):
        raise ParameterTypeException(f'Invalid parameter type value: {param["type"]}')
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
    if len(param) == 0:
        raise ParameterTypeException('No type parameter')
    if _only_types(param):
        d['type'] = param[0] if len(param) == 1 else param
        return d
    raise ParameterTypeException(f"unexpected param type {name}: {json.dumps(param)}")


def __param(_type: str, optional: bool = False, ref: bool = False, flags: list = None):
    return {'type': _type, 'optional': optional, 'ref': ref, 'flags': flags}


def _only_types(param: list) -> bool:
    return not any(item for item in param if not __is_valid_type(item))


def _any_types(param: list) -> bool:
    return any(item for item in param if __is_valid_type(item))


def __is_valid_type(param_type: str) -> bool:
    if isinstance(param_type, dict):
        return param_type['type'] == 'array'
    return param_type in ['string', 'string[]', 'int', 'array', 'array[]']


def __is_valid_flag(flag: str) -> bool:
    return bool(re.match(r"^[A-Z]+(_[A-Z]+){0,4}$", flag))


class ParameterTypeException(Exception):
    pass
