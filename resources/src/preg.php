<?php
namespace TRegx\SafeRegex;

use TRegx\SafeRegex\Constants\PregConstants;
use TRegx\SafeRegex\Exception\CompileSafeRegexException;
use TRegx\SafeRegex\Exception\MalformedPatternException;
use TRegx\SafeRegex\Exception\RuntimeSafeRegexException;
use TRegx\SafeRegex\Exception\SafeRegexException;
use TRegx\SafeRegex\Exception\SuspectedReturnSafeRegexException;
use TRegx\SafeRegex\Guard\GuardedExecution;
use TRegx\SafeRegex\Guard\Strategy\PregFilterSuspectedReturnStrategy;
use TRegx\SafeRegex\Guard\Strategy\PregReplaceSuspectedReturnStrategy;
use TRegx\SafeRegex\Guard\Strategy\SilencedSuspectedReturnStrategy;

class preg
{
    /**
     * {@template:match}
     * 
     * Performs a single regular expression match. Retrieves only the first matched occurrence.
     * 
     * @param string $pattern  
     * <p>A delimited pattern to search for, with optional flags.</p>
     * 
     * Examples of delimited patterns with flags:
     * <ul>
     *     <li>/^[a-z]+$/m</li>
     *     <li>#https?://(www\.)?\.[a-z]+\.[a-z]+#i</li>
     * </ul>
     * 
     * Available flags:
     * <ul>
     *     <li>i (case insensitive) - If this modifier is set, letters in the pattern match both upper and lower case
     *         letters.
     *     </li>
     *     <li>m (multiline) - By default, PCRE treats the subject string as consisting of a single "line" of characters (even
     *         if it actually contains several newlines). The "start of line" metacharacter (^) matches only at the start of
     *         the string, while the "end of line" metacharacter ($) matches only at the end of the string, or before a
     *         terminating newline (unless D modifier is set). This is the same as Perl. When this modifier is set, the "start
     *         of line" and "end of line" constructs match immediately following or immediately before any newline in the
     *         subject string, respectively, as well as at the very start and end. This is equivalent to Perl's /m modifier. If
     *         there are no "\n" characters in a subject string, or no occurrences of ^ or $ in a pattern, setting this
     *         modifier has no effect.
     *     </li>
     *     <li>s (dot-all) - If this modifier is set, a dot metacharacter in the pattern matches all characters, including
     *         newlines. Without it, newlines are excluded. This modifier is equivalent to Perl's /s modifier. A negative class
     *         such as [^a] always matches a newline character, independent of the setting of this modifier.
     *     </li>
     *     <li>x (extended) - If this modifier is set, whitespace data characters in the pattern are totally ignored except
     *         when escaped or inside a character class, and characters between an unescaped # outside a character class and
     *         the next newline character, inclusive, are also ignored. This is equivalent to Perl's /x modifier, and makes it
     *         possible to include commentary inside complicated patterns. Note, however, that this applies only to data
     *         characters. Whitespace characters may never appear within special character sequences in a pattern, for example
     *         within the sequence (?( which introduces a conditional subpattern.
     *     </li>
     *     <li>A (anchored) - If this modifier is set, the pattern is forced to be "anchored", that is, it is constrained to
     *         match only at the start of the string which is being searched (the "subject string"). This effect can also be
     *         achieved by appropriate constructs in the pattern itself, which is the only way to do it in Perl.
     *     </li>
     *     <li>D (dollar end-only) - If this modifier is set, a dollar metacharacter in the pattern matches only at the end of
     *         the subject string. Without this modifier, a dollar also matches immediately before the final character if it is
     *         a newline (but not before any other newlines). This modifier is ignored if m modifier is set. There is no
     *         equivalent to this modifier in Perl.
     *     </li>
     *     <li>S (analyze) - When a pattern is going to be used several times, it is worth spending more time analyzing it in
     *         order to speed up the time taken for matching. If this modifier is set, then this extra analysis is performed.
     *         At present, studying a pattern is useful only for non-anchored patterns that do not have a single fixed starting
     *         character.
     *     </li>
     *     <li>U (ungreedy) - This modifier inverts the "greediness" of the quantifiers so that they are not greedy by default,
     *         but become greedy if followed by ?. It is not compatible with Perl. It can also be set by a (?U) modifier
     *         setting within the pattern or by a question mark behind a quantifier (e.g. .*?).
     *         <p>Note:</p>
     *         It is usually not possible to match more than <b>pcre.backtrack_limit</b> characters in ungreedy mode.
     *     </li>
     * </ul>
     * 
     * <p>For a non-delimited pattern, use pattern() or Pattern::of().</p>
     * @param string $subject  
     * @param int $flags [optional]  
     * @param &string[] $matches [optional]  
     * @param &int $offset [optional]  
     * 
     * @return int `1` if the `pattern` matches given `subject`, `0` if it does not
     * 
     * @throws MalformedPatternException
     * @throws RuntimeSafeRegexException
     * @throws SuspectedReturnSafeRegexException
     * @throws CompileSafeRegexException
     * @throws SafeRegexException
     * 
     * @see preg::match_all()
     * @see pattern()
     * @see Pattern::of()
     * @link https://www.php.net/manual/en/function.preg-match.php
     * @link https://t-regx.com/docs/match-first
     */
    public static function match($pattern, $subject, array &$matches = null, $flags = 0, $offset = 0)
    {
        return GuardedExecution::invoke('preg_match', function () use ($offset, $flags, &$matches, $subject, $pattern) {
            return @\preg_match($pattern, $subject, $matches, $flags, $offset);
        });
    }

