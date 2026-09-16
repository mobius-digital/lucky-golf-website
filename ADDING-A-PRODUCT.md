# Adding a new product

What to do when a new club, shirt or accessory exists and the AI needs to know
about it. Written for a driver or an iron set, but it works for anything.

---

## The short version

1. Add the specs to **`references-product-guide-v1.8.md`**
2. Run **`python tools/build-copy-skill.py`**
3. Upload **`lucky-golf-copy.zip`** at claude.ai → Settings → Capabilities → Skills

That's it. Step 1 is the only part that takes thinking.

---

## Step 1: write down the specs

Open `references-product-guide-v1.8.md` and add the product under the right
category heading. Copy the shape of an existing entry. For a club that means:

    LGD01 Lucky Driver
    Category: driver
    Head material: ...
    Head size: ...
    Loft options: ...
    Shaft: ...
    Flex options: ...
    Hand: ...
    Headcover: ...
    Price: $...

Two rules that matter more than the format:

- **Only write down what you actually know.** A blank is fine. A guess is not,
  because the AI treats this file as true and will repeat it everywhere.
- **If you invent a new kind of field** (a driver has "head size" and no wedge
  does), that is fine. Just add it.

If the whole category is new, add a new heading for it, and add the category
to the line near the top of the file that lists what Lucky sells.

## Step 2: rebuild the skill

In the Website folder:

    python tools/build-copy-skill.py

It copies the four reference docs into the skill, checks the zip is one
Claude will accept, and prints what went in. If a doc gets renamed in a
version bump (`v1.8` becomes `v1.9`), the script will stop and tell you to
update the filename at the top of `tools/build-copy-skill.py`.

## Step 3: upload it

claude.ai → Settings → Capabilities → Skills → replace `lucky-golf-copy`
with the new `lucky-golf-copy.zip`.

**Check it worked:** open a new chat and ask *"what does Lucky sell?"* The new
product should be in the answer.

---

## Why this is more than a spec sheet

The skill now carries four documents, and a new product needs all four:

| Document | What it does for a new product |
|---|---|
| Product reference guide | What is true. Specs, price, options. |
| How We Write | How Lucky sounds. Unchanged by a new product. |
| Spec-to-benefit | Turns "450cc titanium" into a reason to buy. |
| Golf culture | How golfers actually talk about this kind of club. |

The last two matter most for a category Lucky has never sold. There is no
existing driver copy for the AI to imitate, so without them it will write
about a driver the way it writes about a wedge, and a driver is not a big
wedge. The skill has instructions telling it to open both before drafting.

---

## Things that will go wrong

**The AI invents a spec you never supplied.** It is told not to, and to ask
instead. If you see a number you do not recognise, check it against the
product guide. That file is the only source of truth.

**You update the doc and nothing changes.** You skipped step 2 or step 3. The
skill is a copy; editing the repo doc alone does nothing until it is rebuilt
and re-uploaded. This exact drift already happened once: the uploaded skill
sat on How We Write v6 and Product Guide v1.1 for weeks after v8.1 and v1.8
were written.

**People outside Claude need the specs too.** `LUCKY-AI-BRIEF.md` has its own
copy of the product facts, in a table near the bottom. Update that table when
you add a product, or your team pasting it into ChatGPT will be working from
an old catalogue.
