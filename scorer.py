"""
Judges whether an answer is correct.

`run_eval.py` looks for a function here called `judge`, with this exact
shape: `judge(question, expects, answer, results) -> bool`. If it finds
one, the Run columns in results/ carry real pass/fail verdicts instead of
blanks.

The approach here is plain substring matching: does the `expects` phrase
from questions.py show up somewhere in the answer, once both are cleaned
up so small differences (case, punctuation, extra spaces) don't cause a
false miss?
"""

import re


def normalize(text: str) -> str:
    """Lowercase, strip punctuation, collapse whitespace."""
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def contains_phrase(answer: str, expects: str) -> bool:
    """Does the expected phrase appear in the answer, once both are normalized?"""
    return normalize(expects) in normalize(answer)


def judge(question: str, expects: str, answer: str, results) -> bool:
    """The function run_eval.py calls. True = correct, False = wrong."""
    return contains_phrase(answer, expects)