    /**
     * {@template:match_all}
     * 
     * Performs a global regular expression match.
     * 
     * @param string $pattern  
     * <p>A delimited pattern to search for, with optional flags.</p>
     * 
     * Examples of delimited patterns with flags:
     * <ul>
     *     <li>/^[a-z]+$/m</li>
     *     <li>#https?://(www\.)?\.[a-z]+\.[a-z]+#i</li>
     * </ul>
     * 
     * Available flags:
     * <ul>
     *     <li>i (case insensitive) - If this modifier is set, letters in the pattern match both upper and lower case
     *         letters.
     *     </li>
     *     <li>m (multiline) - By default, PCRE treats the subject string as consisting of a single "line" of characters (even
     *         if it actually contains several newlines). The "start of line" metacharacter (^) matches only at the start of
     *         the string, while the "end of line" metacharacter ($) matches only at the end of the string, or before a
     *         terminating newline (unless D modifier is set). This is the same as Perl. When this modifier is set, the "start
     *         of line" and "end of line" constructs match immediately following or immediately before any newline in the
     *         subject string, respectively, as well as at the very start and end. This is equivalent to Perl's /m modifier. If
     *         there are no "\n" characters in a subject string, or no occurrences of ^ or $ in a pattern, setting this
     *         modifier has no effect.
     *     </li>
     *     <li>s (dot-all) - If this modifier is set, a dot metacharacter in the pattern matches all characters, including
     *         newlines. Without it, newlines are excluded. This modifier is equivalent to Perl's /s modifier. A negative class
     *         such as [^a] always matches a newline character, independent of the setting of this modifier.
     *     </li>
     *     <li>x (extended) - If this modifier is set, whitespace data characters in the pattern are totally ignored except
     *         when escaped or inside a character class, and characters between an unescaped # outside a character class and
     *         the next newline character, inclusive, are also ignored. This is equivalent to Perl's /x modifier, and makes it
     *         possible to include commentary inside complicated patterns. Note, however, that this applies only to data
     *         characters. Whitespace characters may never appear within special character sequences in a pattern, for example
     *         within the sequence (?( which introduces a conditional subpattern.
     *     </li>
     *     <li>A (anchored) - If this modifier is set, the pattern is forced to be "anchored", that is, it is constrained to
     *         match only at the start of the string which is being searched (the "subject string"). This effect can also be
     *         achieved by appropriate constructs in the pattern itself, which is the only way to do it in Perl.
     *     </li>
     *     <li>D (dollar end-only) - If this modifier is set, a dollar metacharacter in the pattern matches only at the end of
     *         the subject string. Without this modifier, a dollar also matches immediately before the final character if it is
     *         a newline (but not before any other newlines). This modifier is ignored if m modifier is set. There is no
     *         equivalent to this modifier in Perl.
     *     </li>
     *     <li>S (analyze) - When a pattern is going to be used several times, it is worth spending more time analyzing it in
     *         order to speed up the time taken for matching. If this modifier is set, then this extra analysis is performed.
     *         At present, studying a pattern is useful only for non-anchored patterns that do not have a single fixed starting
     *         character.
     *     </li>
     *     <li>U (ungreedy) - This modifier inverts the "greediness" of the quantifiers so that they are not greedy by default,
     *         but become greedy if followed by ?. It is not compatible with Perl. It can also be set by a (?U) modifier
     *         setting within the pattern or by a question mark behind a quantifier (e.g. .*?).
     *         <p>Note:</p>
     *         It is usually not possible to match more than <b>pcre.backtrack_limit</b> characters in ungreedy mode.
     *     </li>
     * </ul>
     * 
     * <p>For a non-delimited pattern, use pattern() or Pattern::of().</p>
     * @param string $subject  
     * @param &array[] $matches [optional]  
     * @param int $flags [optional]  
     * @param &int $offset [optional]  
     * 
     * @return int the number of `pattern` matches (which might be zero)
     * 
     * @throws MalformedPatternException
     * @throws RuntimeSafeRegexException
     * @throws SuspectedReturnSafeRegexException
     * @throws CompileSafeRegexException
     * @throws SafeRegexException
     * 
     * @see preg::match()
     * @see pattern()
     * @see Pattern::of()
     * @link https://www.php.net/manual/en/function.preg-match-all.php
     * @link https://t-regx.com/docs/match
     */
    public static function match_all($pattern, $subject, array &$matches = null, $flags = PREG_PATTERN_ORDER, $offset = 0)
    {
        return GuardedExecution::invoke('preg_match_all', function () use ($offset, $flags, &$matches, $subject, $pattern) {
            return @\preg_match_all($pattern, $subject, $matches, $flags, $offset);
        });
    }

