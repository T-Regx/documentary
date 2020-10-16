from documentary.document import document, document_many
from test.TestCase import TestCase
from test.resource import resource
from test.std_io import stubbed_output
from test.tmpdir import directory


class EndToEndTest(TestCase):
    def setUp(self) -> None:
        self.maxDiff = 65513

    def test_single(self):
        with stubbed_output() as lines:
            with directory() as tmp:
                # when
                document(documentary_path=resource('input/documentary'),
                         documentation_path=resource('input/documentary/src/SafeRegex/preg.php'),
                         template_path=resource('input/src/SafeRegex/preg.php'),
                         output_path=tmp.join('preg.php'))

                # then
                with open(resource('expected/preg.php'), 'r') as expected:
                    self.assertEqual(expected.read(), tmp.open('preg.php'))

                self.assertEqual([f'File "{resource("input/src/SafeRegex/preg.php")}" documented'], lines())

    def test_many(self):
        with stubbed_output() as lines:
            with directory() as tmp:
                # when
                document_many(
                    documentary_path=resource('input/documentary'),
                    root_path=resource('input'),
                    templates_path='src',
                    output_path=tmp.join('output'))

                # then
                with open(resource('expected/preg.php'), 'r') as expected:
                    self.assertEqual(expected.read(), tmp.open('output/src/SafeRegex/preg.php'))

                with open(resource('expected/Pattern.php'), 'r') as expected:
                    self.assertEqual(expected.read(), tmp.open('output/src/CleanRegex/Pattern.php'))

                self.assertPathsMatch(actual=lines(), expected=[
                    f'File "{resource("input")}/src/SafeRegex/preg.php" documented',
                    f'File "{resource("input")}/src/CleanRegex/Pattern.php" documented',
                ])
