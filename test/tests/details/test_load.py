from json import dumps
from unittest import TestCase

from documentary.details.preprocess_details import load_details
from test.tmpdir import directory


class LoadTest(TestCase):
    def test_empty_files(self):
        with directory() as tmp:
            # given
            tmp.store('declaration.json', dumps({}))
            tmp.store('decorations.json', dumps({}))
            tmp.store('definitions.json', dumps({}))

            # when
            details, _ = load_details(
                declaration=tmp.join('declaration.json'),
                decorations=tmp.join('decorations.json'),
                definitions=tmp.join('definitions.json'),
            )

            # then
            self.assertEqual(second=details, first={})

    def test_missing_files(self):
        with directory() as tmp:
            # when
            details, _ = load_details(
                declaration=tmp.join('missing.json'),
                decorations=tmp.join('missing.json'),
                definitions=tmp.join('missing.json'),
            )

            # then
            self.assertEqual({}, details)