    /**
     * {@template:replace}
     * 
     * Performs a regular expression search and replace.
     * 
     * @param string $pattern  
     * <p>A delimited pattern to search for, with optional flags.</p>
     * 
     * Examples of delimited patterns with flags:
     * <ul>
     *     <li>/^[a-z]+$/m</li>
     *     <li>#https?://(www\.)?\.[a-z]+\.[a-z]+#i</li>
     * </ul>
     * 
     * Available flags:
     * <ul>
     *     <li>i (case insensitive) - If this modifier is set, letters in the pattern match both upper and lower case
     *         letters.
     *     </li>
     *     <li>m (multiline) - By default, PCRE treats the subject string as consisting of a single "line" of characters (even
     *         if it actually contains several newlines). The "start of line" metacharacter (^) matches only at the start of
     *         the string, while the "end of line" metacharacter ($) matches only at the end of the string, or before a
     *         terminating newline (unless D modifier is set). This is the same as Perl. When this modifier is set, the "start
     *         of line" and "end of line" constructs match immediately following or immediately before any newline in the
     *         subject string, respectively, as well as at the very start and end. This is equivalent to Perl's /m modifier. If
     *         there are no "\n" characters in a subject string, or no occurrences of ^ or $ in a pattern, setting this
     *         modifier has no effect.
     *     </li>
     *     <li>s (dot-all) - If this modifier is set, a dot metacharacter in the pattern matches all characters, including
     *         newlines. Without it, newlines are excluded. This modifier is equivalent to Perl's /s modifier. A negative class
     *         such as [^a] always matches a newline character, independent of the setting of this modifier.
     *     </li>
     *     <li>x (extended) - If this modifier is set, whitespace data characters in the pattern are totally ignored except
     *         when escaped or inside a character class, and characters between an unescaped # outside a character class and
     *         the next newline character, inclusive, are also ignored. This is equivalent to Perl's /x modifier, and makes it
     *         possible to include commentary inside complicated patterns. Note, however, that this applies only to data
     *         characters. Whitespace characters may never appear within special character sequences in a pattern, for example
     *         within the sequence (?( which introduces a conditional subpattern.
     *     </li>
     *     <li>A (anchored) - If this modifier is set, the pattern is forced to be "anchored", that is, it is constrained to
     *         match only at the start of the string which is being searched (the "subject string"). This effect can also be
     *         achieved by appropriate constructs in the pattern itself, which is the only way to do it in Perl.
     *     </li>
     *     <li>D (dollar end-only) - If this modifier is set, a dollar metacharacter in the pattern matches only at the end of
     *         the subject string. Without this modifier, a dollar also matches immediately before the final character if it is
     *         a newline (but not before any other newlines). This modifier is ignored if m modifier is set. There is no
     *         equivalent to this modifier in Perl.
     *     </li>
     *     <li>S (analyze) - When a pattern is going to be used several times, it is worth spending more time analyzing it in
     *         order to speed up the time taken for matching. If this modifier is set, then this extra analysis is performed.
     *         At present, studying a pattern is useful only for non-anchored patterns that do not have a single fixed starting
     *         character.
     *     </li>
     *     <li>U (ungreedy) - This modifier inverts the "greediness" of the quantifiers so that they are not greedy by default,
     *         but become greedy if followed by ?. It is not compatible with Perl. It can also be set by a (?U) modifier
     *         setting within the pattern or by a question mark behind a quantifier (e.g. .*?).
     *         <p>Note:</p>
     *         It is usually not possible to match more than <b>pcre.backtrack_limit</b> characters in ungreedy mode.
     *     </li>
     * </ul>
     * 
     * <p>For a non-delimited pattern, use pattern() or Pattern::of().</p>
     * @param string|string[] $replacement  
     * @param string|string[] $subject  
     * @param int $limit [optional]  
     * @param &int $count [optional]  
     * 
     * @return string|string[] returns <b>string</b> if `subject` is a `string`, <b>string[]</b> if `subject` is an `array`
     * <ul>
     *  <li>a new string, :with (:unless) if `subject` is a `string`</li>
     *  <li>an array of new strings, all of them :with (:unless) if `subject` is an `array`</li>
     * </ul>
     * 
     * @throws MalformedPatternException
     * @throws RuntimeSafeRegexException
     * @throws SuspectedReturnSafeRegexException
     * @throws CompileSafeRegexException
     * @throws SafeRegexException
     * 
     * @see preg::replace_callback()
     * @see preg::replace_callback_array()
     * @see preg::filter()
     * @see pattern()
     * @see Pattern::of()
     * @link https://www.php.net/manual/en/function.preg-replace.php
     * @link https://t-regx.com/docs/replace-with
     */
    public static function replace($pattern, $replacement, $subject, $limit = -1, &$count = null)
    {
        return GuardedExecution::invoke('preg_replace', function () use ($limit, $subject, $replacement, $pattern, &$count) {
            return @\preg_replace($pattern, $replacement, $subject, $limit, $count);
        }, new PregReplaceSuspectedReturnStrategy($subject));
    }

