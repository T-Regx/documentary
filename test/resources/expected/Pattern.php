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
 *
 * <p>
 *     Interface representing a match (a result of <b>preg_match()</b> or <b>preg_match_all()</b> method),
 *     that can be used to confidently assert a capturing group existence.
 * </p>
 * <p>With result of:</p>
 * <ul>
 *     <li>
 *         <b>preg_match()</b> (<b>IRawMatch</b>) - it's not possible (because a group can be either missing, or trimmed
 *         by <b>preg_match()</b>). That's why <b>preg_match()</b> is used only for <b>match()->first()</b> without a callback.
 *     </li>
 * </ul>
 * <p>With results of:</p>
 * <ul>
 *     <li><b>preg_match(PREG_UNMATCHED_AS_NULL)</b> - <b>IRawMatchNullable</b></li>
 *     <li><b>preg_match(PREG_OFFSET_CAPTURE)</b> - <b>IRawMatchOffset</b></li>
 *     <li><b>preg_match_all()</b> - <b>IRawMatches</b></li>
 * </ul>
 * <p>...it is possible to assert a capturing group existence - a lack of such group in the results necessarily means
 *     that the group is missing.</p>
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
     *
     * This method returns some prepared pattern.
     *
     * <ul>
     *   <li>Notes:</li>
     *   <li>Don't eat it</li>
     *   <li>Don't send over the network</li>
     * </ul>
     *
     * @param array<int,callable> $input This is some hell of a param. It can use <i>flags</i>, an example
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
