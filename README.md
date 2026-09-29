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

This is a question-answering system over city_guides, a corpus of 14 travel
guides to towns and villages in one fictional region — Givens Mill, Halden Bay,
Thornby Wells and eleven others — plus four cross-cutting guides on eating,
walking, transport and accessibility.

It answers practical questions a visitor would actually ask: what time the mill tearoom opens, where to find fresh seafood, whether a town is manageable on
foot, where you can go birdwatching. Questions with a right answer sitting in
the documents, not matters of taste.

It answers from the guides and nothing else. Every answer names the file it came
from, and a question the guides don't cover gets "I don't have enough
information about that" rather than a plausible invention.

## Chunking Strategy

**Chunk size:** one ## section per chunk — not a fixed number. In practice
183 to 758 characters, 319 on average.
**Overlap:** none.

Every document in city_guides is a Markdown guide to one town, divided into
labelled ## sections — Getting there, Eat and drink, When to go. Each section
is a self-contained topic, and no section depends on the one before it. The
document already says where the boundaries are, so a fixed character count is
the wrong instrument: it ignores the structure that's sitting right there.

I measured all 98 sections before writing anything. The largest is 708
characters, so nothing needs a size cap as a backstop — splitting on headings
alone never produces a chunk too big to handle. And because a heading-aligned
cut never lands mid-sentence, there is nothing for an overlap to rescue, which
is the only job overlap was doing.

Every chunk is prefixed with its document title. This turned out to matter more
than the split itself: the town name appears only in the # Givens Mill title
at the top of the file, never in the sections beneath it, which say "the mill"
and "the tearoom". Without the prefix, 13 other guides describe their parking
and their pubs in near-identical language and nothing distinguishes them.

The starter's fixed 800-character windows gave 51 chunks, 33 of them cut
mid-sentence and 8 under 200 characters — the shortest was 24, a bare
## Getting there heading with its content sliced into the next chunk. The new
strategy gives 94 chunks, none cut mid-sentence, shortest 183.

## Sample Chunks



**Chunk 1** — source: guide_accessibility.md#0 — produced by: chunker.py::split_documents

Getting around the region with limited mobility — Overview

An honest assessment rather than a promotional one. Some of these places are
difficult and it is better to know in advance.


**Chunk 2** — source: guide_corry_vale.md#5 — produced by: chunker.py::split_documents


Corry Vale — Where to stay

Perhaps thirty beds in the entire valley, spread across two pubs and a handful of farmhouse rooms. In summer these are booked months ahead. Camping is permitted on two marked fields and nowhere else.


**Chunk 3** — source: guide_givens_mill.md#2 — produced by: chunker.py::split_documents


Givens Mill — Getting around

Everything is on one street along the river. The mill is at one end and the church at the other, eight minutes apart. The riverside path continues in both directions for as far as you want to walk.


**Chunk 4** — source: guide_kestrelford.md#4 — produced by: chunker.py::split_documents


Kestrelford — What to see

The market square on a Saturday morning is the main event and has run continuously since the 1400s. The parish church has a 13th-century tower you can climb for £2. The old trackbed walk runs six miles to the next village along an easy gradient and is the best half-day here.


**Chunk 5** — source: guide_pellew_sands.md#6 — produced by: chunker.py::split_documents


Pellew Sands — When to go

June and September for the beach without the crowds. July and August are busy and the town is at its most itself, for better and worse. Winter is bleak, largely closed, and has a following among people who like that sort of thing.


## Sample Answer

<!-- One complete question and answer, pasted as text, with the source line
     visible. Milestone 4. -->

**Question:** What are the operating hours of the tearoom in Givens Mill?

**Answer:**


  (best distance 0.325, cutoff 0.7)

The tearoom is open from 10 to 4 daily, except on Tuesdays (guide_givens_mill.md).

Sources retrieved: guide_givens_mill.md


**My relevance cutoff:** 0.70

The two groups came out cleanly separated, with nothing between them:

`
in corpus      0.325 – 0.573
out of scope   0.810 – 0.969
gap            0.573 → 0.810   (0.238 wide)


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



**1. Checking my test questions against the corpus.** I asked Claude to check my questions and expected answers to see if this is something that a user would ask. I also asked if the answers would be retractable with the chunking I chose.

**2. Designing the chunker.** I asked for a chunking strategy for my corpus
rather than a function to paste in. It measured all 98 `##` sections first —
largest 708 characters, so nothing needs a size cap — and proposed splitting on
headings with no overlap, which matched what I'd seen reading the guides.


──────────────────────────────────────────────── -->

---

# Unit 2



## Run Log — Before



| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |5/5|5/5|5/5|MET|
| 2. Every answer names a source |5 of 5|5/5|5/5|5/5|MISSED|
| 3. Gate stops out-of-corpus questions | 4 of 5|5/5|5/5|5/5|MET|
| 4. No chunk ends mid-sentence | 94 of 94 | 94/94 | 94/94 | 94/94 | MET |
| 5. Named source contains the answer | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |

