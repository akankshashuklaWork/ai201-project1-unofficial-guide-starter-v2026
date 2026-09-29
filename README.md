# The Unofficial Guide

**Akanksha Shukla — `city_guides` corpus**

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

**3.** (Unit 2) For `scorer.py`, I told Claude the three functions I
wanted — something to clean up text formatting, something to check if my
expected phrase shows up in the answer, and a main function to tie them
together. It read `run_eval.py` first to find the exact interface required
(a function named `judge`, taking four specific arguments, returning
`True`/`False`) rather than guessing, then wrote the three functions to
match. The part that mattered most: I didn't just trust it worked. I ran
it on real questions myself, and that's how I found that the exact-match
approach had a real flaw neither of us had anticipated when describing
what I wanted — it only showed up once I actually used it on real data.

**4.** (Unit 2) When `scorer.py` marked a correct answer as a fail, I
asked Claude to check systematically instead of guessing — going through
each of the five pipeline stages and checking whether that stage was
actually working for this question. It ruled out a real problem at every
stage and traced the cause to my own `expects` phrase from Unit 1, not the
system. Once I understood where the problem actually was, deciding what to
do about it — fix the scorer, not the pipeline — was mine to decide.

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

This table came from `results/run_2026-09-29_1349_before.md`, which I got
by running `python run_eval.py --label before`. That command asks each of
my 5 questions 3 separate times, with caching off so I get 3 real answers
instead of one cached answer repeated. It also runs my 5 `OUT_OF_SCOPE`
questions once each, since those only get compared against a fixed cutoff
(0.6), not repeated.

The run log file has one row per *question*. My README wants one row per
*criterion*. So I went through and counted — for criterion 1, how many of
my 5 questions passed, per run? That's aggregating, not copy-pasting.

How each one got measured:
- **Criterion 1** used `scorer.py` (the program I built — more on it
  below) to check whether my `expects` phrase shows up in the answer.
- **Criteria 2 and 5** aren't things `scorer.py` knows how to check — it
  only compares against `expects`. I read all 15 answers by hand instead.
- **Criteria 3 and 4** don't change between runs. Criterion 3 is a
  comparison against a fixed number, so it gives the same result every
  time. Criterion 4 depends on chunking, which doesn't change just because
  I asked a question three times. Same number in all 3 columns for both —
  that's correct, not lazy.

**Real output, one example per criterion:**

**1 — retrieved chunk contains the answer.** Test question: *"What hours
do Kestrelford's pubs serve food?"* `scorer.py` marked this a fail in all
3 runs. But the chunk that got retrieved actually has the right
information in it — the full story is in Diagnoses below. Here's the
chunk:

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

A verdict just means: did my measured performance hold up to the target I
wrote in Unit 1, before I'd run anything? "MET" means yes, every run — not
on average. If a target said "4 of 5" and my runs came out 4, 3, 4, that's
a MISS, since the target has to hold every time, not just mostly.

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 | Retrieved chunk contains the answer | MET | Target was "at least 4 of 5." All three runs came out to exactly 4/5 — never higher, never lower. The one question that didn't pass (pub hours) isn't really a retrieval problem: the chunk had the right opening hours in it. It only failed because my `expects` phrase said "12 **to** 2 and 6 **to** 8:30," while the real document says "between 12 **and** 2 and again between 6 **and** 8:30." Same fact, different connector word. Since "at least 4 of 5" is literally what I got, I'm calling this MET — but I want it visible that it wasn't a clean 5/5. |
| 2 | Every answer names a source | MET | Target was "5 of 5," and I got exactly that in all 3 runs — all 15 answers named a source. Not surprising: naming a source isn't the AI's call to make. A single line in `app.py` collects the retrieved filenames automatically, every time. |
| 3 | Gate stops out-of-corpus questions | MET | Target was "at least 4 of 5," got 5/5 every run. Matches what I already knew from Unit 1 — the distance gap between real and fake questions was wide (0.364 vs 0.808), so nothing landed in the middle to confuse the gate. |
| 4 | Chunks are usable even with rough edges | MET | Target was "at least 4 of 5," got 5/5 from a fresh sample via `python app.py chunks -n 5`. A real improvement over the old chunker, which had 1 broken chunk in a same-size sample — this sample had none. |
| 5 | Cited sources actually contain the fact | MET | Target was "at least 4 of 5," got 5/5. I opened each cited document myself and confirmed the fact was actually there, not just that a document happened to be nearby in the results. |

## Diagnoses

The instructions for this section say: for each criterion I missed, figure
out which pipeline stage caused it (loading → chunking → embedding →
retrieval → generation) and explain the mechanism, not just "it didn't
work." **Nothing was actually missed** — all 5 criteria came out MET,
holding across all 3 runs. So this section is about a close call that
*looked* like a failure, why it wasn't one, and whether my targets were
actually hard to hit or just easy.

**The near-miss.** `scorer.py` marked "What hours do Kestrelford's pubs
serve food?" a fail in all 3 runs. My first instinct was to assume
something in the pipeline broke. So I checked each stage:

- **Loading** — right document read? Yes.
- **Chunking** — did the pub-hours sentence get cut apart? No, the whole
  "Eat and drink" section came through as one piece.
