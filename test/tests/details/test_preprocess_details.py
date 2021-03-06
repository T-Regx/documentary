import unittest

from documentary.details.preprocess_details import build_details


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
                'link': ['https://google.com'],
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
        self.assertEqual(second=result, first={
            'print': {
                'definition': 'Replaced string',
                'param': {'text': {'type': 'string', 'optional': False, 'ref': False, 'flags': None}},
                'return': 'replaced string',
                'return-type': 'string',
                'template': {},
                'see': [],
                'link': ['https://google.com'],
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
