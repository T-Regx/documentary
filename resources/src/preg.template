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
     */
    public static function match($pattern, $subject, array &$matches = null, $flags = 0, $offset = 0)
    {
        return GuardedExecution::invoke('preg_match', function () use ($offset, $flags, &$matches, $subject, $pattern) {
            return @\preg_match($pattern, $subject, $matches, $flags, $offset);
        });
    }

    /**
     * {@template:match_all}
     */
    public static function match_all($pattern, $subject, array &$matches = null, $flags = PREG_PATTERN_ORDER, $offset = 0)
    {
        return GuardedExecution::invoke('preg_match_all', function () use ($offset, $flags, &$matches, $subject, $pattern) {
            return @\preg_match_all($pattern, $subject, $matches, $flags, $offset);
        });
    }

    /**
     * {@template:replace}
     */
    public static function replace($pattern, $replacement, $subject, $limit = -1, &$count = null)
    {
        return GuardedExecution::invoke('preg_replace', function () use ($limit, $subject, $replacement, $pattern, &$count) {
            return @\preg_replace($pattern, $replacement, $subject, $limit, $count);
        }, new PregReplaceSuspectedReturnStrategy($subject));
    }

    /**
     * {@template:replace_callback}
     */
    public static function replace_callback($pattern, callable $callback, $subject, $limit = -1, &$count = null)
    {
        return GuardedExecution::invoke('preg_replace_callback', function () use ($pattern, $limit, $subject, $callback, &$count) {
            return @\preg_replace_callback($pattern, $callback, $subject, $limit, $count);
        });
    }

    /**
     * {@template:replace_callback_array}
     */
    public static function replace_callback_array($patterns_and_callbacks, $subject, $limit = -1, &$count = null)
    {
        return GuardedExecution::invoke('preg_replace_callback_array', function () use ($patterns_and_callbacks, $subject, $limit, &$count) {
            return @\preg_replace_callback_array($patterns_and_callbacks, $subject, $limit, $count);
        });
    }

    /**
     * {@template:filter}
     */
    public static function filter($pattern, $replacement, $subject, $limit = -1, &$count = null)
    {
        return GuardedExecution::invoke('preg_filter', function () use ($pattern, $replacement, $subject, $limit, &$count) {
            return @\preg_filter($pattern, $replacement, $subject, $limit, $count);
        }, new PregFilterSuspectedReturnStrategy($subject));
    }

    /**
     * {@template:split}
     */
    public static function split($pattern, $subject, $limit = -1, $flags = 0)
    {
        return GuardedExecution::invoke('preg_split', function () use ($pattern, $subject, $limit, $flags) {
            return @\preg_split($pattern, $subject, $limit, $flags);
        });
    }

    /**
     * {@template:grep}
     */
    public static function grep($pattern, array $input, $flags = 0): array
    {
        return GuardedExecution::invoke('preg_grep', function () use ($flags, $input, $pattern) {
            return @\preg_grep($pattern, $input, $flags);
        }, new SilencedSuspectedReturnStrategy());
    }

    /**
     * {@template:grep_keys}
     */
    public static function grep_keys($pattern, array $input, $flags = 0): array
    {
        return \array_intersect_key($input, \array_flip(self::grep($pattern, \array_keys($input), $flags)));
    }

    /**
     * {@template:quote}
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
     */
    public static function last_error_constant(): string
    {
        return preg::error_constant(\preg_last_error());
    }

    /**
     * {@template:error_constant}
     */
    public static function error_constant(int $error): string
    {
        return (new PregConstants())->getConstant($error);
    }
}