    /**
     * {@template:replace_callback}
     * 
     * Performs a regular expression search and replace.
     * 
     * @param string $pattern  
     * <p>A delimited pattern to search for, with optional flags.</p>
     * 
     * Examples of delimited patterns with flags:
     * <ul>
     *     <li>/^[a-z]+$/m</li>
     *     <li>#https?://(www\.)?\.[a-z]+\.[a-z]+#i</li>
     * </ul>
     * 
     * Available flags:
     * <ul>
     *     <li>i (case insensitive) - If this modifier is set, letters in the pattern match both upper and lower case
     *         letters.
     *     </li>
     *     <li>m (multiline) - By default, PCRE treats the subject string as consisting of a single "line" of characters (even
     *         if it actually contains several newlines). The "start of line" metacharacter (^) matches only at the start of
     *         the string, while the "end of line" metacharacter ($) matches only at the end of the string, or before a
     *         terminating newline (unless D modifier is set). This is the same as Perl. When this modifier is set, the "start
     *         of line" and "end of line" constructs match immediately following or immediately before any newline in the
     *         subject string, respectively, as well as at the very start and end. This is equivalent to Perl's /m modifier. If
     *         there are no "\n" characters in a subject string, or no occurrences of ^ or $ in a pattern, setting this
     *         modifier has no effect.
     *     </li>
     *     <li>s (dot-all) - If this modifier is set, a dot metacharacter in the pattern matches all characters, including
     *         newlines. Without it, newlines are excluded. This modifier is equivalent to Perl's /s modifier. A negative class
     *         such as [^a] always matches a newline character, independent of the setting of this modifier.
     *     </li>
     *     <li>x (extended) - If this modifier is set, whitespace data characters in the pattern are totally ignored except
     *         when escaped or inside a character class, and characters between an unescaped # outside a character class and
     *         the next newline character, inclusive, are also ignored. This is equivalent to Perl's /x modifier, and makes it
     *         possible to include commentary inside complicated patterns. Note, however, that this applies only to data
     *         characters. Whitespace characters may never appear within special character sequences in a pattern, for example
     *         within the sequence (?( which introduces a conditional subpattern.
     *     </li>
     *     <li>A (anchored) - If this modifier is set, the pattern is forced to be "anchored", that is, it is constrained to
     *         match only at the start of the string which is being searched (the "subject string"). This effect can also be
     *         achieved by appropriate constructs in the pattern itself, which is the only way to do it in Perl.
     *     </li>
     *     <li>D (dollar end-only) - If this modifier is set, a dollar metacharacter in the pattern matches only at the end of
     *         the subject string. Without this modifier, a dollar also matches immediately before the final character if it is
     *         a newline (but not before any other newlines). This modifier is ignored if m modifier is set. There is no
     *         equivalent to this modifier in Perl.
     *     </li>
     *     <li>S (analyze) - When a pattern is going to be used several times, it is worth spending more time analyzing it in
     *         order to speed up the time taken for matching. If this modifier is set, then this extra analysis is performed.
     *         At present, studying a pattern is useful only for non-anchored patterns that do not have a single fixed starting
     *         character.
     *     </li>
     *     <li>U (ungreedy) - This modifier inverts the "greediness" of the quantifiers so that they are not greedy by default,
     *         but become greedy if followed by ?. It is not compatible with Perl. It can also be set by a (?U) modifier
     *         setting within the pattern or by a question mark behind a quantifier (e.g. .*?).
     *         <p>Note:</p>
     *         It is usually not possible to match more than <b>pcre.backtrack_limit</b> characters in ungreedy mode.
     *     </li>
     * </ul>
     * 
     * <p>For a non-delimited pattern, use pattern() or Pattern::of().</p>
     * @param callable $callback  
     * @param string|string[] $subject  
     * @param int $limit [optional]  
     * @param &int $count [optional]  
     * 
     * @return string|string[] returns <b>string</b> if `subject` is a `string`, <b>string[]</b> if `subject` is an `array`
     * <ul>
     *  <li>a new string, :with (:unless) if `subject` is a `string`</li>
     *  <li>an array of new strings, all of them :with (:unless) if `subject` is an `array`</li>
     * </ul>
     * 
     * @throws MalformedPatternException
     * @throws RuntimeSafeRegexException
     * @throws SuspectedReturnSafeRegexException
     * @throws CompileSafeRegexException
     * @throws SafeRegexException
     * 
     * @see preg::replace()
     * @see preg::replace_callback_array()
     * @see preg::filter()
     * @see pattern()
     * @see Pattern::of()
     * @link https://www.php.net/manual/en/function.preg-replace-callback.php
     * @link https://t-regx.com/docs/replace-callback
     */
    public static function replace_callback($pattern, callable $callback, $subject, $limit = -1, &$count = null)
    {
        return GuardedExecution::invoke('preg_replace_callback', function () use ($pattern, $limit, $subject, $callback, &$count) {
            return @\preg_replace_callback($pattern, $callback, $subject, $limit, $count);
        });
    }

