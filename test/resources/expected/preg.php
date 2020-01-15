<?php
namespace TRegx\SafeRegex;

use TRegx\SafeRegex\Constants\PregConstants;

interface preg
{
    /**
     * {@documentary:match}
     *
     * Performs a single regular expression match. Retrieves only the first matched occurrence.
     *
     * @param string $pattern <p>A delimited pattern to search for, with optional flags.</p>
     * @param string $subject
     * @param int $flags [optional]
     * @param string[] &$matches [optional, reference]
     * @param int &$offset [optional, reference]
     *
     * @return int <b>1</b> if the <i>pattern</i> matches given <i>subject</i>, <b>0</b> if it does not
     *
     * @throws MalformedPatternException
     * @throws RuntimeSafeRegexException
     * @throws SuspectedReturnSafeRegexException
     * @throws CompileSafeRegexException
     *
     * @see pattern()
     * @see Pattern::of()
     * @see preg::match_all()
     *
     * @link https://t-regx.com
     * @link https://www.regular-expressions.info/unicode.html
     * @link https://www.php.net/manual/en/function.preg-match.php
     * @link https://t-regx.com/docs/match-first
     */
    public static function match($pattern, $subject, array &$matches = null, $flags = 0, $offset = 0);

    /**
     * {@documentary:match_all}
     *
     * Performs a global regular expression match.
     *
     * @param string $pattern <p>A delimited pattern to search for, with optional flags.</p>
     * @param string $subject
     * @param array[] &$matches [optional, reference]
     * @param int $flags [optional]
     * @param int &$offset [optional, reference]
     *
     * @return int the number of <i>pattern</i> matched occurrences (which might be zero)
     *
     * @throws MalformedPatternException
     * @throws RuntimeSafeRegexException
     * @throws SuspectedReturnSafeRegexException
     * @throws CompileSafeRegexException
     *
     * @see pattern()
     * @see Pattern::of()
     * @see preg::match()
     *
     * @link https://t-regx.com
     * @link https://www.regular-expressions.info/unicode.html
     * @link https://www.php.net/manual/en/function.preg-match-all.php
     * @link https://t-regx.com/docs/match
     */
    public static function match_all($pattern, $subject, array &$matches = null, $flags = PREG_PATTERN_ORDER, $offset = 0);

    /**
     * {@documentary:replace}
     *
     * Performs a regular expression search and replace.
     *
     * @param string $pattern <p>A delimited pattern to search for, with optional flags.</p>
     * @param string|string[] $replacement
     * @param string|string[] $subject
     * @param int $limit [optional] <p>The maximum possible replacements for each pattern in each <i>subject</i> string.</p>
     * <p>A <i>limit</i> of <b>-1</b>, <b>0</b> or <b>NULL</b> means "no limit".</p>
     * @param int &$count [optional, reference] <p>If specified, this variable will be filled with the number of replacements done.</p>
     *
     * @return string|string[] returns <b>string</b> if <i>subject</i> is a <b>string</b>, <b>string[]</b> if <i>subject</i> is an <b>array</b>
     * <ul>
     *  <li>a new string, with replaced occurrences of <i>pattern</i> (unless the <i>pattern</i> wasn't matched, in this case the <i>subject</i> is returned unchanged) if <i>subject</i> is a <b>string</b></li>
     *  <li>an array of new strings, all of them with replaced occurrences of <i>pattern</i> (unless the <i>pattern</i> wasn't matched, in this case the <i>subject</i> is returned unchanged) if <i>subject</i> is an <b>array</b></li>
     * </ul>
     *
     * @throws MalformedPatternException
     * @throws RuntimeSafeRegexException
     * @throws SuspectedReturnSafeRegexException
     * @throws CompileSafeRegexException
     *
     * @see pattern()
     * @see Pattern::of()
     * @see preg::replace_callback()
     * @see preg::replace_callback_array()
     * @see preg::filter()
     *
     * @link https://t-regx.com
     * @link https://www.regular-expressions.info/unicode.html
     * @link https://www.php.net/manual/en/function.preg-replace.php
     * @link https://t-regx.com/docs/replace-with
     */
    public static function replace($pattern, $replacement, $subject, $limit = -1, &$count = null);

