from os.path import join
from unittest import TestCase

from documentary.template import bootstrap


class TemplateTest(TestCase):
    def setUp(self) -> None:
        self.maxDiff = 65513

    def test(self):
        # given
        details = self.details('Summary', 'amount', 'int')

        # then
        self.assertRendersTemplateForMethod(details, """
        /**
         * {documentary:method}
         *
         * Summary.
         *
         * @return int amount
         */""")

    def test_missing_definition(self):
        # given
        details = self.details(None, 'amount', 'int')

        # then
        self.assertRendersTemplateForMethod(details, """
        /**
         * {documentary:method}
         *
         * @return int amount
         */""")

    def test_missing_return(self):
        # given
        details = self.details('Summary')

        # then
        self.assertRendersTemplateForMethod(details, """ /**
  * {documentary:method}
  *
  * Summary.
  */""")

    def test_undocumented_method(self):
        # given
        details = {}

        # then
        self.assertRendersTemplateForMethod(details, """
 /**
  * {documentary:method}
  */
  """)

    def test_placeholder_mixed(self):
        self.assertRendersTemplateForMethod(self.details(), """
    /**
     * {@documentary:method}
     */
     """)

    def test_placeholder_tag(self):
        self.assertRendersTemplateForMethod(self.details(), """
    /**
     * @documentary method
     */
     """)

    def assertRendersTemplateForMethod(self, details: dict, content: str):
        # given
        actual = self.render_document(details, content)

        # then
        self.assertEqual(content, actual)

    def render_document(self, details: dict, content: str) -> str:
        documentary = 'resources/input/documentary'
        template = bootstrap(details, documentary, join(documentary, 'SafeRegex/preg.php', 'fragments'), True)
        return template(content)

    def details(self, definition: str = None, _return=None, return_type=None) -> dict:
        return {
            'method': {
                'name': 'method',
                'definition': definition,
                'param': {},
                'return': _return,
                'return-type': return_type,
                'throws': [],
                'see': [],
                'link': [],
            }
        }
