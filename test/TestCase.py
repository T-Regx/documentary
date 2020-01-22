import os
import unittest
from typing import Any


class TestCase(unittest.TestCase):
    def assertEqual(self, expected: Any, actual: Any, msg: str = None) -> None:
        super().assertEqual(first=expected, second=actual)

    def assertPathsMatch(self, expected: list, actual: list, sep: str = None) -> None:
        self.assertCountDifference([e.replace('/', sep or os.sep) for e in expected], actual)

    def assertCountDifference(self, expected: list, actual: list):
        try:
            # assertCountEqual() performs comparison without regard for paths order,
            # which is desired, but when failed, the message doesn't provide
            # option to see a difference.
            super().assertCountEqual(expected, actual)
        except AssertionError:
            # So when assertCountEqual() assertion fails, we catch it and perform
            # regular assertEqual() assertion, so proper difference is displayed.
            super().assertEqual(expected, actual)
