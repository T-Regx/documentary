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
        self.assertEqual(result, {
            'print': {
                'name': 'print',
                'definition': 'Replaced string',
                'param': {'text': {'type': 'string', 'optional': False, 'ref': False, 'flags': None}},
                'return': 'replaced string',
                'return-type': 'string',
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

    def test_join_global_with_empty(self):
        # given
        decorations = {
            'methods': {'foo': {}, 'bar': {}, 'lorem': {}},
            'groups': {'see': [['foo', 'bar', 'lorem']]},
            '*': {
                'see': ['one'],
                'link': ['two'],
                'throws': ['three'],
            }
        }

        # when
        result = build_details(links=decorations)

        # then
        self.assertEqual(second=result, first={
            'foo': {
                'see': ['one', 'bar', 'lorem'],
                'link': ['two'],
                'throws': ['three']
            },

            'bar': {
                'see': ['one', 'foo', 'lorem'],
                'link': ['two'],
                'throws': ['three']
            },

            'lorem': {
                'see': ['one', 'foo', 'bar'],
                'link': ['two'],
                'throws': ['three']
            }
        })

    def test_decoration_without_see(self):
        # when
        result = build_details({}, {}, links={'methods': {'method': {}}})

        # then
        self.assertEqual(result, {'method': {}})
