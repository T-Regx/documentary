# Recursive dictionary merge
# Copyright (C) 2016 Paul Durivage <pauldurivage+github@gmail.com>
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
import collections
import json


def merge_dictionaries(dictionaries: list, allow_override: bool = True) -> dict:
    if len(dictionaries) == 0:
        return {}
    if len(dictionaries) == 1:
        return dictionaries[0]
    base = dictionaries.pop(0).copy()
    for dictionary in dictionaries:
        __dict_merge(base, dictionary, allow_override)
    return base


def __dict_merge(dictionary: dict, copy_from: dict, allow_override: bool = True) -> None:
    for k, v in copy_from.items():
        if (k in dictionary and isinstance(dictionary[k], dict)
                and isinstance(copy_from[k], collections.Mapping)):
            __dict_merge(dictionary[k], copy_from[k])
        else:
            if not allow_override and k in dictionary:
                raise DuplicateKeysException("key '{}' duplicated in both dictionaries ({}, {})"
                                             .format(k, json.dumps(dictionary), json.dumps(copy_from)))
            dictionary[k] = copy_from[k]


class DuplicateKeysException(Exception):
    pass
