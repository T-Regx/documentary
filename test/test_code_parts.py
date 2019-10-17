import unittest

from code_parts import replace_code_parts


class CodePartsTest(unittest.TestCase):
    def test_replace_parts_b(self):
        # when
        code = replace_code_parts("Foo `code` Bar", lambda x: False)

        # then
        self.assertEqual(code, "Foo <b>code</b> Bar")

    def test_replace_parts_i(self):
        # when
        code = replace_code_parts("Foo `code` Bar", lambda x: True)

        # then
        self.assertEqual(code, "Foo <i>code</i> Bar")
