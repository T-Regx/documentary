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

class Pattern
{
    /** @var InternalPattern */
    private $pattern;

    private function __construct(InternalPattern $pattern)
    {
        $this->pattern = $pattern;


    /**
     * {documentary:prepare}
     *
     * This method returns some prepared pattern.
     *
     * <ul>
     *   <li>Notes:</li>
     *   <li>Don't eat it</li>
     *   <li>Don't send over the network</li>
     * </ul>
     *
     * @param callable[] $input This is some hell of a param. It can use <i>flags</i>, an example
     * flag is <b>m</b> or <b>D</b>.
     * @param string $flags [optional]
     *
     * @return Pattern
     *
     * @throws BaseException
     * @throws GeneralException
     *
     * @link http://github.com
     * @link http://youtube.com
     */
    public static function prepare(array $input, string $flags = ''): Pattern
    {
        return PatternBuilder::builder()->prepare($input, $flags);
    }
}
