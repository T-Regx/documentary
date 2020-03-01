from argparse import Namespace as args
from unittest import TestCase

from documentary.paths import resolve_paths
from test.tmpdir import directory


class PathsTest(TestCase):
    def test_default(self):
        with directory() as tmp:
            # given
            tmp.dir('documentary')
            tmp.store(['src'], '')
            tmp.store(['documentary', 'src'], '')

            # when
            doc, root, template, output = resolve_paths(args(root=tmp(), template='src'))

            # then
            self.assertEqual(tmp('documentary'), doc, msg='Failed to assert that documentary path is returned')
            self.assertEqual(tmp(), root, msg='Failed to assert that root path is current working directory')
            self.assertEqual('src', template, msg='Failed to assert template is joined with current working directory')
            self.assertEqual(root, output, msg="Failed to assert that output path is root path")

    def test_raise_for_missing_documentary(self):
        with directory() as tmp:
            # given
            with self.assertRaises(Exception) as error:
                # when
                resolve_paths(args(root=tmp(), template='src'))

            # then
            self.assertEqual(tmp.strip(str(error.exception)), 'To generate documentation, navigate to a directory with "documentary" folder')

    def test_raise_for_missing_template(self):
        with directory() as tmp:
            # given
            tmp.dir('documentary')

            # when
            with self.assertRaises(Exception) as error:
                # when
                resolve_paths(args(root=tmp(), template='src'))

            # then
            self.assertEqual(r"""Tried to documentation file "\src", but it doesn't exist""", tmp.strip((str(error.exception))))

    def test_raise_for_missing_documentation(self):
        with directory() as tmp:
            # given
            tmp.dir('documentary')
            tmp.store(['src'], '')

            # when
            with self.assertRaises(Exception) as error:
                # when
                resolve_paths(args(root=tmp(), template='src'))

            # then
            self.assertEqual('Directory "src" is missing in documentary folder', str(error.exception))
