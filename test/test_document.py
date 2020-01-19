from os.path import join
from unittest import TestCase

from documentary.document import document_file
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
            document_file(
                documentary=documentary,
                declaration=join(documentary, class_path, 'declaration.json'),
                decorations=join(documentary, class_path, 'decoration.json'),
                definitions=join(documentary, class_path, 'definition.json'),
                fragments=join(documentary, class_path, 'fragments'),
                filename='resources/input/SafeRegex/preg.php',
                output=tmp.join('preg.php'),
                include_template_tag=True,
            )

            # then
            with open('resources/expected/preg.php', 'r') as expected:
                self.assertEqual(expected.read(), tmp.open('preg.php'))
