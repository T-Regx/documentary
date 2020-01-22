import unittest

from documentary.details.preprocess_details import ParameterTypeException, build_params


class DetailsTest(unittest.TestCase):

    def test_parse_parameters_defaults(self):
        # given
        declarations = {'str_replace': {'param': {'text': {'type': 'array[]'}}}}

        # when
        result = build_params(params=declarations)

        # then
        self.assertEqual(result, {
            'str_replace': {'param': {'text': {'type': 'array[]', 'optional': False, 'ref': False, 'flags': None}}}})

    def test_parse_parameters_dict(self):
        # given
        declarations = {
            'str_replace': {'param': {'text': {'type': 'int', 'optional': True, 'ref': True}}}}

        # when
        result = build_params(params=declarations)

        # then
        self.assertEqual(result, {
            'str_replace': {'param': {'text': {'type': 'int', 'optional': True, 'ref': True, 'flags': None}}}})

    def test_parse_parameters_dict_flags_as_list(self):
        # given
        declarations = {'str_replace': {'param': {'text': {'bit-sum': ['FLAG_ONE']}}}}

        # when
        result = build_params(params=declarations)

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
        result = build_params(params=declarations)

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
        result = build_params(params=declarations)

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
        result = build_params(params=declarations)

        # then
        self.assertEqual(result, {
            'str_replace': {
                'param': {'flags': {'type': 'int', 'optional': True, 'ref': False, 'flags': ['FLAG_SINGLE']}}}
        })

    def test_parameter_dict_throw_on_no_type(self):
        # then
        self.assertRaises(ParameterTypeException, build_params,
                          params={'str_replace': {'param': {'parameter': {}}}})
