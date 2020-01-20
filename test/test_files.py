from unittest import TestCase

from documentary.files import fragment_fallback, MissingFragmentException, fragment
from test.tmpdir import directory


class FormatTest(TestCase):
    def test_should_traverse_fallback(self):
        with directory() as tmp:
            # given
            tmp.store(['folder', 'first.html'], 'Foo')

            # when
            result = fragment_fallback(tmp.join('folder'), 'first', 'second', tmp.join())

            # then
            self.assertEqual(result, "Foo")

    def test_should_traverse_fallback_second(self):
        with directory() as tmp:
            # given
            tmp.store(['folder', 'second.html'], 'Bar')

            # when
            result = fragment_fallback(tmp.join('folder'), 'first', 'second', tmp.join())

            # then
            self.assertEqual(result, "Bar")

    def test_should_traverse_fallback_project(self):
        with directory() as tmp:
            # given
            tmp.store(['project', 'fragment', 'second.html'], 'Global')
            tmp.store(['a', 'b', 'c', 'foo.html'], '')

            # when
            result = fragment_fallback(tmp.join('a', 'b', 'c'), 'first', 'second', tmp.join())

            # then
            self.assertEqual(result, "Global")

    def test_should_raise_for_missing_fragment(self):
        with directory() as tmp:
            # then
            self.assertRaises(MissingFragmentException, lambda: fragment(tmp.join('folder'), 'missing'))

    def test_should_return_default_for_missing_fragment(self):
        with directory() as tmp:
            # when
            result = fragment(tmp.join('folder'), 'missing', default=lambda: 'returned')

            # then
            self.assertEqual('returned', result)
