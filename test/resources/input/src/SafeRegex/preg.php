<?php
namespace TRegx\SafeRegex;

use TRegx\SafeRegex\Constants\PregConstants;

interface preg
{
    /**
     * {documentary:match}
     */
    public static function match($pattern, $subject, array &$matches = null, $flags = 0, $offset = 0);

    /**
     * {@documentary:match_all}
     */
    public static function match_all($pattern, $subject, array &$matches = null, $flags = PREG_PATTERN_ORDER, $offset = 0);

    /**
     * @documentary replace
     */
    public static function replace($pattern, $replacement, $subject, $limit = -1, &$count = null);

    /**
     * {documentary:replace_callback}
     */
    public static function replace_callback($pattern, callable $callback, $subject, $limit = -1, &$count = null);

    /**
     * {documentary:replace_callback_array}
     */
    public static function replace_callback_array($patterns_and_callbacks, $subject, $limit = -1, &$count = null);

    private static function decorateCallback(string $methodName, $callback);

    /**
     * {documentary:filter}
     */
    public static function filter($pattern, $replacement, $subject, $limit = -1, &$count = null);

    /**
     * {documentary:split}
     */
    public static function split($pattern, $subject, $limit = -1, $flags = 0);

    /**
     * {documentary:grep}
     */
    public static function grep($pattern, array $input, $flags = 0): array;

    /**
     * {documentary:grep_keys}
     */
    public static function grep_keys($pattern, array $input, $flags = 0): array;

    /**
     * {documentary:quote}
     */
    public static function quote($string, $delimiter = null): string;

    /**
     * {documentary:last_error}
     */
    public static function last_error(): int;

    /**
     * {documentary:last_error_constant}
     */
    public static function last_error_constant(): string;

    /**
     * {documentary:error_constant}
     */
    public static function error_constant(int $error): string;
}