Criterion 2's run columns count the five gated-through answers, all of which named a source. The MISSED comes from the five gate refusals, which name no source and are measured in the same single pass as criterion 3.

### Real output

**Criterion 1 — retrieved chunks contain the answer.**
Produced by `run_eval.py::run_once`, retrieval by `store.py::search`.


### Where can I go birdwatching?  — run 1

- Best distance: 0.5729 (passed the gate)
- Sources retrieved: guide_eating.md, guide_elder_ness.md, guide_halden_bay.md


**Criterion 2 — every answer names a source.**
Produced by generate.py::answer_from_chunks.


You can go birdwatching at Elder Ness, which is known for spring and autumn
migration (April to May and September to October).

Source: `guide_elder_ness.md`


**Criterion 3 — the gate stops out-of-corpus questions.**
Produced by run_eval.py::check_out_of_scope, cutoff 0.7.

| Out-of-scope question | Best distance | Gate |
|---|---|---|
| What is the capital of Mongolia? | 0.810 | refused |
| How do I change the oil in a diesel engine? | 0.881 | refused |
| Who won the 1994 World Cup? | 0.969 | refused |
| What is the recommended dosage of ibuprofen for a headache? | 0.835 | refused |
| How do I write a for loop in Rust? | 0.861 | refused |

**Criterion 4 — no chunk ends mid-sentence.**
Produced by chunker.py::split_documents

```
94 chunks

--- guide_accessibility.md (183 chars) ---
Getting around the region with limited mobility — Overview

An honest assessment rather than a promotional one. Some of these places are
difficult and it is better to know in advance.
```

**Criterion 5 — the named source contains the answer.**
Answer from generate.py::answer_from_chunks, verified against corpora/city_guides/documents/

The birdwatching answer above cites guide_elder_ness.md, and that file is the only one in my corpus that mentions birds at all.


## Verdicts


| # | Criterion  | Verdict | How I decided  |
|---|---|---|--- |
| 1 | Retrieved chunks containing the answer | MET | Checked the retrieved chunks directly, not the answers, the expected text appears in at least one chunk for all 5 questions. Target was 4 of 5. |
| 2 | Every answer names a source | MISSED | 15 of 20. All 15 gated-through answers named a source, but the 5 gate refusals named none, and I did state "every answer." |
| 3 | Gate stops out-of-corpus questions | MET | 5 of 5 refused. Closest out-of-scope distance was 0.810 against a 0.70 cutoff, so none was near the line. Measured in one deterministic pass. |
| 4 | No chunk ends mid-sentence | MET | All 94 chunks end with a period — I checked the last character of every one. Target was no exceptions. |
| 5 | Named source contains the answer | MET | 5 of 5. Opened each cited guide and confirmed it contains the answer given. Target was 4 of 5. |

## Diagnoses



**Criterion 2 — every answer names a source. MISSED, 15 of 20.**

No pipeline stage caused this. Generation worked: all 15 answers that reached the
model named a source, and the 5 that didn't were gate refusals, which have no
chunks to cite.

The fault is in the criterion. I wrote "every answer the system produces," and a
refusal is an answer the system produces. So criterion 2 counted every success
of criterion 3 as a failure of criterion 2. The two criteria were in direct
conflict and I did not notice until I scored them. The mechanism is my wording,
not my code — nothing in generate.py or gate.py would change if I fixed it.

**Were my targets set low?**

Criterion 3 had the most room. The gap between my real questions (worst 0.573) and my out-of-scope ones (best 0.810) is over 0.2 wide, against a cutoff of 0.70. My out-of-scope questions — Mongolia, diesel engines, the 1994 World Cup — are nowhere near my corpus. I proved the gate blocks obviously foreign questions, not that it blocks out-of-corpus ones.

Criterion 2 asked the model to repeat a filename already sitting in its prompt. That was never going to be hard.

Criterion 1 was my best prediction and it was wrong. I expected birdwatching to be the hard one because only `guide_elder_ness.md` mentions birds. It scored 0.573 and retrieval found it every time.

**The one I'd tighten:** criterion 3. I'd replace my out-of-scope questions with
ones that use my corpus's own vocabulary but ask about things it doesn't cover.
"Where is the nearest campsite to Elder Ness?" names a real town from my guides,
but no guide mentions campsites. Those land far closer to the 0.70 cutoff than
Mongolia did, and they are a real test of where the cutoff belongs.

A second candidate is criterion 1. My top-k is 5, so "the retrieved chunks
include one that contains the answer" gives the system five chances. Tightening
it to the top 3 would be a meaningfully harder target.



## The Improvement

**What I changed:**

I added a keyword check to the relevance gate. It was comparing distance only.
It now also checks whether the question's content words appear anywhere in the
retrieved chunks, and refuses when they don't. The code is
gate.py::unsupported_terms, called from gate.py::check.

I also replaced the five questions in OUT_OF_SCOPE. That is a better
measurement rather than part of the fix — without it, before and after look
identical, because the old gate refuses Mongolia either way.

