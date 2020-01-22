import unittest

from documentary.details.preprocess_details import polyfill_methods


class DetailsPolyfillMethodsTest(unittest.TestCase):
    def test_empty(self):
        self.assertEqual({}, polyfill_methods({}))

    def test_polyfill_method(self):
        # given
        given = {"foo": {
            "name": 'foo',
            "definition": 'some definition',
            "param": {},
            "return": 'some return value',
            "return-type": 'int',
            "throws": ['FooException'],
            "see": ['bar'],
            "link": ['http://google.com'],
        }}

        # when
        result = polyfill_methods(given)

        # then
        self.assertEqual(second=result, first={
            'foo': {
                "name": 'foo',
                "definition": 'some definition',
                "param": {},
                "return": 'some return value',
                "return-type": 'int',
                "throws": ['FooException'],
                "see": ['bar'],
                "link": ['http://google.com'],
            }
        })

    def test_empty_method(self):
        # given
        given = {"foo": {}}

        # when
        result = polyfill_methods(given)

        # then
        self.assertEqual(second=result, first={
            'foo': {
                "name": 'foo',
                "definition": None,
                "param": {},
                "return": None,
                "return-type": None,
                "throws": [],
                "see": [],
                "link": [],
            }
        })