    /**
     * {@template:replace_callback_array}
     * 
     * Performs a regular expression search and replace.
     * 
     * @param array $patterns_and_callbacks  
     * @param string|string[] $subject  
     * @param int $limit [optional]  
     * @param &int $count [optional]  
     * 
     * @return string|string[] returns <b>string</b> if the `subject` parameter is a `string`, <b>string[]</b> if the `subject` parameter is an `array`
     * <ul>
     *  <li>unmodified `subject` if it matches the `pattern`, or `null` if it doesn't if the `subject` parameter is a `string`</li>
     *  <li>an array containing only elements matched by the `pattern` if the `subject` parameter is an `array`</li>
     * </ul>
     * 
     * @throws MalformedPatternException
     * @throws RuntimeSafeRegexException
     * @throws SuspectedReturnSafeRegexException
     * @throws CompileSafeRegexException
     * @throws SafeRegexException
     * 
     * @see preg::replace()
     * @see preg::replace_callback()
     * @see preg::filter()
     * @see pattern()
     * @see Pattern::of()
     * @link https://www.php.net/manual/en/function.preg-replace-callback-array.php
     */
    public static function replace_callback_array($patterns_and_callbacks, $subject, $limit = -1, &$count = null)
    {
        return GuardedExecution::invoke('preg_replace_callback_array', function () use ($patterns_and_callbacks, $subject, $limit, &$count) {
            return @\preg_replace_callback_array($patterns_and_callbacks, $subject, $limit, $count);
        });
    }

    /**
     * {@template:filter}
     * 
     * Performs a regular expression search and replace.
     * 
     * @param string|string[] $pattern  
     * <p>A delimited pattern to search for, with optional flags.</p>
     * 
     * Examples of delimited patterns with flags:
     * <ul>
     *     <li>/^[a-z]+$/m</li>
     *     <li>#https?://(www\.)?\.[a-z]+\.[a-z]+#i</li>
     * </ul>
     * 
     * Available flags:
     * <ul>
     *     <li>i (case insensitive) - If this modifier is set, letters in the pattern match both upper and lower case
     *         letters.
     *     </li>
     *     <li>m (multiline) - By default, PCRE treats the subject string as consisting of a single "line" of characters (even
     *         if it actually contains several newlines). The "start of line" metacharacter (^) matches only at the start of
     *         the string, while the "end of line" metacharacter ($) matches only at the end of the string, or before a
     *         terminating newline (unless D modifier is set). This is the same as Perl. When this modifier is set, the "start
     *         of line" and "end of line" constructs match immediately following or immediately before any newline in the
     *         subject string, respectively, as well as at the very start and end. This is equivalent to Perl's /m modifier. If
     *         there are no "\n" characters in a subject string, or no occurrences of ^ or $ in a pattern, setting this
     *         modifier has no effect.
     *     </li>
     *     <li>s (dot-all) - If this modifier is set, a dot metacharacter in the pattern matches all characters, including
     *         newlines. Without it, newlines are excluded. This modifier is equivalent to Perl's /s modifier. A negative class
     *         such as [^a] always matches a newline character, independent of the setting of this modifier.
     *     </li>
     *     <li>x (extended) - If this modifier is set, whitespace data characters in the pattern are totally ignored except
     *         when escaped or inside a character class, and characters between an unescaped # outside a character class and
     *         the next newline character, inclusive, are also ignored. This is equivalent to Perl's /x modifier, and makes it
     *         possible to include commentary inside complicated patterns. Note, however, that this applies only to data
     *         characters. Whitespace characters may never appear within special character sequences in a pattern, for example
     *         within the sequence (?( which introduces a conditional subpattern.
     *     </li>
     *     <li>A (anchored) - If this modifier is set, the pattern is forced to be "anchored", that is, it is constrained to
     *         match only at the start of the string which is being searched (the "subject string"). This effect can also be
     *         achieved by appropriate constructs in the pattern itself, which is the only way to do it in Perl.
     *     </li>
     *     <li>D (dollar end-only) - If this modifier is set, a dollar metacharacter in the pattern matches only at the end of
     *         the subject string. Without this modifier, a dollar also matches immediately before the final character if it is
     *         a newline (but not before any other newlines). This modifier is ignored if m modifier is set. There is no
     *         equivalent to this modifier in Perl.
     *     </li>
     *     <li>S (analyze) - When a pattern is going to be used several times, it is worth spending more time analyzing it in
     *         order to speed up the time taken for matching. If this modifier is set, then this extra analysis is performed.
     *         At present, studying a pattern is useful only for non-anchored patterns that do not have a single fixed starting
     *         character.
     *     </li>
     *     <li>U (ungreedy) - This modifier inverts the "greediness" of the quantifiers so that they are not greedy by default,
     *         but become greedy if followed by ?. It is not compatible with Perl. It can also be set by a (?U) modifier
     *         setting within the pattern or by a question mark behind a quantifier (e.g. .*?).
     *         <p>Note:</p>
     *         It is usually not possible to match more than <b>pcre.backtrack_limit</b> characters in ungreedy mode.
     *     </li>
     * </ul>
     * 
     * <p>For a non-delimited pattern, use pattern() or Pattern::of().</p>
     * @param string|string[] $replacement  
     * @param string|string[] $subject  
     * @param int $limit [optional]  
     * @param &int $count [optional]  
     * 
     * @return string|string[] returns <b>string</b> if the `subject` parameter is a `string`, <b>string[]</b> if the `subject` parameter is an `array`
     * <ul>
     *  <li>unmodified `subject` if it matches the `pattern`, or `null` if it doesn't if the `subject` parameter is a `string`</li>
     *  <li>an array containing only elements matched by the `pattern` if the `subject` parameter is an `array`</li>
     * </ul>
     * 
     * @throws MalformedPatternException
     * @throws RuntimeSafeRegexException
     * @throws SuspectedReturnSafeRegexException
     * @throws CompileSafeRegexException
     * @throws SafeRegexException
     * 
     * @see preg::replace()
     * @see preg::replace_callback()
     * @see preg::replace_callback_array()
     * @see pattern()
     * @see Pattern::of()
     * @link https://www.php.net/manual/en/function.preg-filter.php
     */
    public static function filter($pattern, $replacement, $subject, $limit = -1, &$count = null)
    {
        return GuardedExecution::invoke('preg_filter', function () use ($pattern, $replacement, $subject, $limit, &$count) {
            return @\preg_filter($pattern, $replacement, $subject, $limit, $count);
        }, new PregFilterSuspectedReturnStrategy($subject));
    }

