"""
The relevance gate.

This runs *before* the model does. It looks at how close the best retrieved
chunk actually is, and if nothing came back close enough it refuses the
question outright.

Why this exists as its own step, rather than just asking the model nicely to
admit when it doesn't know: if you only ask nicely, it will sometimes ignore
you and write something confident and wrong. Those answers are much harder to
catch than obvious errors. Deciding in your own code when there's nothing worth
answering from is more reliable than hoping.

You keep the polite instruction too — it's in generate.py — but as a second
layer. The gate catches the clear misses; the prompt catches the near ones.
"""

from dataclasses import dataclass

import config
from store import Result

REFUSAL = "I don't have enough information about that."

# Words that say nothing about whether the corpus covers a topic. Without them,
# "Where can I find fresh seafood?" trips on "find" and gets refused.
STOPWORDS = set("""a an the is are was were do does did i you it there in on at to of for
and or can could would should what when where who how why my me any with from by as
be been have has had this that these those if not find get got go goes going see
know tell look need want like best good better near nearest time open close many
much some all most other new old take give come able around also just only very""".split())


def _words(text: str) -> list[str]:
    """Lowercase word list with punctuation dropped."""
    return "".join(c if c.isalnum() else " " for c in text.lower()).split()


def unsupported_terms(question: str, results: list[Result]) -> list[str]:
    """
    Content words in the question that appear nowhere in the retrieved chunks.

    This is the keyword half of the gate. Distance cannot tell the difference
    between "Where can I go birdwatching?" and "Where is the nearest campsite
    to Elder Ness?" — both retrieve the Elder Ness guide, and both score well
    under the cutoff, because both are *about* Elder Ness. Only one of them has
    an answer in there.

    Matching is prefix-based rather than exact so "birdwatching" counts as
    supported by "bird" and "cafes" by "cafe". Without that, ordinary word
    endings look like missing topics.
    """
    vocabulary = set(_words(" ".join(r.text for r in results)))
    stems = [word for word in vocabulary if len(word) >= 4]

    missing = []
    for word in _words(question):
        if word in STOPWORDS or len(word) <= 2 or word in vocabulary:
            continue
        if any(stem.startswith(word[:4]) or word.startswith(stem) for stem in stems):
            continue
        missing.append(word)
    return missing


@dataclass
class GateDecision:
    passed: bool
    best_distance: float
    threshold: float
    missing_terms: tuple[str, ...] = ()

    @property
    def explanation(self) -> str:
        if self.missing_terms:
            return (
                f"best distance {self.best_distance:.3f} is under the "
                f"{self.threshold} cutoff, but the chunks never mention "
                f"{', '.join(self.missing_terms)} — refusing"
            )
        if self.passed:
            return (
                f"best distance {self.best_distance:.3f} "
                f"is under the {self.threshold} cutoff"
            )
        return (
            f"best distance {self.best_distance:.3f} "
            f"is over the {self.threshold} cutoff — refusing"
        )


def check(
    results: list[Result],
    threshold: float | None = None,
    question: str | None = None,
) -> GateDecision:
    """
    Decide whether the retrieved chunks are close enough to answer from.

    Remember: LOWER distance is better. A question passes when its best chunk
    is *under* the threshold.

    Pass `question` as well and the gate adds a keyword check on top of the
    distance one: a question whose content words appear nowhere in the
    retrieved text is refused even when the distance is good. See
    `unsupported_terms` for why distance on its own is not enough.

    `question` is optional so the older two-argument call still works.
    """
    threshold = config.THRESHOLD if threshold is None else threshold

    if not results:
        return GateDecision(passed=False, best_distance=1.0, threshold=threshold)

    best = min(r.distance for r in results)
    missing = tuple(unsupported_terms(question, results)) if question else ()

    return GateDecision(
        passed=best < threshold and not missing,
        best_distance=best,
        threshold=threshold,
        missing_terms=missing,
    )
