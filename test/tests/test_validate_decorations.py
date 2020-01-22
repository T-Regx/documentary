from unittest import TestCase

from schema import SchemaError

from documentary.validate import decorations


class DefaultsDecorationsTest(TestCase):
    # Zero level down

    def test_empty(self):
        decorations({})

    # First level down

    def test_empty_methods(self):
        decorations({"methods": {}})

    def test_empty_groups(self):
        decorations({"groups": {}})

    def test_empty_asterisk(self):
        decorations({"*": {}})

    def test_empty_first_level(self):
        decorations({
            "methods": {},
            "groups": {},
            "*": {}
        })

    # Second level down

    def test_empty_method(self):
        decorations({"methods": {"match": {}}})

    def test_empty_group_see(self):
        decorations({"groups": {"see": []}})

    def test_empty_group_throws(self):
        decorations({"groups": {"throws": []}})

    def test_empty_asterisk_see(self):
        decorations({"*": {"see": []}})

    def test_empty_asterisk_link(self):
        decorations({"*": {"link": []}})

    def test_empty_asterisk_throws(self):
        decorations({"*": {"see": []}})

    # Third level down

    def test_method_see(self):
        decorations({"methods": {"match": {"see": []}}})

    def test_method_link(self):
        decorations({"methods": {"match": {"link": []}}})

    def test_method_manual(self):
        decorations({"methods": {"match": {"manual": {}}}})

    def test_method_throws(self):
        decorations({"methods": {"match": {"throws": []}}})

    def test_method_raise_throws_half_methods(self):
        self.assertRaises(SchemaError, lambda: decorations({"methods": {"match": {"throws": [{"methods": []}]}}}))

    def test_method_raise_throws_half_exceptions(self):
        self.assertRaises(SchemaError, lambda: decorations({"methods": {"match": {"throws": [{"exceptions": []}]}}}))

    def test_group_see_raise_on_empty_group(self):
        # given
        invalid_groups = {
            'empty': [[]],
            'single': [['A']],
        }

        # when
        for name, invalid in invalid_groups.items():
            with self.subTest(name):
                self.assertRaises(SchemaError, lambda: decorations({"groups": {"see": invalid}}))

    def test_full(self):
        decorations({
            "methods": {
                "match": {
                    "see": ["match_all"],
                    "link": ["http://google.com"],
                    "manual": {
                        "a": "https://www.php.net/manual/en/function.preg-match.php",
                        "b": "https://t-regx.com/docs/match-first"
                    },
                    "throws": ['RuntimeException']
                },
                "match_all": {
                    "see": ["match"],
                    "link": ["https://faceboob.com"],
                    "manual": {
                        "a": "https://www.php.net/manual/en/function.preg-match-all.php",
                        "b": "https://t-regx.com/docs/match"
                    },
                    "throws": ["Exception"]
                },
            },
            "groups": {
                "see": [[
                    "match",
                    "match_all"
                ]],
                "throws": [{
                    "methods": ["match", "match_all"],
                    "exceptions": ["MalformedPatternException", "RuntimeSafeRegexException"]
                }]
            },
            "*": {
                "see": [
                    "pattern()",
                    "Pattern::of()"
                ],
                "link": [
                    "https://t-regx.com",
                    "https://www.regular-expressions.info/unicode.html"
                ],
                "throws": [
                    'SafeRegexException'
                ]
            }
        })