- **Embedding** — turned into a searchable vector correctly? Yes, based
  on what happened next.
- **Retrieval** — did search actually find this chunk? Yes, every time —
  best distance 0.144, one of the closest matches of any question.
- **Generation** — did the model write a correct answer? Yes, all 3 runs
  said "between 12 and 2 and again between 6 and 8:30," exactly right,
  with the correct source named.

All five stages worked. The real problem is outside the pipeline entirely
— it's in my own test setup. My `expects` phrase said `"12 to 2 and 6 to
8:30"`. The real document — and every answer generated from it — phrases
it "between 12 **and** 2 and again between 6 **and** 8:30." Same fact,
different connector word. `scorer.py` was doing an exact substring match,
so a correct answer worded slightly differently never matched. My pipeline
was never broken. My test was checking for the wrong kind of match.

**Were my targets too easy?** Mostly, yes. Criteria 2 through 5 all beat
their targets comfortably — 5/5 against targets of 4/5 or already-5/5,
every run. Criterion 1 is the exception — it landed exactly on target, not
above it, even though the "miss" inside it wasn't a real system problem.

**What I'd tighten:** criterion 3, from "at least 4 of 5" to "5 of 5." My
Unit 1 distance measurement already showed a 0.44-wide gap between real
questions (worst: 0.364) and fake ones (closest: 0.808) — the widest
margin of any of my criteria. It held at 5/5 here too. A target with that
much spare room isn't testing the edge of anything; it's just confirming
what I already knew was safe.

## The Improvement

**What I changed:** Rewrote one function, `scorer.py::contains_phrase` —
the piece that decides whether an answer counts as correct. The old
version checked whether the *exact* `expects` phrase, as one continuous
piece of text, appeared in the answer. The new version first strips out a
small list of connector words that don't carry the fact ("to," "and,"
"between," "again," "the," "a," "an," "of") from both the `expects` phrase
and the answer, then checks that every remaining word shows up *somewhere*
in the answer, in any order. So "12 to 2 and 6 to 8:30" becomes just the
numbers "12, 2, 6, 8:30" — the check now asks whether those four numbers
are present, not whether the whole sentence matches word for word.

**Why I picked it:** My diagnosis found all five pipeline stages working
correctly for the failing question — the system was retrieving the right
information and writing correct, sourced answers. The only actual problem
was in how I was grading those answers: my `expects` phrase assumed the
word "to," but the real documents consistently use "and" instead. Since
the diagnosis pointed only at this grading mismatch, not at anything in
the pipeline, I made sure my one change targeted exactly that. I didn't
touch chunking, retrieval, or the prompt — nothing pointed at a problem
there.

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

**Did it help?** Yes, in exactly the way I expected before running it —
which is how I know it was a real fix, not a lucky number change. Before:
criterion 1 sat at exactly 4/5, the closest of my five criteria to
actually failing. After: a full 5/5, every run. Nothing else moved, which
makes sense — none of the other four questions had the wording problem, so
there was nothing for this fix to change about them. The clearest proof
it's a real fix: the AI's generated answer text is identical before and
after — same words, same sources. What changed wasn't what the system
said. What changed was how correctly I was able to recognize it was
right.

## What's Still Broken

Technically, nothing — all 5 criteria are MET at 5/5 after my fix. But
"I hit my own targets" isn't the same claim as "there's nothing left to
improve," and I only earned the first one. What's still weak, even though
none of it shows up as a failing number:

- **I only tested 5 questions, and I wrote all 5 myself.** That's a small
  slice of 14 documents and 94 chunks, and since I wrote them, I might have
  unconsciously picked ones I already suspected would work. A trickier
  question I haven't thought of could still fail in a way none of these 5
  would ever catch.
- **None of my 5 questions need two chunks combined to answer.** I don't
  actually know how the system handles a question whose answer is split
  across two sections, because I never wrote one to test it.
- **`scorer.py` is better but still not a real understanding check.** It
  would mark "eleven" and "11" as different words, or miss a correct
  synonym. It compares words on the page, not meaning.

I'm stopping here because the assignment scopes exactly one improvement,
and I made the one my diagnosis pointed at. These aren't things I ran out
of time for — I never attempted them, and I'd want to test all three
before trusting this system with something that mattered more than a
class project.

## What I'd Do Differently

**Criterion 1** — I'd write `expects` as a list of the individual facts
that matter (`["12", "2", "6", "8:30"]`) instead of one exact sentence
fragment. That's basically what my Milestone 4 fix does anyway, just
designed in from the start instead of patched in afterward. I'd never have
gotten the false "fail" if I'd been testing for the actual facts instead of
one specific sentence structure.

**Criterion 3** — I'd set a stricter target from day one: "5 of 5" instead
of "at least 4 of 5." I already had the evidence for it in Unit 1 — a
0.44-wide distance gap with nothing in the middle. I just played it safe
instead of trusting that measurement. Both runs this unit came out 5/5,
which shows the caution wasn't necessary.

**Criterion 2** — I wouldn't change this one. My Unit 1 reasoning — that
naming a source is guaranteed by my own code, not the AI's judgment — held
up exactly as expected: 5/5 in every run, both units. Nothing here needs
revising just for the sake of it.
