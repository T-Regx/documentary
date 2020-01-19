from os.path import join
from unittest import TestCase

from documentary.template import bootstrap


class TemplateTest(TestCase):
    def setUp(self) -> None:
        self.maxDiff = 65513

    def test(self):
        # given
        details = {
            'method': {
                'name': 'method',
                'definition': 'Summary',
                'param': {},
                'return': 'amount',
                'return-type': 'int',
                'throws': [],
                'see': [],
                'link': [],
            }
        }

        # then
        self.assertRendersTemplateForMethod(details, """
        /**
         * {@documentary:method}
         *
         * Summary.
         *
         * @return int amount
         */""")

    def test_missing_definition(self):
        # given
        details = {
            'method': {
                'name': 'method',
                'definition': None,
                'param': {},
                'return': 'amount',
                'return-type': 'int',
                'throws': [],
                'see': [],
                'link': [],
            }
        }

        # then
        self.assertRendersTemplateForMethod(details, """
        /**
         * {@documentary:method}
         *
         * @return int amount
         */""")

    def test_missing_return(self):
        # given
        details = {
            'method': {
                'name': 'method',
                'definition': 'Summary',
                'param': {},
                'return': None,
                'return-type': None,
                'throws': [],
                'see': [],
                'link': [],
            }
        }

        # then
        self.assertRendersTemplateForMethod(details, """ /**
  * {@documentary:method}
  *
  * Summary.
  */""")

    def test_ignores_undocumented_method(self):
        # given
        details = {}

        # then
        self.assertRendersTemplateForMethod(details, """
 /**
  * {@documentary:method}
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
