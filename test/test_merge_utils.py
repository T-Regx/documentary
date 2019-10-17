from unittest import TestCase

from merge_utils import merge_dictionaries, DuplicateKeysException


class MergeUtilsTest(TestCase):
    def test_merge_directories(self):
        # given
        first, second = self.examples()

        # when
        result = merge_dictionaries([first, second])

        # then
        self.assertEqual(result, {
            "one": {
                "two": {
                    "nested-first": "Foo",
                    "nested-second": "Lorem",
                }
            },
            "first": "Bar",
            "second": "Ipsum",
            "common": "The new one"
        })

    def test_merge_without_overrides(self):
        # given
        first, second = self.examples()

        # then
        self.assertRaises(DuplicateKeysException, merge_dictionaries, [first, second], allow_override=False)

    @staticmethod
    def examples():
        first = {
            "one": {
                "two": {
                    "nested-first": "Foo"
                }
            },
            "first": "Bar",
            "common": "The old one"
        }
        second = {
            "one": {
                "two": {
                    "nested-second": "Lorem"
                }
            },
            "second": "Ipsum",
            "common": "The new one"
        }
        return first, second

    def test_single_dictionary(self):
        # given
        _input = {"a": 1, "b": 2}

        # when
        result = merge_dictionaries([_input])

        # then
        self.assertEqual(result, _input)

    def test_empty_list(self):
        # when
        result = merge_dictionaries([])

        # then
        self.assertEqual(result, {})
