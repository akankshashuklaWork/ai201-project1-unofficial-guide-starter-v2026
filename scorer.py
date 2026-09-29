"""
Judges whether an answer is correct.

`run_eval.py` looks for a function here called `judge`, with this exact
shape: `judge(question, expects, answer, results) -> bool`. If it finds
one, the Run columns in results/ carry real pass/fail verdicts instead of
blanks.

Unit 2 Milestone 4 improvement: the original version required the exact
`expects` phrase to appear as one contiguous substring. That broke on
"What hours do Kestrelford's pubs serve food?" — expects "12 to 2 and 6
to 8:30", but the source document (and every answer generated from it)
phrases the same fact "between 12 and 2 and again between 6 and 8:30".
Same fact, different connecting words, so the exact-phrase check never
matched. The fix: strip out a small set of connector words that don't
carry the actual fact, then check that every remaining word from
`expects` shows up somewhere in the answer, in any order. This still
requires the real content (numbers, names) to be present — it just stops
demanding one specific sentence structure.
"""

import re

# Connector words that can vary in phrasing without changing the fact.
# Deliberately small and generic — not tuned to any one question.
_CONNECTORS = {"to", "and", "between", "again", "the", "a", "an", "of"}


def normalize(text: str) -> str:
    """Lowercase, strip punctuation, collapse whitespace."""
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def content_words(text: str) -> set[str]:
    """Normalized words from `text`, minus connector words that carry no fact."""
    return {word for word in normalize(text).split() if word not in _CONNECTORS}


def contains_phrase(answer: str, expects: str) -> bool:
    """Does every content word in `expects` show up somewhere in `answer`?

    Order-independent on purpose: "12 to 2 and 6 to 8:30" and "between 12
    and 2 and again between 6 and 8:30" carry the same four numbers in the
    same order, just connected differently. Checking presence rather than
    exact sequence catches that without accepting genuinely different facts,
    since the numbers/names themselves still all have to be there.
    """
    expected = content_words(expects)
    if not expected:
        return False
    return expected.issubset(content_words(answer))


def judge(question: str, expects: str, answer: str, results) -> bool:
    """The function run_eval.py calls. True = correct, False = wrong."""
    return contains_phrase(answer, expects)
