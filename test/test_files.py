from unittest import TestCase

from files import fragment_fallback
from test.tmpdir import directory


class FormatTest(TestCase):
    def test_should_traverse_fallback(self):
        with directory() as tmp:
            # given
            tmp.store(['folder', 'first.html'], 'Foo')

            # when
            result = fragment_fallback(tmp.join('folder'), 'first', 'second')

            # then
            self.assertEqual(result, "Foo")

    def test_should_traverse_fallback_second(self):
        with directory() as tmp:
            # given
            tmp.store(['folder', 'second.html'], 'Bar')

            # when
            result = fragment_fallback(tmp.join('folder'), 'first', 'second')

            # then
            self.assertEqual(result, "Bar")
