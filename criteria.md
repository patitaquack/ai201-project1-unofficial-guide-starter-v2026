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

Four of my questions are about topics several guides mention, so I expect those
to be found easily. But "Where can I go birdwatching?" only has one guide that
covers it — `guide_elder_ness.md` is the only file in my corpus that mentions
birds at all. With just one document to find, that's the one I expect to be
hard, so I left room for one miss.

---

## 2. Every answer names a source

Every answer the system produces names at least one source document.

**Why this target:**



I set this at all five because the system doesn't have to find anything extra to do it. The filename is already in the prompt — every chunk gets a
`[from guide_elder_ness.md]` line above it, and the system prompt tells the
model to name the file it used. It seems simple enough that all five should
pass. The criterion is checking whether it will follow that simple instruction
each time.



---

## 3. The relevance gate stops out-of-corpus questions

When I ask a question my documents clearly don't cover, the relevance gate
stops it and the system returns "I don't have enough information about that" —
in at least 4 of 5 tries.

<!-- The five questions are the ones in `OUT_OF_SCOPE` at the bottom of
     `questions.py`, and `run_eval.py` puts them through the gate and writes
     what happened into your run log. Swap them for your own if you'd rather —
     just keep five of them, or the "4 of 5" above has nothing to be 4 of. -->

**Why this target:**
<!-- What did your distances look like when you set the cutoff in Milestone 4?
     Was there a clean gap, or did the two groups overlap? -->

     When i set the cutoff for Milestone 4, there was a clean gap. Five questions had best distances between 0.325 and 0.573. The five out-of-scope questions were between 0.810 and 969, nothing landed in between. The gap is more that 0.2 wide- so I put the cutoff at 0.70, roughly in the middle of it. I set the target at 4 of 5 rather than 5 of 5 because gap being clean one moment foesnt mean every out-of-corpus question will be above 0.810.

---

## 4. Something about your chunks

No chunk ends mid-sentence


**Why this target:**

the starters fixed 800 character splitter cuts 33 of 51 chunks mid- sentece. My guides are markdown with sections of 150-400 characters, each a selfcontained topic. A splitter respects the boundaries and shouldn't need to cut a sentence.




---

## 5. the source named actually contains the answer

For at least 4 of my 5 questions, the guide the answer names is one that actually contains the answer.


**Why this target:**

This asks if it cited a file that really has the information.
It is worth testing, so that the model can name a file that it did use to answer.








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
