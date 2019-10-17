import unittest

from utils import first


class UtilsTest(unittest.TestCase):
    def test_first(self):
        # when
        value = first([1, 2, 3], lambda x: x == 2)

        # then
        self.assertEqual(value, 2)

    def test_first_none(self):
        # when
        value = first([1, 2, 3], lambda x: False)

        # then
        self.assertIsNone(value)
