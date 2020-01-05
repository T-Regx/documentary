from unittest import TestCase

from validate import definitions


class DefaultsDefinitionsTest(TestCase):
    # Zero level down

    def test_empty(self):
        definitions({})

    # First level down

    def test_empty_first_level(self):
        definitions({
            "match_all": {},
        })

    # Second level down

    def test_definition(self):
        definitions({"match": {"definition": ""}})

    def test_return(self):
        definitions({"match": {"return": ""}})

    def test_full(self):
        definitions({
            "match": {
                "definition": "Performs a single regular expression match. Retrieves only the first matched occurrence.",
                "return": "`1` if the `pattern` matches given `subject`, `0` if it does not"
            },
            "match_all": {
                "definition": "Performs a global regular expression match",
                "return": "the number of `pattern` matched occurrences (which might be zero)"
            },
        })
