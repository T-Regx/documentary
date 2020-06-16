<?php
namespace TRegx\CleanRegex;

use TRegx\CleanRegex\ForArray\ForArrayPattern;
use TRegx\CleanRegex\ForArray\ForArrayPatternImpl;
use TRegx\CleanRegex\Internal\InternalPattern;
use TRegx\CleanRegex\Internal\Subject;
use TRegx\CleanRegex\Match\MatchPattern;
use TRegx\CleanRegex\Remove\RemoveLimit;
use TRegx\CleanRegex\Remove\RemovePattern;
use TRegx\CleanRegex\Replace\NonReplaced\DefaultStrategy;
use TRegx\CleanRegex\Replace\NonReplaced\ReplacePatternFactory;
use TRegx\CleanRegex\Replace\ReplaceLimit;
use TRegx\CleanRegex\Replace\ReplaceLimitImpl;
use TRegx\CleanRegex\Replace\ReplacePatternImpl;
use TRegx\CleanRegex\Replace\SpecificReplacePatternImpl;
use TRegx\SafeRegex\preg;

/**
 * {@documentary::class}
 */
class Pattern
{
    /** @var InternalPattern */
    private $pattern;

    private function __construct(InternalPattern $pattern)
    {
        $this->pattern = $pattern;


    /**
     * {documentary:prepare}
     */
    public static function prepare(array $input, string $flags = ''): Pattern
    {
        return PatternBuilder::builder()->prepare($input, $flags);
    }
}