    /**
     * {@documentary:replace_callback}
     *
     * Performs a regular expression search and replace.
     *
     * @param string $pattern <p>A delimited pattern to search for, with optional flags.</p>
     * @param callable $callback
     * @param string|string[] $subject
     * @param int $limit [optional] <p>The maximum possible replacements for each pattern in each <i>subject</i> string.</p>
     * <p>A <i>limit</i> of <b>-1</b>, <b>0</b> or <b>NULL</b> means "no limit".</p>
     * @param int &$count [optional, reference] <p>If specified, this variable will be filled with the number of replacements done.</p>
     *
     * @return string|string[] returns <b>string</b> if <i>subject</i> is a <b>string</b>, <b>string[]</b> if <i>subject</i> is an <b>array</b>
     * <ul>
     *  <li>a new string, with replaced occurrences of <i>pattern</i> (unless the <i>pattern</i> wasn't matched, in this case the <i>subject</i> is returned unchanged) if <i>subject</i> is a <b>string</b></li>
     *  <li>an array of new strings, all of them with replaced occurrences of <i>pattern</i> (unless the <i>pattern</i> wasn't matched, in this case the <i>subject</i> is returned unchanged) if <i>subject</i> is an <b>array</b></li>
     * </ul>
     *
     * @throws MalformedPatternException
     * @throws RuntimeSafeRegexException
     * @throws SuspectedReturnSafeRegexException
     * @throws CompileSafeRegexException
     *
     * @see pattern()
     * @see Pattern::of()
     * @see preg::replace()
     * @see preg::replace_callback_array()
     * @see preg::filter()
     *
     * @link https://t-regx.com
     * @link https://www.regular-expressions.info/unicode.html
     * @link https://www.php.net/manual/en/function.preg-replace-callback.php
     * @link https://t-regx.com/docs/replace-callback
     */
    public static function replace_callback($pattern, callable $callback, $subject, $limit = -1, &$count = null);

    /**
     * {@documentary:replace_callback_array}
     *
     * Performs a regular expression search and replace.
     *
     * @param callable[] $patterns_and_callbacks
     * @param string|string[] $subject
     * @param int $limit [optional] <p>The maximum possible replacements for each pattern in each <i>subject</i> string.</p>
     * <p>A <i>limit</i> of <b>-1</b>, <b>0</b> or <b>NULL</b> means "no limit".</p>
     * @param int &$count [optional, reference] <p>If specified, this variable will be filled with the number of replacements done.</p>
     *
     * @return string|string[] returns <b>string</b> if the <i>subject</i> parameter is a <b>string</b>, <b>string[]</b> if the <i>subject</i> parameter is an <b>array</b>
     * <ul>
     *  <li>unmodified <i>subject</i> if it matches the <b>pattern</b>, or <b>null</b> if it doesn't if the <i>subject</i> parameter is a <b>string</b></li>
     *  <li>an array containing only elements matched by the <b>pattern</b> if the <i>subject</i> parameter is an <b>array</b></li>
     * </ul>
     *
     * @throws MalformedPatternException
     * @throws RuntimeSafeRegexException
     * @throws SuspectedReturnSafeRegexException
     * @throws CompileSafeRegexException
     *
     * @see pattern()
     * @see Pattern::of()
     * @see preg::replace()
     * @see preg::replace_callback()
     * @see preg::filter()
     *
     * @link https://t-regx.com
     * @link https://www.regular-expressions.info/unicode.html
     * @link https://www.php.net/manual/en/function.preg-replace-callback-array.php
     */
    public static function replace_callback_array($patterns_and_callbacks, $subject, $limit = -1, &$count = null);

    private static function decorateCallback(string $methodName, $callback);

