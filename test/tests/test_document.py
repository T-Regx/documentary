from unittest import TestCase

from documentary.document import document
from test.resource import resource
from test.tmpdir import directory


class EndToEndTest(TestCase):
    def setUp(self) -> None:
        self.maxDiff = 65513

    def test_single(self):
        with directory() as tmp:
            # when
            document(documentary_path=resource('input/documentary'),
                     documentation_path=resource('input/documentary/SafeRegex/preg.php'),
                     template_path=resource('input/SafeRegex/preg.php'),
                     output_path=tmp.join('preg.php'))

            # then
            with open(resource('expected/preg.php'), 'r') as expected:
                self.assertEqual(expected.read(), tmp.open('preg.php'))
