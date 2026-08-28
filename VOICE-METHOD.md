# The voice pass — how to do this on every page

Written 2026-08-25 after Cole: *"Overall copy still doesn't sound like somebody
is talking and writing this, it sounds like you are following rules again. Be a
PERSON and talk, not so choppy."* And then: *"Go through every page and fix the
caption headings, and then develop a plan to do this on EVERY PAGE."*

This is that plan. It exists because "sounds like a person" felt unfixable until
it got broken into the parts a machine can catch and the parts only a person can.

---

## What actually went wrong, named

Three distinct faults, and they need different treatment.

### 1. Stiff forms — machine-catchable

Writing **"that is not"** where a person says **"that's not"**. This was the
single loudest tell and it was everywhere.

Measured: the approved Our Story page runs about **one contraction per 30
words**. The copy Cole rejected ran **one per 220**. That is not a stylistic
preference, it is the difference between speech and a rulebook.

**164 stiff forms** were relaxed across 28 files in this pass.

### 2. Caption headings — human judgement, no shortcut

A heading has three possible jobs and only one of them is wrong:

| | | Verdict |
|---|---|---|
| **Line** | Says something | Keep |
| **Caption** | Describes the block it sits on | **Fix** |
| **Label** | Functional wayfinding | Keep plain |

- Caption: *"One wedge, side by side"*, *"The Lucky timeline"*, *"From
  application to creator"*. These describe furniture.
- Line: *"Spot the difference"*, *"How a gold wedge turned into all this"*,
  *"What happens after you hit send"*.
- Label: row keys (`Head construction`, `Face`), breadcrumbs, support page
  titles. **Deliberately plain. Writing these in voice is the opposite
  mistake** and would make a spec table unusable.

**The worst sub-type is the META heading** — one that describes its own
writing. *"Bounce, in one paragraph"*. *"The bar, stated plainly"*. *"That is
not an accident of wording, it is the argument."* A page should never narrate
how it was built.

### 3. Explaining the device — human judgement

Telling the reader what a layout is doing. Cut it and just point: *"Look at
rows two and three."*

---

## Do not trust a script to judge a heading

This was tried. A detector flagged **106 of 166** headings, and most flags were
wrong — it condemned *"The stuff that wears out first"* and *"Quiet hands hole
more short putts"*, which are good lines. **Judgement did not automate.** The
script's only honest job is telling you which FILE to go and read.

The same lesson applies to the contraction fixer. Its guard only fires when a
real word follows, because sentence-final **"the gap under it is."** must never
become "it's". Roughly half the raw matches were exactly that, and a tool that
reports those as errors teaches everyone to ignore it.

---

## The tool

```bash
python tools/voice-audit.py          # every copy file, stiffest first
python tools/voice-audit.py --stiff  # the exact phrases, with context
```

Reads two columns:

- **stiff > 0** → real, fix it.
- **`read it`** → no stiff forms, just little contracted speech. Usually fine
  for short spec copy. **Go read it. Do not bulk-edit it.** A grip page can
  score 137 words-per-contraction and be perfectly well written, because there
  is nowhere in it a person would naturally contract.

Exit code is non-zero while any file carries stiff forms, so it can gate a
build if that is ever wanted.

---

## Running it on a page

1. `python tools/voice-audit.py` and take the top file.
2. Fix the stiff forms. The guarded pass handles the bulk; check the two cases
   it deliberately skips (a stiff pair followed by `$`, a digit or markup).
3. Read every heading in the file and sort each into line / caption / label.
   Rewrite the captions. Leave the labels alone.
4. Read the paragraphs aloud. Fragments where flow belongs is the remaining
   fault the script cannot see: *"A tour contract. Somebody is paid to…"* reads
   as a brochure cut into strips. Real sentences connect.
5. Rebuild and run all four guards.

---

## Two places the rules deliberately do not apply

- **The refund policy** (`_support-returns`). Categorical statements a customer
  may hold us to keep the formal form: *"A club returned without authorization
  is not accepted."* Only the explanatory sentences were relaxed. This file is
  exempt from the bulk pass by design.
- **Customer reviews.** Quoted review text is verbatim and is never edited,
  ever. Several stiff forms on the homepage sit inside review quotes. Editing
  them would be fabricating a review.

---

## Where it landed

| | Before | After |
|---|---|---|
| Files carrying stiff forms | 32 of 40 | 1 |
| Stiff forms in copy | 164 | 6 |
| Caption headings | 11 found | 0 |
| British spellings in copy | 21 | 0 |

The one file and six forms remaining are the refund policy's categorical rules
(*"A club returned without authorization is not accepted"*), left formal on
purpose per the exemption above. Everything explanatory in that file now talks.

Guards after: `--check` 59 identical, `--links` 0 dangling,
`test-variants.js` holds, `normalize-products.py --check` identical.

**The bar, for anything written from here:** if you would not say it out loud to
a golfer standing next to you, it is not finished.


---

## Addendum: what the full read found (2026-08-25)

Cole asked for every word read, not just the machine pass. It was worth doing.
The audit had already cleared the mechanical faults; **reading found nine more
that no script would have caught**, and four of them were damage the script
itself had done.

### The tools broke copy, and only reading caught it

The contraction fixer turned **"a coating you have to baby"** into *"you've to
baby"*. It hit six files. `have to` and `has to` express OBLIGATION and never
contract in English, and the fixer did not know that. Same root cause produced
**"If you've one"** on the Patriot page, from "If you have one" — a valid-looking
contraction that is only correct before a past participle ("you've got one").

Both the fixer and `voice-audit.py` are now guarded against it. **This is the
argument for reading:** an automated pass over 12,500 words introduced errors at
roughly the rate it fixed them in that one category, and reported none of them.

### The audit disagreed with itself three times

The report, the `--stiff` lister and the fixer each ended up with their own copy
of the guard regex, so they gave different answers to the same question. One of
them had a literal backspace byte in it where `` should have been, which
silently disabled the whole exclusion. There is now a single `GUARD` constant
and both paths use it.

A tool that contradicts itself is worse than no tool. Check the report and the
lister agree before trusting either.

### What reading found that measurement could not

- **A duplicated paragraph on a live page.** The blade putter's look block had
  *"Gold, 385 grams, and no interest in disappearing"* immediately after a
  sentence ending in the same nine words. It read as a copy-paste error.
- **Developer vocabulary in two form notices.** The Ambassador and Contact
  pages told visitors their fields were *"the markup for the Shopify build"*
  and that there was *"no server behind this file"*.
- **A line telling customers our policy was unfinished.** The FAQ said a
  shipping-cost case *"isn't written down yet"*.
- **Two more British spellings** the first sweep missed because its word list
  was too short: `kerbs`, and `off-centre` inside prose (the earlier pass had
  dismissed every `centre` as a CSS class name, which was true for nine of
  eleven).

### The lesson for the next pass

The script tells you which file to open. Everything that actually made the copy
worse — duplicated text, leaked internal language, broken grammar, a promise
that the policy is incomplete — was invisible to it.