    /**
     * {@documentary:filter}
     *
     * Performs a regular expression search and replace.
     *
     * @param string|string[] $pattern <p>A delimited pattern to search for, with optional flags.</p>
     * @param string|string[] $replacement
     * @param string|string[] $subject
     * @param int $limit [optional] <p>The maximum possible replacements for each pattern in each <i>subject</i> string.</p>
     * <p>A <i>limit</i> of <b>-1</b>, <b>0</b> or <b>NULL</b> means "no limit".</p>
     * @param int &$count [optional, reference] <p>If specified, this variable will be filled with the number of replacements done.</p>
     *
     * @return string|string[] returns <b>string</b> if the <i>subject</i> parameter is a <b>string</b>, <b>string[]</b> if the <i>subject</i> parameter is an <b>array</b>
     * <ul>
     *  <li>unmodified <i>subject</i> if it matches the <i>pattern</i>, or <b>null</b> if it doesn't if the <i>subject</i> parameter is a <b>string</b></li>
     *  <li>an array containing only elements matched by the <i>pattern</i> if the <i>subject</i> parameter is an <b>array</b></li>
     * </ul>
     *
     * @throws MalformedPatternException
     * @throws RuntimeSafeRegexException
     * @throws SuspectedReturnSafeRegexException
     * @throws CompileSafeRegexException
     *
     * @see pattern()
     * @see Pattern::of()
     * @see preg::replace()
     * @see preg::replace_callback()
     * @see preg::replace_callback_array()
     *
     * @link https://t-regx.com
     * @link https://www.regular-expressions.info/unicode.html
     * @link https://www.php.net/manual/en/function.preg-filter.php
     */
    public static function filter($pattern, $replacement, $subject, $limit = -1, &$count = null);

    /**
     * {@documentary:split}
     *
     * Splits string by a regular expression.
     *
     * @param string $pattern <p>The pattern to search for, as a string.</p>
     * @param string $subject
     * @param int $limit [optional] <p>
     *   If specified, then only substrings up to <i>limit</i> are returned with the rest of the string being placed in the last
     *   substring. A <i>limit</i> of <b>-1</b>, <b>0</b> or <b>NULL</b> means "no limit".
     * </p>
     *
     * <p>
     *   To simply bypass <i>limit</i> parameter and to specify <i>flags</i>, the next parameter, PHP documentation suggests that
     *   <b>null</b> should be used, as an "unspecified" value.
     * </p>
     * @param int $flags [optional]
     *
     * @return string[]|array[] returns <b>string[]</b> by default, <b>array[]</b> if flag <b>PREG_SPLIT_OFFSET_CAPTURE</b> is used
     * <ul>
     *  <li>substrings of <i>subject</i> split along boundaries matched by <i>pattern</i> by default</li>
     *  <li>substrings of <i>subject</i> and their offsets if flag <b>PREG_SPLIT_OFFSET_CAPTURE</b> is used</li>
     * </ul>
     *
     * @throws MalformedPatternException
     * @throws RuntimeSafeRegexException
     * @throws SuspectedReturnSafeRegexException
     * @throws CompileSafeRegexException
     *
     * @see pattern()
     * @see Pattern::of()
     *
     * @link https://t-regx.com
     * @link https://www.regular-expressions.info/unicode.html
     * @link https://www.php.net/manual/en/function.preg-split.php
     * @link https://t-regx.com/docs/split
     */
    public static function split($pattern, $subject, $limit = -1, $flags = 0);

    /**
     * {@documentary:grep}
     *
     * Filters array entries that match the pattern.
     *
     * @param string $pattern <p>A delimited pattern to search for, with optional flags.</p>
     * @param array $input
     * @param int $flags [optional]
     *
     * @return array a filtered array indexed using the keys from the <i>input</i> array
     *
     * @throws MalformedPatternException
     * @throws RuntimeSafeRegexException
     * @throws SuspectedReturnSafeRegexException
     * @throws CompileSafeRegexException
     *
     * @see pattern()
     * @see Pattern::of()
     * @see preg::grep_keys()
     *
     * @link https://t-regx.com
     * @link https://www.regular-expressions.info/unicode.html
     * @link https://www.php.net/manual/en/function.preg-grep.php
     * @link https://t-regx.com/docs/filter
     */
    public static function grep($pattern, array $input, $flags = 0): array;

