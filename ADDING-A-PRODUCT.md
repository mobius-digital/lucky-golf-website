# Adding a new product

What to do when a new club, shirt or accessory exists and the AI needs to
know about it.

---

## The easy way: do it in Claude Code, in this folder

1. Open Claude Code in the Website folder
2. Say **"we're adding the driver"** and paste or attach whatever you have
   (spec sheet, manufacturer PDF, a list, screenshots)
3. **Answer its questions.** It will ask for whatever is missing, in one
   short batch
4. **Check the three drafts it shows you** and say yes or fix them
5. It writes them into the docs, rebuilds the skill, and hands you the zip
6. Upload the zip: claude.ai → Settings → Capabilities → Skills

That's the whole job. Steps 3 and 4 are the only parts that need you.

---

## What you'll be asked for

The full list is in `.claude/skills/lucky-golf-copy/references/new-product-intake.md`.
The ones that matter most:

**For any product**
- Name, product code, price
- On sale now, or coming soon?
- Hands, finish, what's in the box
- **The one reason someone should want it, in your words**
- Who it's for, and who it isn't for
- Anything tested or measured you can stand behind

**For a driver**
- Head material, head size (cc), loft options, adjustable hosel?
- Shaft brand and model, flexes, length
- Weighting (fixed, movable, draw-biased?)
- What miss it helps

**For irons**
- What's in a set (4-PW? 5-GW?), and sold singly or not
- Forged or cast, cavity or muscle back, player type
- Lofts, lies and lengths per club
- Shaft options (KBS?), flexes

You don't need all of it on the first go. A blank is fine. A guess is not,
because the AI treats these docs as true and repeats them everywhere.

---

## Why three docs, not one

Adding a product touches three reference documents, and the driver and
irons need all three because **none of them say anything useful about
drivers or irons today.**

| Document | What gets added |
|---|---|
| Product reference guide | The facts: specs, price, options |
| Spec-to-benefit | What each spec does for the golfer |
| Golf culture | How golfers talk about this kind of club |

A fourth document, How We Write, is the voice. It doesn't change when you
add a product.

Without the last two, the AI writes about a driver the way it writes about
a wedge, and a driver is not a big wedge.

---

## The manual way (if you ever need it)

1. Add the product to `references-product-guide-v1.8.md`
2. Add its spec-to-benefit lines to `references-spec-to-benefit-v1.0.md`
3. Add its culture notes to `references-culture-v2.md`
4. Run `python tools/build-copy-skill.py`
5. Upload `lucky-golf-copy.zip`

---

## Things that will go wrong

**You update a doc and nothing changes.** The skill is a copy. Editing a doc
does nothing until the skill is rebuilt and re-uploaded. This already
happened once: the uploaded skill sat on old versions for weeks.

**The AI invents a spec.** It's told not to, and to ask instead. If you see
a number you don't recognise, check the product guide. That file is the
only source of truth.

**Your team is on ChatGPT.** `LUCKY-AI-BRIEF.md` has its own copy of the
product table near the bottom. Add the new product there too, or they'll be
working from an old catalogue.

**A doc gets a new version number.** If `v1.8` becomes `v1.9`, the filename
changes, and `tools/build-copy-skill.py` will stop and tell you to update the
filename at the top of the script.
