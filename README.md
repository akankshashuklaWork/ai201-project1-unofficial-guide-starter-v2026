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

**3.** (Unit 2) Unit 2 asks students to build a `scorer.py` file that can
automatically grade whether an answer is right or wrong, instead of
reading every answer by hand. I already knew, roughly, the three pieces I
wanted: something to clean up text so small differences like capitalization
don't matter, something to check if my expected phrase shows up in the
answer, and a main function to tie it together. I described those three
pieces to Claude by name. Before writing anything, it went and read the
actual `run_eval.py` file to find out exactly what shape my function
needed to be in order for the rest of the project to actually find and use
it — it turned out there's a very specific requirement (a function named
exactly `judge`, taking four particular arguments in order, returning
`True` or `False`) that I wouldn't have known to get right on my own. It
then wrote the three functions to match. Here's the part that mattered
most, though: once I had it, I didn't just assume it worked — I ran my
real evaluation with it, on real questions, and that's how I discovered
that even though the code did exactly what I'd asked it to do, "what I'd
asked for" (an exact word-for-word match) had a real flaw I hadn't
anticipated when I was describing what I wanted. That flaw only became
visible once I actually used the tool on real data, not from just reading
the code.

**4.** (Unit 2) Once I saw `scorer.py` mark a genuinely correct answer as a
"fail," my first instinct was to assume something in my actual system was
broken. Instead of guessing, I asked Claude to help me check systematically
— going through each of the five stages a RAG system goes through (loading
the documents, splitting them into chunks, turning them into searchable
numbers, finding the closest match, and finally writing an answer) and
checking whether that specific stage was working correctly for this one
question. It walked through all five with me, checked the actual retrieved
chunk against the actual answer text, and ruled out a real problem at
every single stage — the fact really was being retrieved and used
correctly. That process pointed the actual cause somewhere neither of us
had first suspected: not in the RAG system at all, but in the `expects`
phrase I myself had written back in Unit 1. Once I understood exactly
where the problem was and why it was happening, deciding what to actually
do about it — improve the scorer's matching logic rather than touch
anything in the real pipeline — was a decision I made myself, based on
that diagnosis.

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

This table came from a file called `results/run_2026-09-29_1349_before.md`,
which I got by running `python run_eval.py --label before` in my terminal.
Here's what that command actually does, in plain terms: it takes each of my
5 questions from `questions.py`, asks my system the same question 3
separate times in a row (with the response cache turned off, so I get 3
real, independently-generated answers instead of the same cached answer
copy-pasted 3 times), and writes down what happened each time. It also asks
all 5 of my `OUT_OF_SCOPE` questions once each, since those only need to be
checked against a fixed number (the 0.6 cutoff), not repeated.

That file has **one row per question** — 5 rows, one per question, each
showing pass/fail for run 1/2/3. But the table my README needs has **one
row per criterion** — 5 rows, one per criterion. So I had to go through and
count: for criterion 1, how many of my 5 questions passed, in each of the 3
runs? That's a different way of slicing the same data, and it's real work,
not copy-pasting one table into another.

Here's how each criterion actually got measured:
- **Criterion 1** used `scorer.py` — a small program I built (more on that
  in the next section) that checks whether my `expects` phrase (the word or
  short phrase I decided in Unit 1 that a correct answer must contain) shows
  up in the system's actual answer text.
- **Criteria 2 and 5** couldn't be checked by `scorer.py`, because it only
  knows how to compare against `expects` — it has no idea what "names a
  source" or "the source is actually correct" means. So for these two, I
  read all 15 answers myself (5 questions × 3 runs) and checked by eye.
- **Criteria 3 and 4** are special: they don't change between runs at all.
  Criterion 3 (the relevance gate) is just comparing a number (the best
  distance found) against a fixed cutoff (0.6) — that comparison gives the
  exact same result every time you run it, since nothing random is
  involved. Criterion 4 (chunk quality) depends only on how my documents get
  chunked, and my chunker doesn't change no matter how many times I ask
  a question. So the same number is correct in all 3 columns for these
  two — that's not me being lazy, it's genuinely how the math works out.

**Real output, one example per criterion:**

**1 — retrieved chunk contains the answer.** My test question here was
*"What hours do Kestrelford's pubs serve food?"* When I ran this through
`scorer.py`, it came back "fail" in all 3 runs. But when I actually went
and looked at the chunk my system retrieved to answer this question, the
correct information is right there in it — I'll explain exactly why the
scorer still said "fail" in the Diagnoses section below, but first, here's
proof the chunk itself is correct:

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

