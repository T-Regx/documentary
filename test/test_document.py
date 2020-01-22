from os.path import join
from unittest import TestCase

from documentary.document import document
from test.tmpdir import directory


class EndToEndTest(TestCase):
    def setUp(self) -> None:
        self.maxDiff = 65513

    def test(self):
        with directory() as tmp:
            # given
            documentary = 'resources/input/documentary'
            class_path = 'SafeRegex/preg.php'

            # when
            document(
                documentary_path=documentary,
                template_path='resources/input/SafeRegex/preg.php',
                class_path=join(documentary, class_path),
                output_path=tmp.join('preg.php'))

            # then
            with open('resources/expected/preg.php', 'r') as expected:
                self.assertEqual(expected.read(), tmp.open('preg.php'))