    /**
     * {@template:split}
     * 
     * Splits string by a regular expression.
     * 
     * @param string $pattern  
     * The pattern to search for, as a string.
     * Same here
     * @param string $subject  
     * @param int $limit [optional]  
     * @param int $flags [optional]  
     * 
     * @return string[]|array[] returns <b>string[]</b> by default, <b>array[]</b> if flag `PREG_SPLIT_OFFSET_CAPTURE` is used
     * <ul>
     *  <li>substrings of `subject` split along boundaries matched by `pattern` by default</li>
     *  <li>substrings of `subject` and their offsets if flag `PREG_SPLIT_OFFSET_CAPTURE` is used</li>
     * </ul>
     * 
     * @throws MalformedPatternException
     * @throws RuntimeSafeRegexException
     * @throws SuspectedReturnSafeRegexException
     * @throws CompileSafeRegexException
     * @throws SafeRegexException
     * 
     * @see pattern()
     * @see Pattern::of()
     * @link https://www.php.net/manual/en/function.preg-split.php
     * @link https://t-regx.com/docs/split
     */
    public static function split($pattern, $subject, $limit = -1, $flags = 0)
    {
        return GuardedExecution::invoke('preg_split', function () use ($pattern, $subject, $limit, $flags) {
            return @\preg_split($pattern, $subject, $limit, $flags);
        });
    }

