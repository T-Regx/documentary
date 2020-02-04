import unittest

from documentary.markup import replace_template_strings


class CodePartsTest(unittest.TestCase):
    def test_replace_parts_b(self):
        # when
        code = replace_template_strings("Foo `code` Bar", lambda x: 'b')

        # then
        self.assertEqual(code, "Foo <b>code</b> Bar")

    def test_replace_parts_i(self):
        # when
        code = replace_template_strings("Foo `code` Bar", lambda x: 'i')

        # then
        self.assertEqual(code, "Foo <i>code</i> Bar")

    def test_pass_parameter_name(self):
        # when
        replace_template_strings("Foo `code` Bar", lambda x: self.assertEqual('code', x))
