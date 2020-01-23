from os.path import join
from unittest import TestCase

from documentary.document import document
from test.resource import resource
from test.tmpdir import directory


class EndToEndTest(TestCase):
    def setUp(self) -> None:
        self.maxDiff = 65513

    def test(self):
        with directory() as tmp:
            # given
            documentary = resource('input/documentary')

            # when
            document(documentary_path=documentary,
                     documentation_path=join(documentary, 'SafeRegex/preg.php'),
                     template_path=resource('input/SafeRegex/preg.php'),
                     output_path=tmp.join('preg.php'))

            # then
            with open(resource('expected/preg.php'), 'r') as expected:
                self.assertEqual(expected.read(), tmp.open('preg.php'))