A verdict here just means: did my system's actual, measured performance
hold up to the number I wrote down back in Unit 1, before I'd run anything?
"MET" means yes, in every single run — not just on average. The doc I was
given is strict about this: if my target said "4 of 5" and my 3 runs came
out 4, 3, 4, that would count as a MISS, because the target has to hold
every time, not show up occasionally and then dip below it once. I kept
that rule in mind for every row below.

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 | Retrieved chunk contains the answer | MET | My target from Unit 1 was "at least 4 of 5." All three of my runs came out to exactly 4/5 — not 5/5, but never below 4/5 either, so the target held every single time. The one question that didn't pass (the pub hours question) isn't actually a real retrieval problem — when I went and read the chunk my system pulled back for that question, the correct opening hours were right there in the text. The only reason it got marked "fail" is that my `expects` phrase (the word/phrase I wrote back in Unit 1 that a correct answer has to contain) was worded "12 **to** 2 and 6 **to** 8:30," but the real document — and every answer generated from it — phrases the same fact as "between 12 **and** 2 and again between 6 **and** 8:30." Same numbers, same fact, just a different connecting word. Since 4 of 5 is literally what my target said ("at least 4"), I'm calling this a genuine MET rather than pretending it was actually a perfect run — it wasn't, and I want that to be visible. |
| 2 | Every answer names a source | MET | My target was "5 of 5," the strictest of my five criteria, and all three runs came out exactly 5/5 — every single answer, across all 15 (5 questions × 3 runs), named at least one source document. This isn't surprising to me, because back in Unit 1 I explained why I thought this one would be safe: naming a source isn't something the AI model has to remember to do on its own. My own Python code (a single line in `app.py`) automatically collects the filenames of whatever chunks got retrieved and attaches them to every answer, every time. The AI can't forget to do something that isn't actually its job to do. |
| 3 | Gate stops out-of-corpus questions | MET | My target was "at least 4 of 5," and I got 5/5 in every run — better than I required. This matches something I already knew from Unit 1: when I measured the "distance" (a number that tells you how closely related a question is to what's actually in my documents) for my 5 real questions versus my 5 made-up nonsense questions, there was a big, clean gap between the two groups (0.364 for my worst real question, versus 0.808 for my closest nonsense question). With a gap that wide, I wasn't surprised nothing landed in the middle and confused the system. |
| 4 | Chunks are usable even with rough edges | MET | My target was "at least 4 of 5," and I got 5/5 when I pulled a fresh sample of 5 chunks using `python app.py chunks -n 5` and read through them myself. This is actually a real improvement I can point to: back before I rebuilt my chunker in Unit 1's Milestone 3, the *old* chunker (the one that just cut text every 800 characters, ignoring sentence or paragraph boundaries) produced 1 genuinely broken chunk out of a same-sized sample — a chunk that was just one leftover sentence about a hospital, with no indication of which town it was even talking about. My new chunker, which cuts at each document's own section headings instead, didn't produce a single broken chunk in this sample. |
| 5 | Cited sources actually contain the fact | MET | My target was "at least 4 of 5," and I got 5/5. To check this one, I couldn't just trust that a source being *named* meant it was *correct* — I had to actually open each cited document myself and read it, to confirm the fact my system claimed really is written there, word for word, and not just a document that happened to be nearby in the search results. I did this for all 5 questions, and every single citation checked out as genuinely accurate. |

## Diagnoses

The instructions for this section say: for each criterion I missed, figure
out which of the five pipeline stages caused it (loading → chunking →
embedding → retrieval → generation), and explain the actual mechanism, not
just "it didn't work." **But in my case, nothing was actually missed** — all
5 criteria came out MET, holding across all 3 runs. So instead of diagnosing
a failure, this section is me being honest about a close call that *looked*
like a failure, and explaining exactly why it wasn't one, plus thinking
honestly about whether my targets were actually hard to hit or just easy.

**The near-miss, explained properly.** `scorer.py` (the little program I
built to automatically grade my system's answers) marked the question "What
hours do Kestrelford's pubs serve food?" as a fail, in all 3 runs. My first
instinct was to assume something in my pipeline was broken. So I went
through each of the five stages one at a time, the same way the assignment
wants me to for a real failure:

- **Loading** — did the right document even get read off disk? Yes,
  `guide_kestrelford.md` was loaded correctly, same as every other document.
- **Chunking** — did my chunker cut the pub-hours sentence in a way that
  lost information? No — the whole "Eat and drink" section came through as
  one complete chunk, sentence intact.
- **Embedding** — did the chunk get turned into a search-able vector
  correctly? Yes — I could tell because of what happened at the next stage.
- **Retrieval** — did my search actually find and return this chunk when I
  asked the question? Yes, every time — the "best distance" was 0.144, one
  of the closest matches across all my questions, meaning the system was
  very confident it had found the right chunk.
- **Generation** — did the AI model write a correct answer using that
  chunk? Yes — every one of the 3 runs said the pubs serve food "between 12
  and 2 and again between 6 and 8:30," which is exactly correct, and it even
  named the right source document each time.

So all five stages worked perfectly. The actual problem is something the
assignment's five-stage list doesn't even cover, because it isn't part of
the RAG pipeline at all — it's in my own **test setup**. Back in Unit 1, I
wrote my `expects` phrase (the exact text I told my test framework a
correct answer must contain) as `"12 to 2 and 6 to 8:30"`. But the real
document text — and every single answer my system generated from it —
phrases the same fact as "between 12 **and** 2 and again between 6 **and**
8:30." Same numbers, same fact, genuinely correct — just connected with the
word "and" instead of the word "to." My original `scorer.py` was built to
do an exact substring match (after cleaning up capitalization, punctuation
and extra spaces), so it was looking for my *exact* wording, word for word,
and a phrase that says the same true thing in slightly different words
never matched. In short: my pipeline was never broken. My test was checking
for the wrong kind of match.

**Were my targets set too easy?** Looking honestly at the numbers, mostly
yes. Criteria 2 through 5 all beat their targets comfortably — I asked for
"at least 4 of 5" (or already the strictest possible, "5 of 5") and got a
clean 5/5 on all of them, every run. That's a sign I probably wasn't
pushing my system very hard with those targets. Criterion 1 is the one
honest exception — it landed exactly on its target, 4 of 5, not higher —
so that's the one place where my Unit 1 self actually set a number with
real stakes, even though it turned out the "miss" inside that 4/5 wasn't a
real system problem after all.

**Which one would I tighten, and to what?** I'd tighten criterion 3 (the
relevance gate — the part of my system that's supposed to say "I don't
know" instead of guessing when a question is outside what my documents
cover) from "at least 4 of 5" up to "5 of 5." My reasoning: back in Unit 1,
when I measured how far apart my "real" questions and my "nonsense"
questions were (using a number called "distance," where lower means more
related), I found a huge, clean gap — my worst real question scored 0.364,
and my closest nonsense question scored 0.808. That's a 0.44-wide gap with
absolutely nothing in the middle, the widest safety margin of any of my
five criteria. And sure enough, in this unit's actual testing, it held at
a full 5/5 in every single run, no exceptions. When a target has that much
extra room between what I required and what the system actually
consistently does, it isn't really testing the edge of what the system can
do — it's just confirming something I already knew was safe. Raising it to
5/5 would turn it into a real standard instead of a comfortable one.

## The Improvement

**What I changed:** I rewrote one function, `scorer.py::contains_phrase`,
which is the piece of code that actually decides whether an answer counts
as "correct." The old version worked like this: clean up both the
`expects` phrase and the answer (make everything lowercase, remove
punctuation, collapse extra spaces), then check whether the *exact,
whole* `expects` phrase — as one continuous piece of text, in that exact
word order — shows up somewhere inside the answer. The new version works
differently: it first strips out a small list of "connector" words that
don't actually carry any of the real information (words like "to," "and,"
"between," "again," "the," "a," "an," "of"), from *both* the `expects`
phrase and the answer. Then, instead of requiring the whole phrase to
appear as one continuous chunk of text, it just checks that every
remaining word — the words that actually carry the fact, like numbers and
names — shows up *somewhere* in the answer, in any order. So "12 to 2 and
6 to 8:30" becomes, after stripping connectors, just the four numbers "12,
2, 6, 8:30" — and the check now just asks "are all four of these numbers
present in the answer," rather than "does this whole sentence appear
verbatim."

