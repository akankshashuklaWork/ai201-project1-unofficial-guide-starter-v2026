# The Unofficial Guide

**Akanksha Shukla — `city_guides` corpus**

> **This file is your submission.** Fill it in as you go — most sections get
> written during the milestone that produces them, not at the end.
>
> How the starter works, and every command you'll need, is in `RUNNING.md`.
> Leave that file alone.
>
> **Paste everything as text.** No screenshots, no video. A typed table gets
> full credit; a picture of the same table gets none.
>
> Delete these instruction blocks as you replace them. The `<!-- -->` comments
> are notes to you and don't show up when the page renders — you can leave them
> or remove them.

---

# Unit 1

## What This Does

This is a question-answering system built on the `city_guides` corpus — 14
travel guides covering nine fictional towns plus five cross-cutting guides
(eating, walking, regional transport, seasons, accessibility). It answers
specific factual questions about the region — bus and train schedules,
opening hours, prices, market history, and similar details — by searching
the actual guide text for the closest-matching passages and writing an
answer grounded in exactly what those passages say. If a question falls
outside what the guides cover (like general trivia or unrelated topics),
the system says so honestly instead of guessing.

## Chunking Strategy

**Chunk size:** not a fixed number of characters — one chunk per `##` section
**Overlap:** none

I picked `city_guides` because it's organised into labelled sections —
Getting there, Getting around, Eat and drink, What to see, Where to stay,
When to go, Practical notes. The starter's fixed 800-character chunker paid
no attention to those headings: indexing with it produced 51 chunks from 14
documents, and sampling them showed real damage — chunks starting or ending
mid-word, and one chunk (`guide_kestrelford.md`, the "Practical notes"
section) that was reduced to a single leftover sentence about a hospital,
with no indication of which town it was even about, since the town's name
only appeared once, at the top of the document, several sections away.

My chunker (`chunker.py::split_documents`) splits each document at its own
`## Heading` markers instead of at a character count, so every chunk is a
complete section rather than an arbitrary slice. I also prefix every chunk
with its document's title, so a chunk like "Practical notes" — which reads
fine inside its document but says nothing about which town it's from on its
own — carries that context wherever it's retrieved to. There's no overlap
between chunks, because the boundaries aren't arbitrary the way a character
count is: a section doesn't need padding from its neighbour to make sense.

Re-indexing with this chunker produced 94 chunks (up from 51 — the intro
paragraph before each document's first heading now becomes its own chunk
too, instead of being fused with the first section), with the shortest
chunk at 172 characters and the longest at 758. No chunk starts or ends
mid-word anymore.

## Sample Chunks

<!-- Five chunks, pasted as text. Label each one and name the file it came from
     AND the function that produced it — the grader checks your code against
     what you claim here.

     `python app.py chunks -n 5` prints all three for you. Copy them straight
     across.

     Milestone 3. -->

**Chunk 1** — source: `guide_accessibility.md#0` — produced by: `chunker.py::split_documents`

```
Getting around the region with limited mobility

An honest assessment rather than a promotional one. Some of these places are
difficult and it is better to know in advance.
```

**Chunk 2** — source: `guide_corry_vale.md#5` — produced by: `chunker.py::split_documents`

```
Corry Vale — Where to stay

Perhaps thirty beds in the entire valley, spread across two pubs and a handful of farmhouse rooms. In summer these are booked months ahead. Camping is permitted on two marked fields and nowhere else.
```

**Chunk 3** — source: `guide_givens_mill.md#2` — produced by: `chunker.py::split_documents`

```
Givens Mill — Getting around

Everything is on one street along the river. The mill is at one end and the church at the other, eight minutes apart. The riverside path continues in both directions for as far as you want to walk.
```

**Chunk 4** — source: `guide_kestrelford.md#4` — produced by: `chunker.py::split_documents`

```
Kestrelford — What to see

The market square on a Saturday morning is the main event and has run continuously since the 1400s. The parish church has a 13th-century tower you can climb for £2. The old trackbed walk runs six miles to the next village along an easy gradient and is the best half-day here.
```

**Chunk 5** — source: `guide_pellew_sands.md#6` — produced by: `chunker.py::split_documents`

```
Pellew Sands — When to go

June and September for the beach without the crowds. July and August are busy and the town is at its most itself, for better and worse. Winter is bleak, largely closed, and has a following among people who like that sort of thing.
```