    /**
     * {@template:grep}
     * 
     * Filters array entries that match the pattern.
     * 
     * @param string $pattern  
     * <p>A delimited pattern to search for, with optional flags.</p>
     * 
     * Examples of delimited patterns with flags:
     * <ul>
     *     <li>/^[a-z]+$/m</li>
     *     <li>#https?://(www\.)?\.[a-z]+\.[a-z]+#i</li>
     * </ul>
     * 
     * Available flags:
     * <ul>
     *     <li>i (case insensitive) - If this modifier is set, letters in the pattern match both upper and lower case
     *         letters.
     *     </li>
     *     <li>m (multiline) - By default, PCRE treats the subject string as consisting of a single "line" of characters (even
     *         if it actually contains several newlines). The "start of line" metacharacter (^) matches only at the start of
     *         the string, while the "end of line" metacharacter ($) matches only at the end of the string, or before a
     *         terminating newline (unless D modifier is set). This is the same as Perl. When this modifier is set, the "start
     *         of line" and "end of line" constructs match immediately following or immediately before any newline in the
     *         subject string, respectively, as well as at the very start and end. This is equivalent to Perl's /m modifier. If
     *         there are no "\n" characters in a subject string, or no occurrences of ^ or $ in a pattern, setting this
     *         modifier has no effect.
     *     </li>
     *     <li>s (dot-all) - If this modifier is set, a dot metacharacter in the pattern matches all characters, including
     *         newlines. Without it, newlines are excluded. This modifier is equivalent to Perl's /s modifier. A negative class
     *         such as [^a] always matches a newline character, independent of the setting of this modifier.
     *     </li>
     *     <li>x (extended) - If this modifier is set, whitespace data characters in the pattern are totally ignored except
     *         when escaped or inside a character class, and characters between an unescaped # outside a character class and
     *         the next newline character, inclusive, are also ignored. This is equivalent to Perl's /x modifier, and makes it
     *         possible to include commentary inside complicated patterns. Note, however, that this applies only to data
     *         characters. Whitespace characters may never appear within special character sequences in a pattern, for example
     *         within the sequence (?( which introduces a conditional subpattern.
     *     </li>
     *     <li>A (anchored) - If this modifier is set, the pattern is forced to be "anchored", that is, it is constrained to
     *         match only at the start of the string which is being searched (the "subject string"). This effect can also be
     *         achieved by appropriate constructs in the pattern itself, which is the only way to do it in Perl.
     *     </li>
     *     <li>D (dollar end-only) - If this modifier is set, a dollar metacharacter in the pattern matches only at the end of
     *         the subject string. Without this modifier, a dollar also matches immediately before the final character if it is
     *         a newline (but not before any other newlines). This modifier is ignored if m modifier is set. There is no
     *         equivalent to this modifier in Perl.
     *     </li>
     *     <li>S (analyze) - When a pattern is going to be used several times, it is worth spending more time analyzing it in
     *         order to speed up the time taken for matching. If this modifier is set, then this extra analysis is performed.
     *         At present, studying a pattern is useful only for non-anchored patterns that do not have a single fixed starting
     *         character.
     *     </li>
     *     <li>U (ungreedy) - This modifier inverts the "greediness" of the quantifiers so that they are not greedy by default,
     *         but become greedy if followed by ?. It is not compatible with Perl. It can also be set by a (?U) modifier
     *         setting within the pattern or by a question mark behind a quantifier (e.g. .*?).
     *         <p>Note:</p>
     *         It is usually not possible to match more than <b>pcre.backtrack_limit</b> characters in ungreedy mode.
     *     </li>
     * </ul>
     * 
     * <p>For a non-delimited pattern, use pattern() or Pattern::of().</p>
     * @param array $input  
     * @param int $flags [optional]  
     * 
     * @return array a filtered array indexed using the keys from the `input` array
     * 
     * @throws MalformedPatternException
     * @throws RuntimeSafeRegexException
     * @throws SuspectedReturnSafeRegexException
     * @throws CompileSafeRegexException
     * @throws SafeRegexException
     * 
     * @see preg::grep_keys()
     * @see pattern()
     * @see Pattern::of()
     * @link https://www.php.net/manual/en/function.preg-grep.php
     * @link https://t-regx.com/docs/filter
     */
    public static function grep($pattern, array $input, $flags = 0): array
    {
        return GuardedExecution::invoke('preg_grep', function () use ($flags, $input, $pattern) {
            return @\preg_grep($pattern, $input, $flags);
        }, new SilencedSuspectedReturnStrategy());
    }

