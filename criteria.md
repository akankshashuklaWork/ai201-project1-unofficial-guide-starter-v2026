# Acceptance criteria — The Unofficial Guide

Five criteria that say what "working" means for this system, written in unit 1
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"Retrieval works"* is an opinion. *"For at
least 4 of my 5 test questions, the top results include a chunk containing the
answer"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter or looser one. A reason that says something about your corpus or your
pipeline earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## 1. Retrieved chunks contain the answer

For at least 4 of my 5 test questions, the retrieved chunks include one that
contains the answer.

**Why this target:**
I checked how close the best matching chunk was for each of my 5 questions.
Lower numbers mean a closer match. My market-year question scored 0.364,
which was the weakest of my five — the others were all closer (0.144 to
0.303). Since I already know that question is my shakiest one, I picked
4 of 5 instead of 5 of 5, so I'm not promising something I already have a
reason to doubt.

---

## 2. Every answer names a source

Every answer the system produces names at least one source document.

**Why this target:**
This criterion says "every answer," so the bar is already 100% (5 of 5),
unlike criteria 1 and 3, which only ask for 4 of 5. Promising 100% is
normally risky, but it's realistic here because naming a source isn't
something the AI could forget to do. In my code (`app.py`, the
`ask_pipeline` function), the source names come from my own Python line —
`outcome["sources"] = sorted({r.source for r in results})` — which runs
automatically every time a question passes the gate. It just collects the
filename of every retrieved chunk. The AI model never decides whether to
include this; my code guarantees it. The only way it could fail is if
retrieval came back with nothing at all, and the relevance gate already
catches that case and refuses before it gets this far.

---

## 3. The relevance gate stops out-of-corpus questions

When I ask a question my documents clearly don't cover, the relevance gate
stops it and the system returns "I don't have enough information about that" —
in at least 4 of 5 tries.

**Why this target:**
I measured the best distance for my 5 real test questions and my 5
OUT_OF_SCOPE questions. In-corpus distances ranged 0.144-0.364; out-of-scope
distances ranged 0.808-0.982. That's a clean gap of 0.44 with nothing in it,
noticeably wider than the 0.45-0.75 range most corpora land in for their
final cutoff — so I kept the starter's default of 0.6, which sits
comfortably in the middle of that gap. I chose "4 of 5" rather than "5 of 5"
because even with a clean gap, a single unusual phrasing could still land
closer to the boundary than these five samples did.

---

## 4. Something about your chunks

When I sample 5 chunks, at least 4 of 5 contain enough intact text to answer
a question on their own, even if the first or last word is cut off at the
chunk boundary.

**Why this target:**
Looking at 5 real chunks from `city_guides`, only 1 (`guide_kestrelford.md#3`)
was genuinely unusable — a single stray sentence about a hospital with no
indication of which town it belonged to. The others had messy edges (a word
cut off) but still contained a complete, answerable thought. I'm targeting
"usable" rather than "cosmetically clean," since a chunk that's slightly
rough at the edges but still answers a question is doing its job.

---

## 5. Your choice

For at least 4 of my 5 test questions, the source(s) named in the answer
actually contain the fact used in the answer — not just any document, but
one that genuinely supports the answer given.

**Why this target:**
Some facts in my corpus appear in more than one document — for example, the
1963 rail line closure is mentioned in both `guide_brightwater.md` and
`guide_regional_transport.md`. I don't require the exact same document every
time, since either one is a legitimate source for that fact. But I do want
most citations to be real, not a document that happens to be nearby in the
results but doesn't actually contain the claim. A wrong citation is worse
than no citation, because it looks trustworthy and isn't.



---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 2 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 1. Retrieved chunks contain the answer

         For at least 4 of my 5 test questions, the retrieved chunks include
         one that contains the answer.

         **Why this target:** ...

         > **Revised in unit 2:** For at least 4 of 5 questions, the top three
         > results contain the answer.
         >
         > **Why revised:** I couldn't judge "the chunks include one that
         > contains the answer" the same way twice — I scored two questions
         > differently on Monday than on Wednesday. The new version is
         > something I can actually check.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said 4 of 5 but got 2 of 5, so 2 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.

     The whole reason the originals stay visible is so someone can see what you
     said before you knew the answer.
     ───────────────────────────────────────────────────────────────────────── -->