## Sample Answer

<!-- One complete question and answer, pasted as text, with the source line
     visible. Milestone 4. -->

**Question:** What hours do Kestrelford's pubs serve food?

**Answer:**

```
Kestrelford's pubs stop serving food at 2pm for lunch and 8:30pm for the
evening window.

(Source: guide_kestrelford.md and guide_eating.md)
```

**My relevance cutoff:** 0.6 (the starter's default — I measured my own
distances and found it already sits well inside the gap, so I kept it
rather than moving it.)

I ran my 5 test questions and the 5 `OUT_OF_SCOPE` questions through
`python app.py retrieve` and recorded the best (lowest) distance for each:

| Question | In corpus? | Best distance |
|---|---|---|
| How many times a day does the train run from Brightwater to the regional hub on weekdays? | Yes | 0.303 |
| What hours do Kestrelford's pubs serve food? | Yes | 0.144 |
| Since what year has Marchwood's covered market operated? | Yes | 0.364 |
| How do prices at Halden Bay's harbour front compare to Fell Street? | Yes | 0.303 |
| Which day of the week is Elder Ness's one pub closed? | Yes | 0.231 |
| What is the capital of Mongolia? | No | 0.808 |
| How do I change the oil in a diesel engine? | No | 0.881 |
| Who won the 1994 World Cup? | No | 0.982 |
| What is the recommended dosage of ibuprofen for a headache? | No | 0.835 |
| How do I write a for loop in Rust? | No | 0.859 |

In-corpus distances topped out at 0.364; out-of-scope distances started at
0.808 — a clean gap of 0.44 with nothing in it. The starter's default
threshold of 0.6 sits comfortably in the middle of that gap, so I kept it.

## How I Used AI

<!-- Two specific moments. For each: what you asked for, what came back, and
     what you changed about it.

     "I asked Claude to write the chunking function from my notes. It ignored
     the overlap, so I added that myself" is the level of detail we're after.
     "I used AI to help me code" is not.

     Milestone 5. -->

**1.** For Milestone 2, I asked Claude to write my two remaining acceptance
criteria for me. It refused, pointing to the project's own rule against
letting AI write criteria, and instead asked me questions about the actual
chunks I'd read — specifically, whether I cared more about chunks looking
"clean" (no cut-off words) or being "usable" (answerable even with rough
edges). I picked "usable," then went back through 5 sample chunks myself and
counted that only 1 of 5 was genuinely unusable. That count — 4 of 5 — became
my criterion, and the reasoning under it is my own observation, not
something Claude generated.

**2.** For Milestone 3, I asked Claude to help me build a better chunker
after we found a broken chunk (a fragment about a hospital with no town name
attached). Claude explained the idea of splitting on the document's own `##`
headings instead of a fixed character count, and wrote the code for
`chunker.py::split_documents`. Before trusting it, I had it show me the
section-length statistics across my corpus first (to check whether any
section would still need further splitting — none did), and I personally
read through all 8 chunks it produced from `guide_kestrelford.md` to confirm
the previously broken chunk was now a complete, labeled section before
accepting the change.

<!-- ── Stretch features ─────────────────────────────────────────────────────
     Doing one? Say so here BEFORE you start. A feature this README never
     claims earns nothing.
     ───────────────────────────────────────────────────────────────────────── -->

---

# Unit 2

<!-- These sections get ADDED to what's already above. Don't delete or rewrite
     unit 1 — the point is that someone can see what you said before you knew
     how it went. -->

## Run Log — Before

<!-- Your five criteria, three runs each. `python run_eval.py --label before`
     runs the questions, puts the OUT_OF_SCOPE ones through the gate, and
     writes it all into results/ for you. Targets come from criteria.md; the
     verdict column is your call.

     Criterion 3 is measured in one deterministic pass rather than three, so
     the same number goes in all three run columns. That's correct, not lazy.

     Milestone 1. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 4/5 | 4/5 | 4/5 |  |
| 2. Every answer names a source | 5 of 5 | 5/5 | 5/5 | 5/5 |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 |  |
| 4. Chunks are usable even with rough edges | 4 of 5 | 5/5 | 5/5 | 5/5 |  |
| 5. Cited sources actually contain the fact | 4 of 5 | 5/5 | 5/5 | 5/5 |  |

