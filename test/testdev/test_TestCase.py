import unittest

from test.TestCase import TestCase


class TestCaseTest(unittest.TestCase):
    def test_empty(self):
        # when
        TestCase().assertPathsMatch([], [])

    def test_paths_match(self):
        # when
        with self.subTest("windows"):
            TestCase().assertPathsMatch(['a/b/c'], [r'a\b\c'], sep='\\')

        # when
        with self.subTest("unix"):
            TestCase().assertPathsMatch(['a/b/c'], [r'a/b/c'], sep='/')

    def test_paths_match_malformed(self):
        # given
        with self.subTest("windows"):
            # when
            self.assertRaises(AssertionError, lambda: TestCase().assertPathsMatch([r'a/b/c'], [r'a/b\c'], sep='\\'))

        # given
        with self.subTest("unix"):
            # when
            self.assertRaises(AssertionError, lambda: TestCase().assertPathsMatch([r'a/b/c'], [r'a\b/c'], sep='/'))
