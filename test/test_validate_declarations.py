from unittest import TestCase

from schema import SchemaError

from validate import declarations


class DefaultsDeclarationsTest(TestCase):
    # Zero level down

    def test_empty(self):
        declarations({})

    # First level down

    def test_empty_first_level(self):
        declarations({"match": {}})

    # Third level down

    def test_empty_param(self):
        declarations({"match": {"param": {}}})

    def test_raise_on_invalid_param(self):
        self.assertRaises(SchemaError, lambda: declarations({"match": {"param": {"a": 2}}}))

    def test_full(self):
        declarations({
            "match": {
                "param": {
                    "pattern": "string",
                    "subject": "string",
                    "flags": ["PREG_OFFSET_CAPTURE", "PREG_UNMATCHED_AS_NULL"],
                    "matches": ["string[]", "optional", "&ref"],
                    "offset": ["int", "optional", "&ref"]
                },
                "return-type": "int"
            },
            "match_all": {
                "param": {
                    "pattern": "string",
                    "subject": "string",
                    "matches": ["array[]", "optional", "&ref"],
                    "flags": ["PREG_PATTERN_ORDER", "PREG_SET_ORDER", "PREG_OFFSET_CAPTURE", "PREG_UNMATCHED_AS_NULL"],
                    "offset": ["int", "optional", "&ref"]
                },
                "return-type": "int"
            },
        })