    /**
     * {@documentary:grep_keys}
     *
     * Filters array entries with keys that match the pattern.
     *
     * @param string $pattern <p>A delimited pattern to search for, with optional flags.</p>
     * @param array $input
     * @param int $flags [optional]
     *
     * @return array a filtered array indexed using the keys from the <i>input</i> array
     *
     * @throws MalformedPatternException
     * @throws RuntimeSafeRegexException
     * @throws SuspectedReturnSafeRegexException
     * @throws CompileSafeRegexException
     *
     * @see pattern()
     * @see Pattern::of()
     * @see preg::grep()
     *
     * @link https://t-regx.com
     * @link https://www.regular-expressions.info/unicode.html
     * @link https://t-regx.com/docs/filter#filter-by-keys
     */
    public static function grep_keys($pattern, array $input, $flags = 0): array;

    /**
     * {@documentary:quote}
     *
     * <p>
     *   Puts a backslash in <i>string</i>, before every character, that is a part of the regular expression
     *   syntax. It's crucial when using a runtime string (which may contain special regex characters)
     *   that needs to matched as a regular expression.
     * </p>
     * <p>The special regular expression characters are: . \ + * ? [ ^ ] $ ( ) { } = ! < > | : - #</p>
     * <p>Note that / is not a special regular expression character.</p>
     * <br>
     * <p>Notes:</p>
     * <ul>
     *   <li>Note, that <b>preg::quote()</b> is not meant to be applied to the $replacement string(s) of <b>preg_replace()</b> etc.</li>
     * </ul>
     *
     * @param string $string
     * @param string $delimiter [optional]
     *
     * @return string the quoted (escaped) string
     *
     * @see Pattern::quote()
     * @see Pattern::unquote()
     * @see PreparedPattern
     * @see pattern()
     * @see Pattern::of()
     *
     * @link https://t-regx.com/docs/handling-user-input
     * @link https://t-regx.com
     * @link https://www.regular-expressions.info/unicode.html
     * @link https://www.php.net/manual/en/function.preg-quote.php
     * @link https://t-regx.com/docs/quoting
     */
    public static function quote($string, $delimiter = null): string;

    /**
     * {@documentary:last_error}
     *
     * Returns the error code of the last <b>preg_*()</b> method execution (as int).
     *
     * @return int error code of the last <b>preg_*()</b> method execution
     *
     * @see pattern()
     * @see Pattern::of()
     * @see preg::last_error_constant()
     * @see preg::error_constant()
     *
     * @link https://t-regx.com
     * @link https://www.regular-expressions.info/unicode.html
     * @link https://www.php.net/manual/en/function.preg-last-error.php
     */
    public static function last_error(): int;

    /**
     * {@documentary:last_error_constant}
     *
     * Returns the error name of the last <b>preg_*()</b> method execution (as string).
     *
     * @return string error name of the last <b>preg_*()</b> method execution
     *
     * @see pattern()
     * @see Pattern::of()
     * @see preg::last_error()
     * @see preg::error_constant()
     *
     * @link https://t-regx.com
     * @link https://www.regular-expressions.info/unicode.html
     * @link https://www.php.net/manual/en/function.preg-last-error.php
     */
    public static function last_error_constant(): string;

    /**
     * {@documentary:error_constant}
     *
     * Returns the error name for a given error code.
     *
     * @param int $error
     *
     * @return string error name of a given error code
     *
     * @see pattern()
     * @see Pattern::of()
     * @see preg::last_error()
     * @see preg::last_error_constant()
     *
     * @link https://t-regx.com
     * @link https://www.regular-expressions.info/unicode.html
     * @link https://www.php.net/manual/en/function.preg-last-error.php
     */
    public static function error_constant(int $error): string;
}