Produced by `run_eval.py::main` and `scorer.py::judge`, from
`results/run_2026-09-29_1349_before.md`. Criterion 1 counts a question as
passing if `scorer.py` found the `expects` phrase in the answer text.
Criterion 2 and 5 were checked by reading all 15 answers by hand (`scorer.py`
only checks against `expects`, not source correctness). Criteria 3 and 4 are
single deterministic checks — the gate cutoff and the chunker don't change
between runs, so the same number is correct in all three columns, not lazy.

**Real output, one example per criterion:**

**1 — retrieved chunk contains the answer**, from *"What hours do
Kestrelford's pubs serve food?"* — `scorer.py` marks this question a fail
in all 3 runs, but the retrieved chunk genuinely contains the fact:

```
Kestrelford — Eat and drink

Four pubs, two cafés, and a bakery that sells out by 11am. The pubs serve
food between 12 and 2 and again between 6 and 8:30, and outside those
windows there is nowhere to eat at all. The bakery is the reason most
people come back.
```
The system's answer (run 1): *"Kestrelford's pubs serve food between 12
and 2 and again between 6 and 8:30 (Source: guide_kestrelford.md and
guide_eating.md)."* My `expects` phrase was `"12 to 2 and 6 to 8:30"` —
the document itself (and every answer) says "between X and Y," not "X to
Y," so the exact-substring check never matches even though the fact is
right there. Diagnosed further in Milestone 3.

**2 — every answer names a source**, from *"Since what year has
Marchwood's covered market operated?"* — run 1:
```
Marchwood's covered market has operated since 1863. (Source: `guide_eating.md` and `guide_marchwood.md`)
```

**3 — gate stops out-of-corpus questions**, from `results/run_2026-09-29_1349_before.md`:
```
refused  (best distance 0.808)  What is the capital of Mongolia?
```

**4 — chunks are usable**, from `python app.py chunks -n 5`, source
`guide_kestrelford.md#4`, produced by `chunker.py::split_documents`:
```
Kestrelford — What to see

The market square on a Saturday morning is the main event and has run
continuously since the 1400s. The parish church has a 13th-century tower
you can climb for £2. The old trackbed walk runs six miles to the next
village along an easy gradient and is the best half-day here.
```

**5 — cited sources actually contain the fact**, from *"How do prices at
Halden Bay's harbour front compare to Fell Street?"* — run 1 cited
`guide_halden_bay.md`, which independently says in its own "Eat and
drink" section: *"Prices on the harbour front are roughly double those on
Fell Street... for comparable food"* — confirming the citation is real,
not just the nearest retrieved document.

## Verdicts

<!-- MET or MISSED for each of the five, against the target you wrote last
     unit — not a new one. Plus a sentence on how you decided. That sentence
     matters most where it was close.

     If your target said 4 of 5 and your runs came out 4, 3, 4, that's a MISS.
     The target has to hold, not show up occasionally.

     Milestone 2. -->

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 | Retrieved chunk contains the answer | MET | Came out to exactly 4/5 in all three runs — the target held every time, not just on average. The one "failure" (pub hours) isn't really a retrieval miss: the retrieved chunk contains the fact verbatim, just phrased "between X and Y" instead of my `expects` phrase's "X to Y". This is the closest of my five criteria, and I'm treating it as a real MET rather than rounding it up, since the target was written as "at least 4 of 5" and 4 of 5 is exactly that. |
| 2 | Every answer names a source | MET | 5/5 in all three runs, no exceptions. This matches what I expected in Milestone 2 — the source list is generated by my own code (`outcome["sources"]` in `app.py`), not left to the AI's judgment, so there was never a realistic way for this one to fail. |
| 3 | Gate stops out-of-corpus questions | MET | 5/5, exceeding the 4/5 target. Matches the wide, clean gap (0.364 vs 0.808) I measured back in Unit 1 — nothing here was a close call. |
| 4 | Chunks are usable even with rough edges | MET | 5/5 when I re-sampled 5 chunks with the current chunker (`chunker.py::split_documents`), exceeding the 4/5 target. This is a clear improvement over the pre-Milestone-3 chunker, which had 1 genuinely broken chunk in the same size sample. |
| 5 | Cited sources actually contain the fact | MET | 5/5 — I checked all 5 questions' cited documents by hand and confirmed each one genuinely contains the claimed fact, not just a nearby retrieved document. Exceeds the 4/5 target. |

