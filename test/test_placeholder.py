import unittest

from placeholder import populate


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
        result = populate(string, lambda _, __: 'Replaced')

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
        populate(string, lambda param, _: self.assertEqual('input_parameter', param))

    def test_calls_with_indent(self):
        # given
        string = self.given_document()

        # when
        populate(string, lambda _, indent: self.assertEqual(8, indent))

    def given_document(self) -> str:
        return """
        Some text
        /**
         * {@documentary:input_parameter}
         *
         * Foo Bar
         */
        Some other text
        """

    def test_ignore_param_missing(self):
        self.assertIgnoresPlaceholder("""
        /**
         * {@documentary:}
         */
        """)

    def test_ignore_param_syntax_error(self):
        self.assertIgnoresPlaceholder("""
        /**
         * {@documentary:!@#}
         */
        """)

    def test_ignore_placeholder_unclosed(self):
        self.assertIgnoresPlaceholder("""
        /**
         * {@documentary:work}
        """)

    def test_ignore_commented_out_with_hash(self):
        self.assertIgnoresPlaceholder("""
    #   /**
         * {@documentary:work}
         */
        """)

    def test_ignore_commented_out_with_double_slash(self):
        self.assertIgnoresPlaceholder("""
       //**
         * {@documentary:work}
         */
        """)

    def test_ignore_commented_out_with_double_slash_2(self):
        self.assertIgnoresPlaceholder("""
    //  /**
         * {@documentary:work}
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
         * {@documentary:work}
         */
        """)

    def test_populates_comment_above(self):
        # given
        string = """
    #
        /**
         * {@documentary:work}
         */
        """

        # when
        result = populate(string, lambda _, __: 'Replaced')

        # then
        self.assertEqual(second=result, first="\n    #\nReplaced\n        ")

    def test_replaces_non_greedy(self):
        # given
        string = """
        /**
         * {@documentary:work}
         */
         */
        """

        # when
        result = populate(string, lambda _, __: 'Replaced')

        # then
        self.assertEqual(second=result, first="\nReplaced\n         */\n        ")

    def assertIgnoresPlaceholder(self, string: str):
        self.assertEqual(first=string,
                         second=populate(string, lambda _, __: ''),
                         msg="Failed to assert that malformed placeholder was ignored")
