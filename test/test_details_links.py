import unittest

from details import build_details


class DetailsTest(unittest.TestCase):
    def test_default_see(self):
        # given
        decorations = {'methods': {'print': {'see': ['see1', 'see2'], 'links': ['link1', 'link2']}}}

        # when
        result = build_details(links=decorations)

        # then
        self.assertEqual(result, {
            'print': {
                'see': ['see1', 'see2'],
                'links': ['link1', 'link2'],
            }
        })

    def test_groups(self):
        # given
        decorations = {
            'methods': {
                'replace_much': {'see': ['Foo']},
                'search': {'see': ['Lorem']},
                'replace': {'see': ['Bar']},
                'search_very': {'see': ['Ipsum']},
                'eval': {'see': ['Dont fucking use this!']}
            },
            'groups': [
                ['replace_much', 'replace'],
                ['search', 'search_very'],
            ]
        }

        # when
        result = build_details(links=decorations)

        # then
        self.assertEqual(result, {
            'replace_much': {'see': ['Foo', 'replace']},
            'search': {'see': ['Lorem', 'search_very']},
            'replace': {'see': ['Bar', 'replace_much']},
            'search_very': {'see': ['Ipsum', 'search']},
            'eval': {'see': ['Dont fucking use this!']}
        })

    def test_asterisk(self):
        # given
        decorations = {
            'methods': {'print': {'see': ['see-method'], 'link': ['://link'], 'throws': ['exception']}},
            '*': {'see': ['global-see', 'another-global-see'], 'link': ['global-link'], 'throws': ['global-throw']}
        }

        # when
        result = build_details(links=decorations)

        # then
        self.assertEqual({
            'print': {
                'see': ['see-method', 'global-see', 'another-global-see'],
                'link': ['://link', 'global-link'],
                'throws': ['exception', 'global-throw']
            }
        }, result)
