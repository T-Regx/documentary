from unittest import TestCase
from unittest.mock import MagicMock

from documentary.markup import replace_template_strings


class CodePartsTest(TestCase):
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

    def test_array(self):
        # given
        mock = MagicMock(spec=lambda x: '')

        # when
        replace_template_strings("Foo `['Foo', \"Bar\"]` Bar", mock)

        # then
        mock.assert_called_with("['Foo', \"Bar\"]")
