# The Unofficial Guide

<!-- Replace this line with your name and which corpus you picked. -->

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

<!-- Three or four sentences. Which corpus you picked, and the kinds of
     questions your system answers. Write it for someone who has never seen
     this repo.

     Milestone 5. -->

## Chunking Strategy

**Chunk size:** one `##` section per chunk — not a fixed number. In practice
183 to 758 characters, 319 on average.
**Overlap:** none.

Every document in `city_guides` is a Markdown guide to one town, divided into
labelled `##` sections — Getting there, Eat and drink, When to go. Each section
is a self-contained topic, and no section depends on the one before it. The
document already says where the boundaries are, so a fixed character count is
the wrong instrument: it ignores the structure that's sitting right there.

I measured all 98 sections before writing anything. The largest is 708
characters, so nothing needs a size cap as a backstop — splitting on headings
alone never produces a chunk too big to handle. And because a heading-aligned
cut never lands mid-sentence, there is nothing for an overlap to rescue, which
is the only job overlap was doing.

Every chunk is prefixed with its document title. This turned out to matter more
than the split itself: the town name appears only in the `# Givens Mill` title
at the top of the file, never in the sections beneath it, which say "the mill"
and "the tearoom". Without the prefix, 13 other guides describe their parking
and their pubs in near-identical language and nothing distinguishes them.

The starter's fixed 800-character windows gave 51 chunks, 33 of them cut
mid-sentence and 8 under 200 characters — the shortest was 24, a bare
`## Getting there` heading with its content sliced into the next chunk. The new
strategy gives 94 chunks, none cut mid-sentence, shortest 183.

## Sample Chunks

<!-- Five chunks, pasted as text. Label each one and name the file it came from
     AND the function that produced it — the grader checks your code against
     what you claim here.

     `python app.py chunks -n 5` prints all three for you. Copy them straight
     across.

     Milestone 3. -->

**Chunk 1** — source: `guide_accessibility.md#0` — produced by: `chunker.py::split_documents`

```
Getting around the region with limited mobility — Overview

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

**Question:** What are the operating hours of the tearoom in Givens Mill?

**Answer:**

```
  (best distance 0.325, cutoff 0.7)

The tearoom is open from 10 to 4 daily, except on Tuesdays (guide_givens_mill.md).

Sources retrieved: guide_givens_mill.md
```

**My relevance cutoff:** 0.70

The two groups came out cleanly separated, with nothing between them:

```
in corpus      0.325 – 0.573
out of scope   0.810 – 0.969
gap            0.573 → 0.810   (0.238 wide)
```

I put the cutoff at 0.70, near the middle of that gap. The starter's 0.6 also
works — it refuses all five out-of-scope questions and admits all five real
ones — but it clears my worst real question by only 0.027. My two weakest
questions, "Is there a town with a tearoom?" at 0.569 and "Where can I go
birdwatching?" at 0.573, are the ones that don't name a town, and a vaguer
phrasing of either would land above 0.6 and be refused with the answer sitting
right there. 0.70 leaves 0.13 of room above them and still sits 0.11 below the
nearest out-of-scope question.

What I get wrong at 0.70: the gap is this wide because my out-of-scope
questions are about Mongolia and Rust loops — absurd, not merely off-topic. A
question about my towns whose answer isn't in the guides scores far lower and
sails straight through. "How far is it from Givens Mill to Halden Bay?" — a
distance the corpus never states — comes back at 0.351, nowhere near any
cutoff I could set without refusing real questions. The gate cannot catch that
case, by construction; only the grounding instruction can, and it does.

**top-k: 5, unchanged.** Worth keeping rather than lowering: for "Is there a
town with a tearoom?" the chunk holding the answer comes back third, behind an
unrelated Corry Vale overview. At top-k 2 that question would fail outright.

**Grounding instruction: left as the starter wrote it.** I tested it on the
Givens Mill to Halden Bay distance, which passes the gate at 0.351 and pulls
three genuinely relevant guides, none of which contains a mileage. It answered
"I don't have enough information" instead of estimating one, so I had nothing
to tighten.

| Question | In corpus? | Best distance |
|---|---|---|
| What are the operating hours of the tearoom in Givens Mill? | Yes | 0.325 |
| Is Thornby Wells easy for walking? | Yes | 0.372 |
| Where can I find fresh seafood? | Yes | 0.465 |
| Is there a town with a tearoom? | Yes | 0.569 |
| Where can I go birdwatching? | Yes | 0.573 |
| What is the capital of Mongolia? | No | 0.810 |
| What is the recommended dosage of ibuprofen for a headache? | No | 0.835 |
| How do I write a for loop in Rust? | No | 0.861 |
| How do I change the oil in a diesel engine? | No | 0.881 |
| Who won the 1994 World Cup? | No | 0.969 |

## How I Used AI

<!-- Two specific moments. For each: what you asked for, what came back, and
     what you changed about it.

     "I asked Claude to write the chunking function from my notes. It ignored
     the overlap, so I added that myself" is the level of detail we're after.
     "I used AI to help me code" is not.

     Milestone 5. -->

**1.**

**2.**

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
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

<!-- Underneath, paste the REAL output for each criterion from one of your
     runs — the actual text your system produced, not a description of it.
     Name the file and function that produced it. -->

## Verdicts

<!-- MET or MISSED for each of the five, against the target you wrote last
     unit — not a new one. Plus a sentence on how you decided. That sentence
     matters most where it was close.

     If your target said 4 of 5 and your runs came out 4, 3, 4, that's a MISS.
     The target has to hold, not show up occasionally.

     Milestone 2. -->

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 |  |  |  |
| 2 |  |  |  |
| 3 |  |  |  |
| 4 |  |  |  |
| 5 |  |  |  |

## Diagnoses

<!-- For each miss: which stage caused it, and how. The stage alone isn't
     enough — you need the mechanism.

     Not a diagnosis: "Question 3 didn't work."
     A diagnosis:     "Question 3 asks about laundry costs. The answer is in
                       one sentence that got split across two chunks, so
                       neither chunk on its own contains it."

     The five stages: loading → chunking → embedding → retrieval → generation.

     Look for a pattern. If three misses all ask about numbers, that's one
     problem, not three.

     Missed nothing? Say so, then say honestly whether your targets were set
     low, and which one you'd tighten and to what.

     Milestone 3. -->

## The Improvement

**What I changed:**

**Why I picked it:**

<!-- Connect it to a specific diagnosis above in one sentence. If you can't,
     you picked a fix because it sounded impressive. -->

### Run Log — After

<!-- Same format, same five criteria, three runs each.
     `python run_eval.py --label after` -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

**Did it help?**

<!-- Say plainly whether it did, and how you know. If it made things worse,
     say that — a change that backfired, honestly reported, earns full credit
     and is more interesting than one that worked. What matters is that you can
     tell.

     Milestone 4. -->

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