**Why I picked it:**

My diagnosis said criterion 3's MET was an artifact of easy out-of-scope
questions, and when I wrote harder ones the gate let all five through at
distances as low as 0.327 — better than four of my five real questions.

### Run Log — After



Produced by run_eval.py::mai, written to results/run_2026-09-29_1352_after.md.
15 model calls. Same model as the before run.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 2. Every answer names a source | 5 of 5 | 5/5 | 5/5 | 5/5 | MISSED |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. No chunk ends mid-sentence | 94 of 94 | 94/94 | 94/94 | 94/94 | MET |
| 5. Named source contains the answer | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |

Criterion 2's run columns count the five gated-through answers, all of which
named a source. The MISSED is still the five refusals, which name none. That
number did not change because I did not change the wording.

**Did it help?**

<!-- Say plainly whether it did, and how you know. If it made things worse,
     say that — a change that backfired, honestly reported, earns full credit
     and is more interesting than one that worked. What matters is that you can
     tell.

     Milestone 4. -->

Yes, and I can say how much. The before and after run logs are not the honest
comparison for criterion 3, because the questions changed between them. The
honest comparison is the harder questions against each version of the gate,
which costs no model calls and which I measured both ways:

```
harder questions, old gate (distance only)       0 of 5 refused
harder questions, new gate (distance + keyword)  5 of 5 refused
```

Nothing regressed. All five real questions still pass the gate, all 15 answers
still name a source, and criteria 1, 4 and 5 are unchanged.

**The fix the assignment suggested is not the fix that worked.** I tried BM25
scoring first, as the hybrid search option describes, and measured it:

```
REAL questions       best BM25  5.54 – 15.75
UNCOVERED questions  best BM25  8.20 – 10.03
```

Those overlap, so no BM25 cutoff separates them. The reason is that questions
like "Where is the nearest campsite to Elder Ness?" contain real town names,
and BM25 rewards that match. BM25 asks how strongly a question matches. What I
needed was whether any content word matches at all. That is the check I ended
up writing.

## What's Still Broken

<!-- For each criterion still missed after your fix: what you'd do about it,
     and why you stopped where you did.

     "I ran out of time" is fine if it's true. Pretending nothing is left is
     not.

     Milestone 5. -->

**Criterion 2 is still MISSED, at 15 of 20.** I did not touch it. The fix is one
sentence — change "every answer" to "every answer that passed the relevance
gate" — but that is a revision to a criterion rather than a change to the
system, and I had one improvement to spend on Milestone 4. I spent it on
criterion 3, which was a real failure rather than a wording problem.

**My stopword list is fitted to my own test set.** gate.py::STOPWORDS decides
which words count as content words, and I built it by running my ten questions
and adding whatever broke them — "find" had to go in because it made the
seafood question fail. A new question using some other ordinary verb could be
refused for no good reason. A real fix would use a standard English stopword
list rather than one I tuned until my own tests passed.

**The keyword check only sees the retrieved chunks.** If retrieval misses the
one chunk that contains the answer, the check sees a corpus that appears not to
cover the topic and refuses. That turns a retrieval failure into a refusal,
which looks like correct behaviour in my run log. I have no test that would
catch it.

**I wrote all five out-of-corpus questions myself,** knowing what my corpus
contains. Someone else's questions would be a fairer test, and five is a small
number to conclude anything from.

## What I'd Do Differently



Three of my five had measurement problems rather than result problems.

**Criterion 2.** I'd write "every answer that passed the relevance gate names a
source." As written it counted the gate's refusals as failures, so criterion 2
punished criterion 3 for working. I did not notice the two contradicted each
other until I scored them.

**Criterion 1.** I'd say how I intended to measure it. "The retrieved chunks
include one that contains the answer" sounds checkable, but my scorer reads the
*answer text*, not the chunks — so for most of this unit I was measuring
something different from what the criterion said, and I had to go back and
check the chunks separately. I'd also tighten it to the top 3 rather than all of
top-k, since my top-k is 5 and that gives the system five chances.

**Criterion 3.** I'd pick harder out-of-scope questions from the start. Mongolia
and diesel engines share no vocabulary with a regional travel guide, and the
distances showed it — nothing under 0.810 against a 0.70 cutoff. I only found
out my gate was broken because I went looking in Milestone 3.

**Criterion 5.** I'd say what happens when an answer names two files. I wrote
"*the* guide the answer names," and two of my answers cited two guides each.
Both contained the answer so it did not change the verdict, but the criterion
does not say how to score it.

**Criterion 4 is the one I'd keep as it is.** "No chunk ends mid-sentence" is a
single thing I can check by looking at the last character of 94 chunks, and it
gave the same answer every time. The difference is that I knew how I would
measure it before I wrote it.

**The pattern:** I wrote five criteria before I had any way to check them. The
one I could check mechanically is the one that held up. Next time I'd write the
check at the same time as the criterion — if I can't say how I'd measure it, I
don't really have a criterion yet.
