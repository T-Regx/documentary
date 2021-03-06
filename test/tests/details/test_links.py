import unittest

from documentary.details.preprocess_details import build_links


class DetailsTest(unittest.TestCase):
    def test_default_see(self):
        # given
        decorations = {'methods': {'print': {'see': ['see1', 'see2'], 'link': ['link1', 'link2']}}}

        # when
        result = build_links(decorations)

        # then
        self.assertEqual(result, {
            'print': {
                'see': ['see1', 'see2'],
                'link': ['link1', 'link2'],
            }
        })

    def test_see_groups(self):
        # given
        decorations = {
            'methods': {
                'replace_much': {'see': ['Foo']},
                'search': {'see': ['Lorem']},
                'replace': {'see': ['Bar']},
                'search_very': {'see': ['Ipsum']},
                'eval': {'see': ['Dont fucking use this!']}
            },
            'groups': {
                'see': [
                    ['replace_much', 'replace'],
                    ['search', 'search_very'],
                ]
            }
        }

        # when
        result = build_links(decorations)

        # then
        self.assertEqual(result, {
            'replace_much': {'see': ['Foo', 'replace']},
            'search': {'see': ['Lorem', 'search_very']},
            'replace': {'see': ['Bar', 'replace_much']},
            'search_very': {'see': ['Ipsum', 'search']},
            'eval': {'see': ['Dont fucking use this!']}
        })

    def test_see_groups_raises_for_missing_methods(self):
        # given
        decorations = {
            'methods': {},
            'groups': {'see': [['other', 'bar']]}
        }

        # when
        with self.assertRaises(Exception) as error:
            build_links(decorations)

        # then
        self.assertEqual("Method 'other' used in 'groups.see' is not declared", str(error.exception))

    def test_asterisk(self):
        # given
        decorations = {
            'methods': {'print': {'see': ['see-method'], 'link': ['://link'], 'throws': ['exception']}},
            '*': {'see': ['global-see', 'another-global-see'], 'link': ['global-link'], 'throws': ['global-throw']}
        }

        # when
        result = build_links(decorations)

        # then
        self.assertEqual({
            'print': {
                'see': ['see-method', 'global-see', 'another-global-see'],
                'link': ['://link', 'global-link'],
                'throws': ['exception', 'global-throw']
            }
        }, result)

    def test_throws_groups(self):
        # given
        decorations = {
            'methods': {
                'replace_much': {'throws': ['Foo']},
                'search': {'throws': ['Lorem']},
                'replace': {'throws': ['Bar']},
                'search_very': {'throws': ['Ipsum']},
                'eval': {'throws': ['Dont fucking use this!']}
            },
            'groups': {
                'see': [],
                'throws': [
                    {'methods': ['replace_much', 'replace'], 'exceptions': ['a', 'b']},
                    {'methods': ['search', 'search_very'], 'exceptions': ['c', 'd']},
                ]
            }
        }

        # when
        result = build_links(decorations)

        # then
        self.assertEqual(second=result, first={
            'replace_much': {'throws': ['Foo', 'a', 'b']},
            'search': {'throws': ['Lorem', 'c', 'd']},
            'replace': {'throws': ['Bar', 'a', 'b']},
            'search_very': {'throws': ['Ipsum', 'c', 'd']},
            'eval': {'throws': ['Dont fucking use this!']}
        })

    def test_throws_groups_raises_for_missing_methods(self):
        # given
        decorations = {
            'methods': {},
            'groups': {'throws': [{'methods': ['foo', 'bar'], 'exceptions': []}]}
        }

        # when
        with self.assertRaises(Exception) as error:
            build_links(decorations)

        # then
        self.assertEqual(str(error.exception), "Method 'foo' used in 'groups.throws' is not declared")

    def test_decoration_without_see(self):
        # when
        result = build_links({'methods': {'method': {}}})

        # then
        self.assertEqual(result, {'method': {}})

    def test_join_global_with_empty(self):
        # given
        decorations = {
            'methods': {'foo': {}, 'bar': {}, 'lorem': {}},
            'groups': {'see': [['foo', 'bar', 'lorem']]},
            '*': {
                'see': ['one'],
                'link': ['two'],
                'throws': ['three'],
            }
        }

        # when
        result = build_links(decorations)

        # then
        self.assertEqual(second=result, first={
            'foo': {
                'see': ['one', 'bar', 'lorem'],
                'link': ['two'],
                'throws': ['three']
            },

            'bar': {
                'see': ['one', 'foo', 'lorem'],
                'link': ['two'],
                'throws': ['three']
            },

            'lorem': {
                'see': ['one', 'foo', 'bar'],
                'link': ['two'],
                'throws': ['three']
            }
        })