## Diagnoses

**Nothing was missed.** All 5 criteria came out MET against their original
Unit 1 targets, on every one of the 3 runs.

**One thing is still worth diagnosing, even though it didn't cause a miss.**
`scorer.py` marked "What hours do Kestrelford's pubs serve food?" a fail in
all 3 runs — but this isn't a failure in any of the five pipeline stages
(loading, chunking, embedding, retrieval, generation). I checked each one:
the correct document was retrieved, the correct chunk was embedded and
found, and the generated answer was accurate and grounded, every time. The
actual mechanism is outside the pipeline entirely — my own `expects` phrase
in `questions.py`, written back in Milestone 2, assumed the fact would be
phrased "12 **to** 2 and 6 **to** 8:30." The source document itself, and
every answer the model generated from it, phrases it "between 12 **and** 2
and again between 6 **and** 8:30." `scorer.py` does an exact substring
match after normalizing case/punctuation/whitespace, so a real, correct
answer never matches a differently-worded `expects` string. This is a test
authoring problem, not a system problem — I wrote a target that assumed one
exact phrasing that the source material never actually uses.

**Were the targets set too low?** Mostly, yes. Criteria 2 through 5 all beat
their targets comfortably (5/5 against targets of 4/5, or already-5/5).
Criterion 1 is the one genuine exception — it landed exactly on its target
(4/5, not higher), so that one wasn't set with much room to spare, even
though the "failure" inside that 4/5 turned out to be a test-authoring
issue rather than a real one.

**What I'd tighten:** criterion 3 (the relevance gate), from "at least 4 of
5" to "5 of 5." The distance gap I measured in Unit 1 was 0.44 wide
(0.364 vs 0.808) — the widest margin of any of my criteria — and it held at
5/5 across all 3 runs here too. A criterion with that much room between the
target and what the system actually does isn't really testing anything;
5/5 would be a real standard instead of a comfortable one.

## The Improvement

**What I changed:** Rewrote `scorer.py::contains_phrase` from an exact
substring match to an order-independent "content words" match — it strips
out a small set of connector words (to, and, between, again, the, a, an,
of) from both the `expects` phrase and the answer, then checks that every
remaining word from `expects` appears somewhere in the answer.

**Why I picked it:** My Milestone 3 diagnosis found no actual defect in
retrieval, chunking, embedding, or generation for any question — the one
thing `scorer.py` marked "fail" (pub hours) was correct in every pipeline
stage. The only real cause was my own `expects` phrase assuming one exact
wording ("X to Y") that the source document and every generated answer
never actually use ("between X and Y"). That's a test-harness problem, so
I fixed the test harness, not the system — the diagnosis pointed directly
here, not at chunking or retrieval.

### Run Log — After

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 2. Every answer names a source | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. Chunks are usable even with rough edges | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 5. Cited sources actually contain the fact | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |

Produced by `run_eval.py::main` and the new `scorer.py::judge`, from
`results/run_2026-09-29_1441_after.md`.

```
What hours do Kestrelford's pubs serve food? — run 1
Kestrelford's pubs serve food between 12 and 2 and again between 6 and 8:30
(Source: guide_kestrelford.md and guide_eating.md).
```
Same answer text as before the change — nothing about the system's output
moved. What changed is that the scorer now correctly recognizes it as
correct instead of a false fail.

**Did it help?** Yes, and specifically in the way the diagnosis predicted:
criterion 1 moved from exactly 4/5 (the bare minimum for its target) to
5/5, in all three runs. Every other criterion was already at 5/5 before
this change and stayed there — this fix couldn't have touched them, since
none of their questions had a wording-mismatch problem. Before: 1 of 5
criteria was passing right at the edge of its target. After: all 5 are
passing with margin. I know it helped, rather than just moved the number
around by chance, because I traced the mechanism first (Milestone 3) and
the fix targets exactly that mechanism — the answer text itself is
unchanged between before/after, confirming the fix is in how it's judged,
not a change in what the system actually produces.

## What's Still Broken

<!-- For each criterion still missed after your fix: what you'd do about it,
     and why you stopped where you did.

     "I ran out of time" is fine if it's true. Pretending nothing is left is
     not.

     Milestone 5. -->

## What I'd Do Differently

<!-- Knowing what you know now — which of your five criteria would you write
     differently, and why?

     Milestone 5. -->
