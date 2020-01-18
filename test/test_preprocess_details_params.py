import unittest

from schema import SchemaError

from preprocess_details import build_details, ParameterTypeException


class DetailsTest(unittest.TestCase):

    def test_parse_parameters_defaults(self):
        # given
        declarations = {'str_replace': {'param': {'text': {'type': 'array[]'}}}}

        # when
        result = build_details(params=declarations)

        # then
        self.assertEqual(result, {
            'str_replace': {'param': {'text': {'type': 'array[]', 'optional': False, 'ref': False, 'flags': None}}}})

    def test_parse_parameters_dict(self):
        # given
        declarations = {
            'str_replace': {'param': {'text': {'type': 'int', 'optional': True, 'ref': True}}}}

        # when
        result = build_details(params=declarations)

        # then
        self.assertEqual(result, {
            'str_replace': {'param': {'text': {'type': 'int', 'optional': True, 'ref': True, 'flags': None}}}})

    def test_parse_parameters_dict_flags_as_list(self):
        # given
        declarations = {'str_replace': {'param': {'text': {'bit-sum': ['FLAG_ONE']}}}}

        # when
        result = build_details(params=declarations)

        # then
        self.assertEqual(result, {
            'str_replace': {'param': {'text': {'type': 'int', 'optional': True, 'ref': False, 'flags': ['FLAG_ONE']}}}})

    def test_parse_parameters_list(self):
        # given
        declarations = {
            'str_replace': {
                'param': {
                    'p1': ['string'],
                    'p2': ['int'],
                    'p3': ['string[]'],
                    'p4': ['string', 'optional', '&ref'],
                    'p5': ['string', '&ref'],
                    'p6': {'bit-sum': ['FLAG_ONE', 'FLAG_TWO', 'FLAG_THREE']}
                }
            }
        }

        # when
        result = build_details(params=declarations)

        # then
        self.assertEqual(result, {
            'str_replace': {
                'param': {
                    'p1': {'type': 'string', 'optional': False, 'ref': False, 'flags': None},
                    'p2': {'type': 'int', 'optional': False, 'ref': False, 'flags': None},
                    'p3': {'type': 'string[]', 'optional': False, 'ref': False, 'flags': None},
                    'p4': {'type': 'string', 'optional': True, 'ref': True, 'flags': None},
                    'p5': {'type': 'string', 'optional': False, 'ref': True, 'flags': None},
                    'p6': {'type': 'int', 'optional': True, 'ref': False,
                           'flags': ['FLAG_ONE', 'FLAG_TWO', 'FLAG_THREE']},
                },
            }
        })

    def test_parse_parameters_inherit(self):
        # given
        declarations = {
            'copy': {'param': {'from': 'string', 'to': 'string'}, 'return-type': 'string'},
            'mb_copy': {'inherit': 'copy'},
        }

        # when
        result = build_details(params=declarations)

        # then
        self.assertEqual(result, {
            'copy': {
                'param': {
                    'from': {'type': 'string', 'optional': False, 'ref': False, 'flags': None},
                    'to': {'type': 'string', 'optional': False, 'ref': False, 'flags': None}},
                'return-type': 'string'},
            'mb_copy': {'param': {
                'from': {'type': 'string', 'optional': False, 'ref': False, 'flags': None},
                'to': {'type': 'string', 'optional': False, 'ref': False, 'flags': None}},
                'return-type': 'string'}
        })

    def test_parse_parameters_list_single_flat(self):
        # given
        declarations = {'str_replace': {'param': {'flags': {'bit-sum': ['FLAG_SINGLE']}}}}

        # when
        result = build_details(params=declarations)

        # then
        self.assertEqual(result, {
            'str_replace': {
                'param': {'flags': {'type': 'int', 'optional': True, 'ref': False, 'flags': ['FLAG_SINGLE']}}}
        })

    def test_parameter_list_throw_on_invalid_type(self):
        # given
        declarations = {'str_replace': {'param': {'invalid-type': ['asd']}}}

        # then
        self.assertRaises(SchemaError, build_details, params=declarations)

    def test_parameter_dict_throw_on_invalid_type(self):
        # given
        declarations = {'str_replace': {'param': {'text': {'type': 'asd'}}}}

        # then
        self.assertRaises(SchemaError, build_details, params=declarations)

    def test_parameter_dict_throw_on_invalid_flag(self):
        # then
        self.assertRaises(SchemaError, build_details,
                          params={'str_replace': {'param': {'text': {'flags': ['lowercase']}}}})
        self.assertRaises(SchemaError, build_details,
                          params={'str_replace': {'param': {'text': {'flags': [' ']}}}})
        self.assertRaises(SchemaError, build_details,
                          params={'str_replace': {'param': {'text': {'flags': ['ONE_VALID', '-invalid-']}}}})

    def test_parameter_list_throw_on_empty_flag(self):
        # then
        self.assertRaises(SchemaError, build_details, params={'str_replace': {'param': {'p': {'flags': []}}}})
        self.assertRaises(SchemaError, build_details, params={'str_replace': {'param': {'p': {'flags': None}}}})

    def test_parameter_list_throw_on_no_type(self):
        # then
        self.assertRaises(SchemaError, build_details,
                          params={'str_replace': {'param': {'parameter': ['optional']}}})

    def test_parameter_dict_throw_on_no_type(self):
        # then
        self.assertRaises(ParameterTypeException, build_details,
                          params={'str_replace': {'param': {'parameter': {}}}})

    def test_decoration_without_see(self):
        # when
        result = build_details({}, {}, links={'methods': {'method': {}}})

        # then
        self.assertEqual(result, {'method': {}})
