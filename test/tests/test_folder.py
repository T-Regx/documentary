from documentary.folder import discover_templates, TemplatesDiscoveryException
from test.TestCase import TestCase
from test.tmpdir import directory


class FolderTest(TestCase):
    def test_should_raise_for_no_documentary(self):
        with directory() as tmp:
            # given
            tmp.store('src/file', 'template')

            # when
            with self.assertRaises(TemplatesDiscoveryException) as error:
                discover_templates('src', tmp.join(), tmp.join('documentary'))

            # then
            self.assertEqual("File/folder 'src' is not documented", str(error.exception))

    def test_should_discover_itself(self):
        with directory() as tmp:
            # given
            tmp.store('src/app/first.py', 'template')

            # when
            result = discover_templates('src/app/first.py', tmp.join(), tmp.join('documentary'))

            # then
            self.assertEqual(['src/app/first.py'], result)

    def test_should_raise_for_missing_file(self):
        with directory() as tmp:
            # given
            tmp.store('src/app/first.py', 'template')

            # when
            with self.assertRaises(FileNotFoundError) as error:
                discover_templates('src/app/second.py', tmp.join(), tmp.join('documentary'))

            # then
            self.assertEqual(str(error.exception), "File/folder 'src/app/second.py' does not exist")

    def test_should_discover_children(self):
        with directory() as tmp:
            # given - templates
            tmp.store('src/main/second.py', 'template file')
            tmp.store('src/main/sub/first.py', 'template file')
            tmp.store('src/test/first.py', 'template file')
            # given - documents
            tmp.store('docs/src/main/first.py/definition.json', '{}')
            tmp.store('docs/src/main/second.py/definition.json', '{}')
            tmp.store('docs/src/main/sub/first.py/definition.json', '{}')
            tmp.store('docs/src/main/sub/second.py/definition.json', '{}')
            tmp.store('docs/src/test/first.py/definition.json', '{}')
            tmp.store('docs/src/test/second.py/definition.json', '{}')

            # when
            result = discover_templates('src', tmp.join(), documentary=tmp.join('docs'))

            # then
            self.assertCountEqual(actual=result, expected=[
                'src/main/second.py',
                'src/main/sub/first.py',
                'src/test/first.py',
            ])

    def test_should_raise_for_not_documented_folder(self):
        with directory() as tmp:
            # given
            tmp.store('src/main/second.py', 'template file')
            tmp.dir('docs/src/test')

            # when
            with self.assertRaises(TemplatesDiscoveryException) as error:
                discover_templates('src/main', tmp.join(), documentary=tmp.join('docs'))

            # then
            self.assertEqual("File/folder 'src/main' is not documented", str(error.exception))
