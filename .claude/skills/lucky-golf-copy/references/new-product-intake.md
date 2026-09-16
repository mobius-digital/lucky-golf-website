# New product intake

Use this when someone gives you specs for a product Lucky has not sold
before, or says "we're adding X". Your job is to turn what they give you
into three additions, one for each reference document, and to ask for
whatever is missing instead of guessing.

Nothing here gets written into copy until the intake is done and the person
has confirmed the three additions.

---

## How to run it

1. **Read what they gave you.** A spec sheet, a manufacturer PDF, a list, a
   screenshot. Pull out every fact you can.
2. **Check it against the question list below** for that category. Mark each
   question: answered, not answered, or not applicable.
3. **Ask the missing questions in one short batch.** Group them. Put the ones
   that block copy first (price, what it is, who it's for). Never more than
   about eight at once. If something is optional, say so.
4. **Draft the three additions** once you have enough:
   - a **product guide entry** (facts only, in the same shape as existing
     entries)
   - **spec-to-benefit lines** (each spec paired with what it does for the
     golfer, plainly)
   - **culture notes** (how golfers talk about this kind of club, the shot it
     lives on, the miss it's for)
5. **Show all three and ask for a yes.** Mark anything you inferred rather
   than were told, so it can be checked.
6. **Tell them the next step:** these go into the repo's reference docs, then
   `python tools/build-copy-skill.py`, then re-upload the zip. Until that
   happens, the skill does not know the product in future chats.

Never invent a number. A blank in the product guide is fine. A guessed spec
gets repeated everywhere.

---

## Questions for any product

- Name and product code (for example LGD01)
- Price. One price, or does it vary by option?
- Is it on sale now, pre-order, or coming? If coming, roughly when?
- Which hands: right, left, both?
- What colour or finish? Is it gold?
- What's in the box? (Headcover? Tool? Anything else?)
- **The one reason someone should want this.** In their words, not ours.
- Who is it for, and who is it NOT for?
- Anything that has been tested or measured that we can say out loud? Real
  numbers only.
- What does a comparable big-name version cost? (Only if they know. Used on
  the comparison page.)

## Driver

- Head material (titanium? carbon crown?)
- Head size in cc
- Loft options, and is the hosel adjustable? If so, what range?
- Face: material and any face technology (variable thickness, etc.)
- Weighting: fixed or movable weights? Draw-biased, neutral, fade?
- Shaft: brand and model, flex options, weight, length
- Grip: brand and model, size
- Swing weight / total weight if known
- What miss does it help: slice, low launch, heel/toe strikes?
- Swing speed or player type it suits
- Sound and feel, if they have a view (drivers get judged on sound)

## Irons

- What's in a set? (4-PW, 5-PW, 5-GW?) Can clubs be bought singly?
- Price per set, and per club if sold singly
- Construction: forged or cast? Cavity back, muscle back, hollow body?
- Head material, and face material if different
- Player type: game improvement, players distance, or players iron?
- Lofts, lies and lengths for each club (a table is ideal)
- Offset, and does it change through the set?
- Any tungsten or perimeter weighting?
- Shaft options: brand and model (KBS?), steel or graphite, flex options
- Grip: brand and model, size options
- Can lie, loft or length be adjusted before shipping, or stock only?
- Finish: gold, chrome, black?
- How golfers try them: the return policy lets one 7-iron be hit on a mat,
  the rest stay sealed. Confirm that still applies.

## Fairway woods and utility irons

Same as driver, plus: what gap does it fill, and which club does it replace?

## Apparel and accessories

- Material and weight, fit, sizes, care instructions
- What makes this one worth having over the one they already own
- For a print or design: what it looks like, in plain words