    /**
     * {@template:grep_keys}
     * 
     * Filters array entries with keys that match the pattern.
     * 
     * @param string $pattern  
     * <p>A delimited pattern to search for, with optional flags.</p>
     * 
     * Examples of delimited patterns with flags:
     * <ul>
     *     <li>/^[a-z]+$/m</li>
     *     <li>#https?://(www\.)?\.[a-z]+\.[a-z]+#i</li>
     * </ul>
     * 
     * Available flags:
     * <ul>
     *     <li>i (case insensitive) - If this modifier is set, letters in the pattern match both upper and lower case
     *         letters.
     *     </li>
     *     <li>m (multiline) - By default, PCRE treats the subject string as consisting of a single "line" of characters (even
     *         if it actually contains several newlines). The "start of line" metacharacter (^) matches only at the start of
     *         the string, while the "end of line" metacharacter ($) matches only at the end of the string, or before a
     *         terminating newline (unless D modifier is set). This is the same as Perl. When this modifier is set, the "start
     *         of line" and "end of line" constructs match immediately following or immediately before any newline in the
     *         subject string, respectively, as well as at the very start and end. This is equivalent to Perl's /m modifier. If
     *         there are no "\n" characters in a subject string, or no occurrences of ^ or $ in a pattern, setting this
     *         modifier has no effect.
     *     </li>
     *     <li>s (dot-all) - If this modifier is set, a dot metacharacter in the pattern matches all characters, including
     *         newlines. Without it, newlines are excluded. This modifier is equivalent to Perl's /s modifier. A negative class
     *         such as [^a] always matches a newline character, independent of the setting of this modifier.
     *     </li>
     *     <li>x (extended) - If this modifier is set, whitespace data characters in the pattern are totally ignored except
     *         when escaped or inside a character class, and characters between an unescaped # outside a character class and
     *         the next newline character, inclusive, are also ignored. This is equivalent to Perl's /x modifier, and makes it
     *         possible to include commentary inside complicated patterns. Note, however, that this applies only to data
     *         characters. Whitespace characters may never appear within special character sequences in a pattern, for example
     *         within the sequence (?( which introduces a conditional subpattern.
     *     </li>
     *     <li>A (anchored) - If this modifier is set, the pattern is forced to be "anchored", that is, it is constrained to
     *         match only at the start of the string which is being searched (the "subject string"). This effect can also be
     *         achieved by appropriate constructs in the pattern itself, which is the only way to do it in Perl.
     *     </li>
     *     <li>D (dollar end-only) - If this modifier is set, a dollar metacharacter in the pattern matches only at the end of
     *         the subject string. Without this modifier, a dollar also matches immediately before the final character if it is
     *         a newline (but not before any other newlines). This modifier is ignored if m modifier is set. There is no
     *         equivalent to this modifier in Perl.
     *     </li>
     *     <li>S (analyze) - When a pattern is going to be used several times, it is worth spending more time analyzing it in
     *         order to speed up the time taken for matching. If this modifier is set, then this extra analysis is performed.
     *         At present, studying a pattern is useful only for non-anchored patterns that do not have a single fixed starting
     *         character.
     *     </li>
     *     <li>U (ungreedy) - This modifier inverts the "greediness" of the quantifiers so that they are not greedy by default,
     *         but become greedy if followed by ?. It is not compatible with Perl. It can also be set by a (?U) modifier
     *         setting within the pattern or by a question mark behind a quantifier (e.g. .*?).
     *         <p>Note:</p>
     *         It is usually not possible to match more than <b>pcre.backtrack_limit</b> characters in ungreedy mode.
     *     </li>
     * </ul>
     * 
     * <p>For a non-delimited pattern, use pattern() or Pattern::of().</p>
     * @param array $input  
     * @param int $flags [optional]  
     * 
     * @return array a filtered array indexed using the keys from the `input` array
     * 
     * @throws MalformedPatternException
     * @throws RuntimeSafeRegexException
     * @throws SuspectedReturnSafeRegexException
     * @throws CompileSafeRegexException
     * @throws SafeRegexException
     * 
     * @see preg::grep()
     * @see pattern()
     * @see Pattern::of()
     * @link https://t-regx.com/docs/filter#filter-by-keys
     */
    public static function grep_keys($pattern, array $input, $flags = 0): array
    {
        return \array_intersect_key($input, \array_flip(self::grep($pattern, \array_keys($input), $flags)));
    }

    /**
     * {@template:quote}
     * 
     * Quotes regular expression characters.
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
     * @link https://t-regx.com/docs/handling-user-input
     * @link https://www.php.net/manual/en/function.preg-quote.php
     * @link https://t-regx.com/docs/quoting
     */
    public static function quote($string, $delimiter = null): string
    {
        if (\preg_quote('#', null) === '#') {
            return \str_replace('#', '\#', \preg_quote($string, $delimiter));
        }
        return \preg_quote($string, $delimiter);
    }

    /**
     * {@template:last_error}
     * 
     * Returns the error code of the last `preg_*()` method execution (as int).
     * 
     * @return int error code of the last `preg_*()` method execution
     * 
     * @see preg::last_error_constant()
     * @see preg::error_constant()
     * @see pattern()
     * @see Pattern::of()
     * @link https://www.php.net/manual/en/function.preg-last-error.php
     */
    public static function last_error(): int
    {
        /**
         * Please, keep in mind that calling `preg::last_error()`, for `preg::*()` methods, is useless,
         * because `preg::*()` functions never fail with `false`, `null` or by error code
         * of `preg_last_error()` method. So in normal situations, this function will always
         * return `PREG_NO_ERROR`.
         *
         * As for now, this method only use case is for `preg_*()` functions
         */

        // @codeCoverageIgnoreStart
        return \preg_last_error();
        // @codeCoverageIgnoreEnd
    }

    /**
     * {@template:last_error_constant}
     * 
     * Returns the error name of the last `preg_*()` method execution (as string).
     * 
     * @return string error name of the last `preg_*()` method execution
     * 
     * @see preg::last_error()
     * @see preg::error_constant()
     * @see pattern()
     * @see Pattern::of()
     * @link https://www.php.net/manual/en/function.preg-last-error.php
     */
    public static function last_error_constant(): string
    {
        return preg::error_constant(\preg_last_error());
    }

    /**
     * {@template:error_constant}
     * 
     * Returns the error name for a given error code.
     * 
     * @param int $error  
     * 
     * @return string error name of a given error code
     * 
     * @see preg::last_error()
     * @see preg::last_error_constant()
     * @see pattern()
     * @see Pattern::of()
     * @link https://www.php.net/manual/en/function.preg-last-error.php
     */
    public static function error_constant(int $error): string
    {
        return (new PregConstants())->getConstant($error);
    }
}