**Why I picked it:** My Milestone 3 diagnosis walked through all five
pipeline stages for the one question that was failing, and found that
every single stage — loading, chunking, embedding, retrieval, and
generation — was working correctly. The system was retrieving the right
information and writing correct, well-sourced answers. The only actual
problem was in how I was *grading* those answers: my `expects` phrase
assumed the model would always phrase things using the word "to" ("12 to
2"), but the real documents — and every answer the model generated —
consistently use "and" instead ("between 12 and 2"). Since my diagnosis
pointed specifically and only at this grading mismatch, and not at
anything in the actual RAG pipeline, I made sure my one allowed change
targeted that exact thing. I didn't touch chunking, retrieval, or the
prompt, because nothing about my diagnosis said there was a problem there
— touching those would have been fixing something that wasn't actually
broken.

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

**Did it help?** Yes, and in exactly the way I expected before I even ran
it, which is how I know it was a real fix and not just a lucky number
change. Before the fix, criterion 1 sat at exactly 4/5, the bare minimum
that still counted as MET — not a failure, but the closest of all five
criteria to actually becoming one. After the fix, criterion 1 moved to a
full 5/5, in every one of the 3 runs. Every other criterion was already
sitting at 5/5 before I made this change, and none of them moved — which
actually makes sense and isn't something to worry about, since none of
those other four questions had the "to" versus "and" wording problem in
the first place, so there was nothing for this specific fix to change
about them. The clearest proof that this was a genuine fix, and not just
me nudging a number until it looked better: the AI's actual generated
answer text is **identical** before and after my change — word for word,
same source citations, same everything. What changed wasn't what the
system said. What changed was how correctly I was able to *recognize*
that the system's answer was right.

## What's Still Broken

Technically, nothing — every single one of my 5 criteria is MET, at a full
5/5, in all 3 runs, after my fix. It would be easy to stop here and call
the system finished, but "I hit my own targets" and "there's nothing left
to improve" are two very different claims, and I only actually earned the
first one. Here's what I know is still weak, even though none of it shows
up as a failing number:

- **I only tested 5 questions, and I wrote all 5 of them myself.** The
  assignment asks for 5, so that's what I have, but 5 questions against 14
  documents and 94 chunks is a small slice of everything my system could
  possibly be asked. Because I'm the one who wrote all 5 questions, I
  might have unconsciously picked questions I already suspected my system
  would handle well. A question I haven't thought of yet — maybe a
  trickier one, or one about a part of a document I skimmed past — could
  still fail in a way none of my current 5 would ever reveal, simply
  because I never asked it.
- **Every single one of my 5 questions has its complete answer sitting in
  one chunk.** None of them require the system to combine two separate
  facts from two different chunks to produce a full answer. That means I
  genuinely don't know how my system behaves on a harder kind of question
  — one where, say, half the answer is in the "Getting there" section and
  the other half is in "Practical notes." I never tested that case,
  because I never wrote a question that needed it.
- **My improved `scorer.py` is better, but it's still not a real
  "understanding" check.** It would still mark "eleven" and "11" as
  completely different words, even though a human reading both would
  immediately know they mean the same number. Same with a correct answer
  that used a synonym in place of the exact word I wrote in `expects` — my
  scorer has no way to know two different words can mean the same thing.
  It's genuinely more forgiving than the old exact-substring version, but
  it's still just comparing words on the page, not meanings.

I'm choosing to stop here rather than keep going, because the assignment
specifically asks for exactly one measured improvement, and I made the one
that my actual diagnosis pointed at — not a random guess at what else
might be wrong. These three points aren't things I ran out of time for;
I'm listing them honestly as things I never attempted in the first place,
and I'd want to actually test all three before I'd trust this system with
something that mattered more than a class project.

## What I'd Do Differently

Knowing everything I know now, having actually run my system and watched
where it came close to a problem versus where it didn't, here's what I'd
change about how I wrote my original five criteria back in Unit 1:

**Criterion 1** — I would have written my `expects` phrases completely
differently from the very start. Instead of writing one exact sentence
fragment like `"12 to 2 and 6 to 8:30"` and hoping the AI model would
happen to phrase its answer exactly that way, I'd write `expects` as a
*list* of the individual pieces of information that actually matter —
something like `["12", "2", "6", "8:30"]` — and check that all of them
show up, regardless of what words connect them. That's basically what my
Milestone 4 fix ended up doing anyway, just built into `scorer.py` after
the fact instead of designed into `questions.py` from the beginning. If
I'd written it this way originally, I never would have gotten a false
"fail" in the first place, because I wouldn't have been testing for one
specific sentence structure — I'd have been testing for the actual facts.

**Criterion 3** — I would have set a stricter target from day one: "5 of 5"
instead of "at least 4 of 5." Here's why I think I was too cautious the
first time: back in Unit 1, before I'd even built this Unit 2 test, I had
already measured the "distance" gap between my real questions and my fake
ones, and found a huge 0.44-wide gap with nothing in the middle (0.364 for
my hardest real question versus 0.808 for my closest fake one). That's
strong evidence, and I had it in hand *before* I wrote my target — I just
didn't trust it enough at the time and played it safe with "4 of 5"
instead. Now that I've actually run the test twice (once before my fix,
once after) and gotten a clean 5/5 both times, I can see that my caution
wasn't necessary. I had the evidence to be stricter all along.

**Criterion 2** — I wouldn't change this one at all. My original reasoning
in Unit 1 was that naming a source isn't something the AI model has to
remember or decide to do — it's guaranteed by a single line of my own
Python code, not by the model's judgment. That reasoning turned out to be
exactly right: this criterion passed at a perfect 5/5 in every run, in
both units, with zero exceptions. When a piece of reasoning holds up this
well under real testing, I don't think the lesson is "I got lucky" — I
think the lesson is that I understood my own system correctly when I wrote
it, and there's nothing here I'd second-guess just for the sake of
revising something.
