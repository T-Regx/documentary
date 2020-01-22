import unittest
from typing import Any


class TestCase(unittest.TestCase):
    def assertEqual(self, expected: Any, actual: Any, msg: str = None) -> None:
        super().assertEqual(first=expected, second=actual)

    def assertCountEqual(self, expected: Any, actual: Any, msg: str = None) -> None:
        super().assertCountEqual(first=expected, second=actual)
