from os.path import join
from unittest import TestCase

from documentary.template import render_template


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
        self.assertRendersTemplateForMethod(details, 'method', """/**
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
        self.assertRendersTemplateForMethod(details, 'method', """/**
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
        self.assertRendersTemplateForMethod(details, 'method', """/**
 * {@documentary:method}
 *
 * Summary.
 */""")

    def assertRendersTemplateForMethod(self, details: dict, method_name: str, expected: str):
        # given
        documentary = 'resources/input/documentary'
        class_path = 'SafeRegex/preg.php'

        # when
        actual = render_template(details, method_name, 0, documentary, join(documentary, class_path, 'fragments'), True)

        # then
        self.assertEqual(expected, actual)
