import unittest

from preprocess_details import build_details


class DetailsTest(unittest.TestCase):
    def test_integration(self):
        # given
        declarations = {
            'print': {
                'param': {'text': 'string'},
                'return-type': 'string'
            }
        }
        decorations = {
            'methods': {'print': {
                'links': ['https://google.com'],
                'throws': []
            }},
        }
        definitions = {
            "print": {
                'definition': 'Replaced string',
                'return': 'replaced string'
            }
        }

        # when
        result = build_details(summaries=definitions, params=declarations, links=decorations)

        # then
        self.assertEqual(result, {
            'print': {
                'name': 'print',
                'definition': 'Replaced string',
                'param': {'text': {'type': 'string', 'optional': False, 'ref': False, 'flags': None}},
                'return': 'replaced string',
                'return-type': 'string',
                'links': ['https://google.com'],
                'throws': []
            }
        })

    def test_empty(self):
        # when
        result = build_details({}, {}, {})

        # then
        self.assertEqual(result, {})

    def test_none(self):
        # when
        result = build_details()

        # then
        self.assertEqual(result, {})
