import unittest
from typing import Union
from unittest.mock import Mock

from documentary.placeholder import populate


class PlaceholderTest(unittest.TestCase):
    def test_empty(self):
        # when
        result = populate('', lambda: self.fail())

        # then
        self.assertEqual(second=result, first='')

    def test_populate(self):
        # given
        string = self.given_document()

        # when
        result = populate(string, lambda *_: 'Replaced')

        # then
        self.assertEqual(second=result, first="""
        Some text
Replaced
        Some other text
        """)

    def test_calls_with_template_parameter(self):
        # given
        string = self.given_document()

        # when
        populate(string, lambda param, _, __: self.assertEqual('input_parameter', param))

    def test_calls_with_indent(self):
        # given
        string = self.given_document()

        # when
        populate(string, lambda _, indent, __: self.assertEqual(8, indent))

    def test_calls_with_placeholder(self):
        # given
        string = self.given_document()

        # when
        populate(string, lambda _, __, placeholder: self.assertEqual('{documentary:input_parameter}', placeholder))

    def given_document(self) -> str:
        return """
        Some text
        /**
         * {documentary:input_parameter}
         *
         * Foo Bar
         */
        Some other text
        """

    def test_ignore_param_missing(self):
        self.assertIgnoresPlaceholder("""
        /**
         * {documentary:}
         */
        """)

    def test_ignore_param_syntax_error(self):
        self.assertIgnoresPlaceholder("""
        /**
         * {documentary:!@#}
         */
        """)

    def test_ignore_placeholder_unclosed(self):
        self.assertIgnoresPlaceholder("""
        /**
         * {documentary:work}
        """)

    def test_ignore_commented_out_with_hash(self):
        self.assertIgnoresPlaceholder("""
    #   /**
         * {documentary:work}
         */
        """)

    def test_ignore_commented_out_with_double_slash(self):
        self.assertIgnoresPlaceholder("""
       //**
         * {documentary:work}
         */
        """)

    def test_ignore_commented_out_with_double_slash_2(self):
        self.assertIgnoresPlaceholder("""
    //  /**
         * {documentary:work}
         */
        """)

    def test_ignore_other_placeholder(self):
        self.assertIgnoresPlaceholder("""
        /**
         * {@other:work}
         */
        """)

    def test_ignore_polluted_placeholder(self):
        self.assertIgnoresPlaceholder("""
        /**
         * asd
         * {documentary:work}
         */
        """)

    def test_populates_comment_above(self):
        # given
        string = """
    #
        /**
         * {documentary:work}
         */
        """

        # when
        result = populate(string, lambda *_: 'Replaced')

        # then
        self.assertEqual(second=result, first="\n    #\nReplaced\n        ")

    def test_replaces_minimal(self):
        # given
        string = "/**{documentary:foo}*/"

        # when
        result = populate(string, lambda *_: 'Replaced')

        # then
        self.assertEqual(second=result, first="Replaced")

    def test_replaces_non_greedy(self):
        # given
        string = """
        /**
         * {documentary:work}
         */
         */
        """

        # when
        result = populate(string, lambda *_: 'Replaced')

        # then
        self.assertEqual(second=result, first="\nReplaced\n         */\n        ")

    def assertIgnoresPlaceholder(self, string: str):
        self.assertEqual(first=string,
                         second=populate(string, lambda *_: ''),
                         msg="Failed to assert that malformed placeholder was ignored")

    def test_ignore_placeholder_if_replacement_is_none(self):
        # given
        string = self.given_document()

        # when
        result = populate(string, lambda *_: None)

        # then
        self.assertEqual(string, result)

    def test_should_raise_for_invalid_replacement(self):
        # given
        string = self.given_document()

        # when
        with self.assertRaises(TypeError) as error:
            populate(string, lambda *_: 2)

        # then
        self.assertEqual(str(error.exception), 'Invalid replacement type')

    def test_should_parse_placeholders(self):
        # given
        placeholders = {
            'def': ("/**{documentary:foo}*/", '{documentary:foo}'),
            'mix': ("/**{@documentary:foo}*/", '{@documentary:foo}'),
            'tag': ("/**@documentary foo*/", '@documentary foo'),

            'def,space': ('/** {documentary:foo} */', '{documentary:foo}'),
            'mix,space': ('/** {@documentary:foo} */', '{@documentary:foo}'),
            'tag,space': ('/** @documentary foo */', '@documentary foo'),
        }

        for name, (template, expected) in placeholders.items():
            with self.subTest(name):
                # when
                placeholder = self.parse(template)

                # then
                self.assertIsNotNone(placeholder, msg=f"Failed to assert that template '{template}' is valid")
                self.assertEqual(expected, placeholder)

    def test_should_not_parse_placeholders(self):
        malformed_placeholders = {
            'at,open': '/**{@documentary:a */',
            'at,closed': '/**@documentary:a}*/',
            'def,open': '/**{documentary:a */',
            'def,closed': '/**documentary:a}*/',

            'tag,colon': '/** @documentary:a */',
            'def,space-in': '/** {documentary a} */',
            'mix,space-in': '/** {@documentary a} */',

            'malformed,space': '/** documentary a */',
            'malformed,colon': '/** documentary:a */',
        }

        for name, template in malformed_placeholders.items():
            with self.subTest(name):
                # when
                self.assertEqual(None, self.parse(template), msg=f"Failed to assert that template '{template}' is invalid")

    def parse(self, template: str) -> Union[None, str]:
        mock = Mock(return_value='')
        populate(template, mock)
        if len(mock.call_args_list) == 0:
            return None
        if len(mock.call_args_list) == 1:
            [((name, indent, template), kwargs)] = mock.call_args_list
            return template
        raise Exception()
