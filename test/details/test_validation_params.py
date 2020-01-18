import unittest

from schema import SchemaError

from documentary.details.preprocess_details import build_details


class DetailsParamsValidationTest(unittest.TestCase):
    def test_list_throw_on_invalid_type(self):
        self.assertParamsInvalid({'str_replace': {'param': {'invalid-type': ['asd']}}})

    def test_dict_throw_on_invalid_type(self):
        self.assertParamsInvalid({'str_replace': {'param': {'text': {'type': 'asd'}}}})

    def test_dict_throw_on_invalid_flag(self):
        # then
        self.assertParamsInvalid({'str_replace': {'param': {'text': {'flags': ['lowercase']}}}})
        self.assertParamsInvalid({'str_replace': {'param': {'text': {'flags': [' ']}}}})
        self.assertParamsInvalid({'str_replace': {'param': {'text': {'flags': ['ONE_VALID', '-invalid-']}}}})

    def test_list_throw_on_empty_flag(self):
        # then
        self.assertParamsInvalid({'str_replace': {'param': {'p': {'flags': []}}}})
        self.assertParamsInvalid({'str_replace': {'param': {'p': {'flags': None}}}})

    def test_list_throw_on_no_type(self):
        # then
        self.assertParamsInvalid({'str_replace': {'param': {'parameter': ['optional']}}})

    def assertParamsInvalid(self, params: dict) -> None:
        self.assertRaises(SchemaError, build_details, params=params)
