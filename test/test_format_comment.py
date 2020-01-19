import unittest

from documentary.format_comment import print_method, format_preg_method


class FormatTest(unittest.TestCase):
    def test(self):
        # when
        result = self._print_method()

        # then
        self.assertEqual(result, """    /**
     * Just a summary.
     *
     * @return string just a return value
     */""")

    def test_include_template(self):
        # when
        result = self._print_method(include_template=True)

        # then
        self.assertEqual(result, """    /**
     * {@documentary:str_replace}
     *
     * Just a summary.
     *
     * @return string just a return value
     */""")

    def test_throws(self):
        # when
        result = self._print_method(throws=['ThirdException', 'FourthException'])

        # then
        self.assertEqual(result, """    /**
     * Just a summary.
     *
     * @return string just a return value
     *
     * @throws ThirdException
     * @throws FourthException
     */""")

    def test_multiple_return_types(self):
        # when
        result = self._print_method(
            return_type=['int', 'int[]'],
            _return={
                'int': {'when': 'if something', 'return': 'a number'},
                'int[]': {'when': 'otherwise', 'return': 'numbers'}
            })

        # then
        self.assertEqual(result, """    /**
     * Just a summary.
     *
     * @return int|int[] returns <b>int</b> if something, <b>int[]</b> otherwise
     * <ul>
     *  <li>a number if something</li>
     *  <li>numbers otherwise</li>
     * </ul>
     */""")

    def test_code_parts(self):
        # when
        result = self._print_method(definition='Function that replaces `word` with `other_word`',
                                    param={'word': {'type': 'int'}},
                                    _return='a value of `s`',
                                    param_mapper=lambda param: '%' + param + '%')

        # then
        self.assertEqual(result, """    /**
     * Function that replaces <i>word</i> with <b>other_word</b>.
     *
     * @param int $word %word%
     *
     * @return string a value of <b>s</b>
     */""")

    def test_multiple_param_types(self):
        # when
        result = self._print_method(param={'word': {'type': ['int', 'int[]']}},
                                    param_mapper=lambda x: 'Foo')

        # then
        self.assertEqual(result, """    /**
     * Just a summary.
     *
     * @param int|int[] $word Foo
     *
     * @return string just a return value
     */""")

    def test_see(self):
        # when
        result = self._print_method(see=['something', 'or nothing'])

        # then
        self.assertEqual(result, """    /**
     * Just a summary.
     *
     * @return string just a return value
     *
     * @see something
     * @see or nothing
     */""")

    def test_links(self):
        # when
        result = self._print_method(links=['some link', 'other link'])

        # then
        self.assertEqual(result, """    /**
     * Just a summary.
     *
     * @return string just a return value
     *
     * @link some link
     * @link other link
     */""")

    def test_preg_method(self):
        # when
        result = format_preg_method('some_name')

        # then
        self.assertEqual(result, "preg::some_name()")

    def test_optional_and_ref_parameters(self):
        # when
        result = self._print_method(param={
            'first': {'type': 'int', 'optional': True},
            'second': {'type': 'int', 'ref': True},
            'both': {'type': 'int', 'optional': True, 'ref': True},
        }, param_mapper=lambda param: '!' + param + '!')

        # then
        self.assertEqual(result, """    /**
     * Just a summary.
     *
     * @param int $first [optional] !first!
     * @param int &$second [reference] !second!
     * @param int &$both [optional, reference] !both!
     *
     * @return string just a return value
     */""")

    def test_params_multiline(self):
        # when
        result = self._print_method(
            param={'first': {'type': 'int'}, 'second': {'type': 'int'}, },
            param_mapper=lambda param: '!' + param + '!\nFoo\nBar\nLorem')

        # then
        self.assertEqual(result, """    /**
     * Just a summary.
     *
     * @param int $first !first!
     * Foo
     * Bar
     * Lorem
     * @param int $second !second!
     * Foo
     * Bar
     * Lorem
     *
     * @return string just a return value
     */""")

    def test_params_single_line(self):
        # when
        result = self._print_method(
            param={'first': {'type': 'int'}, 'second': {'type': 'int'}},
            param_mapper=lambda x: 'Foo')

        # then
        self.assertEqual(result, """    /**
     * Just a summary.
     *
     * @param int $first Foo
     * @param int $second Foo
     *
     * @return string just a return value
     */""")

    def test_param_empty(self):
        # when
        result = self._print_method(param={'first': {'type': 'int'}, 'second': {'type': 'int'}, },
                                    param_mapper=lambda param: '')

        # then
        self.assertEqual(result, """    /**
     * Just a summary.
     *
     * @param int $first
     * @param int $second
     *
     * @return string just a return value
     */""")

    def test_ignore_empty_definition(self):
        # when
        result = self._print_method(definition='',
                                    method_mapper=lambda: self.fail("Failed to assert that file definition is called"))

        # then
        self.assertEqual(result, """    /**
     * @return string just a return value
     */""")

    @staticmethod
    def _print_method(name='str_replace',
                      definition='Just a summary',
                      param=None,
                      _return=None,
                      return_type=None,
                      see=None,
                      links=None,
                      param_mapper=lambda x: x,
                      method_mapper=lambda: '',
                      throws=None,
                      include_template=False):
        return print_method(
            details={
                'name': name,
                'definition': definition,
                'param': param or {},
                'return': _return or 'just a return value',
                'return-type': return_type or 'string',
                'see': see or [],
                'link': links or [],
                'throws': throws or []
            },
            format_method=lambda x: x,  # untested stuffs
            param_mapper=param_mapper,
            definition_fallback=method_mapper,  # untested stuffs
            include_template_tag=include_template,
            indent=4)
