import unittest

from utils import first, interlace


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

    def test_interlace(self):
        self.assertEqual([], interlace([], ''))
        self.assertEqual([1], interlace([1], ''))
        self.assertEqual([1, '', 2, '', 3], interlace([1, 2, 3], ''))
        self.assertEqual([1, '', 2], interlace([1, 2], ''))
