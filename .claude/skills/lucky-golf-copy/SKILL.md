---
name: lucky-golf-copy
description: Write copy in the Lucky Golf brand voice for any format — product descriptions, feature callouts, ad headlines, ad copy, email subject lines, email openers, email body, landing page copy, social captions, video scripts, product tiles, drop announcements, homepage copy, or anything else Lucky Golf publishes. Trigger whenever the user asks for copy, writing, or drafts related to Lucky Golf, Lucky Wedges, LGW01, LGW02, LGH01, LGP01, LGP02, the Carver, the Eclipse (formerly Tracer), the Tracer, the Stryker, the Havoc driver, the Classic Polo, the Blade Polo, or any Lucky Golf product. Also trigger when the user asks to rewrite, edit, or improve existing Lucky Golf copy. Use this skill even when the user doesn't explicitly ask for a "skill" — any Lucky Golf copy task should route through here to ensure the tone, product facts, and format-specific handling stay consistent.
---

# Lucky Golf Copy

The purpose of this skill is to write copy in Lucky Golf's brand voice. Whatever the format — a product description, an ad headline, an email opener, a social caption — the tone stays the same. The shape changes based on the piece.

## First step, every time

There are four reference documents. Two are read every single time; two are opened when the task needs them.

**Always, before writing a word:**

- **`references/how-we-write.md`** — the tone guide. How Lucky sounds. It's short.
- **`references/product-reference-guide.md`** — the fact lookup. Specs, materials, construction terms, prices, CTA options per club family. Verify every fact against it. **Do not use it as an outline. Do not summarize it. Do not let its structure become the structure of the copy.**

**When the piece is about a specific product:**

- **`references/spec-to-benefit.md`** — how a spec becomes a reason to buy. Open this whenever you are about to write a number, a material or a construction detail into copy. A spec on its own is a datasheet; this is the document that turns it into something a golfer wants. It is especially important for a product with no existing Lucky copy to imitate, like a new club category.
- **`references/golf-culture.md`** — how golfers actually talk. Open this when the piece needs the vernacular: what a shot is called, what the miss feels like, what a golfer would say about this club in a group chat. Use it to sound like someone who plays, not to sprinkle slang. Forced vocabulary is worse than plain description.

**The hierarchy, when they seem to disagree:** the product reference guide wins on what is TRUE. The tone guide wins on how it SOUNDS. Spec-to-benefit and culture are raw material for the writer, never phrasing to copy out. If a line from any of them appears verbatim in published copy, that is a failure.

## When someone brings a new product

If the user gives you specs for something Lucky hasn't sold before, or says they're adding a product (a driver, an iron set, a new category), **do not write copy yet.** Open `references/new-product-intake.md` and run the intake: pull out what they gave you, ask for what's missing in one short batch, then draft the additions to all three reference docs (product guide, spec-to-benefit, culture) and get a yes before anything else. The three docs have almost nothing on drivers or irons today, so skipping the intake means writing from nothing.

## Writing about a product that has no copy yet

When a product exists in the product reference guide but has no Lucky copy yet (a driver, an iron set, a new category), do not pattern-match off an existing club. A driver is not a big wedge.

1. Read that product's entry in the product reference guide in full.
2. Open **spec-to-benefit** and work out what each spec actually does for the golfer. Write those out for yourself before drafting.
3. Open **golf-culture** for how this club gets talked about. A driver lives in a different part of the round than a wedge and the language follows.
4. Ask what the single reason to want this club is, and write to that. Everything else supports it.
5. If a fact you need is not in the reference guide, say so and ask. Never fill the gap by guessing at a spec.

## The core principle

Lucky Golf's tone stays consistent across every format. What changes is the **shape** the copy takes. A description flows longer than an ad. A subject line lands in a few words. A caption sits on one line. Same voice, different shapes.

Never let the AI default behavior (thorough, feature-summarizing, exhaustive) override what the piece actually needs. **Descriptions describe, they don't list features. Ads are short and sharp. Emails talk to the reader. Feature callouts can be feature-forward because that's what they're for.**

## Format-specific handling

Different pieces of copy have different jobs. Read `references/prompt-patterns.md` for guidance on each format the skill covers. That file describes what each type of piece **is for** — not how to structure it, but what the reader should feel or do when they see it. Consult it whenever the user asks for a specific format so the copy fits its purpose.

The formats covered:
- Product descriptions (short and long)
- Feature callouts / benefit blocks
- Ads: the parts list (headline, subline, callouts, annotations, offer badge, button, panels, primary text) and the register menu
- Email subject lines
- Email openers / hooks
- Email body
- Email CTAs
- Landing page hero
- Landing page body sections
- Product tile / card copy
- Social captions (feed, story)
- Video scripts (short-form and spoken)
- Drop announcements
- Homepage copy
- PDP (product detail page) sections
- Return / policy / support copy

If a format isn't explicitly covered in `prompt-patterns.md`, use the tone guide and the closest format's guidance as a reference. The tone guide is the constant.

## Working from inspiration

When the user provides reference copy from another brand (a Takomo ad, a Vice email, a Nike headline) and asks for a Lucky version, load `references/prompt-patterns.md` and follow the "Working from inspiration" section. The core rule: translate the underlying move (angle, hook, structural approach), not the surface language (specific phrases, brand-invented terms, cultural anchors). See the worked example in `prompt-patterns.md` for how to break down a source and produce a Lucky version.

## Common failure modes and how to catch them

The AI's default behavior tends toward these mistakes when writing Lucky Golf copy. Watch for them, and rewrite when they show up.

**Descriptions that read like features summaries.** If a product description lists three or four features in sequence, it's a features summary, not a description. Rewrite as a short, flowing piece that promises something the golfer wants and makes them curious about the club — the feature callouts elsewhere on the page will handle the specs.

**Copy that opens with construction.** "CNC-milled from 304 stainless steel with a slight toe hang" is a spec, not a hook. Lead with what the club does for the golfer, then support with construction. Construction belongs after the promise, not before it.

**Choppy fragments.** Fragments and parallel beats are moves for specific spots — headlines, taglines, an occasional short line. They're not the default sentence shape. When every line is a fragment, the copy stops sounding like a person and starts sounding like a brochure that got chopped up to look edgy.

**Forced personality.** Not every piece needs a wink. A quiet product page or a factual email can close without a joke. If a line requires an exclamation point or an emoji to land, it doesn't land.

**Copy that pressures.** Lucky is excited about its gear, never pushy. Enthusiasm is fine. Urgency, begging and hard sells are not. If the copy feels like it's pressuring, rewrite it plainer.

**Parroting reference-guide phrasing.** The Feature → Benefit pairs in the product reference guide are reference material for the writer. They are not sentences to paste into copy. Translate them into flowing prose. Never copy a line from the reference guide verbatim into published copy.

**Templating.** If the same structure appears across multiple pieces (same opening move, same closing rhythm, same phrase in the same spot), the AI is templating instead of writing. Break the pattern. The tone stays the same across formats; the structure should not.

## The measurable checks (added 2026-08-29, from the site-wide voice pass)

These came out of rewriting the whole website until Cole signed off. Run them on your OWN draft before returning it. Each one is concrete.

**1. Count your contractions.** Approved Lucky copy runs about one contraction per 30 words. Copy that reads like a rulebook runs "that is not", "it is", "we do not" and lands near one per 200. Under one per 40 words: go back and fix it. Two exceptions: never contract at the end of a sentence ("the gap under it is." is correct), and never before "to" ("you have to baby" must not become "you've to baby").

**2. No caption headings.** A heading that describes the block it sits on ("One wedge, side by side", "The Lucky timeline") is furniture labelling, not talking. A heading says something ("Spot the difference"). Functional labels (spec rows, nav) are correctly plain; leave those alone.

**3. No meta.** Any sentence describing the writing or the layout itself ("Bounce, in one paragraph") gets cut. Say the thing, never narrate saying it.

**4. Second sentences must turn.** Two plain statements in a row where the second restates the first is the flat double-statement, Cole's most-hated failure. If it doesn't turn, sharpen or pay off the first, cut one.

**5. Say the spec, don't explain it.** "It's micro-grooved," not "tiny grooves milled between the main ones." A golfer says the word with pride; the AI translates it into a manual.

**6. Never list product categories in copy meant to last.** "Wedges, putters and a hybrid" dates the page the day irons and drivers ship.

**7. Ads start from an angle.** Before writing an ad, ask what the angle is. The voice carries into ads; the angle decides what the ad says.

**8. Watch for lists of three.** One is fine. Three in a piece is an AI habit.

**9. Two bits, max, in a description.** A hook up top and maybe one closer. A third joke means the middle has stopped doing its job.

**10. Never sell a putter on its weight.** Feel, roll and looks, not grams.

**11. On a page or a long email, count the bits.** One big moment and one light touch for the whole piece. More than two means cut the extras to straight. The product's big idea appears once, and no feature is explained in more than two places.

**Banned outright:** "milled from a single block" or "one block of" anything (say "fully milled"). Mentioning which hand a club is for ("lefties, this one's yours too"): never call it out in copy; the option picker handles it. The words premium, cheap, luxury, revolutionary. Em dashes (Cole banned them 2026-08-15; use a period, comma, colon or parentheses). Exclamation marks. Naming a competitor (say "the big names"). Any price, percentage or multiplier not in the product reference guide, and any invented proof number (real Judge.me or Shopify numbers are fine). The founder's name, anywhere.

**Rule Zero for the tone guide's example lines:** the approved lines quoted in how-we-write are calibration, not a phrase bank. Never reuse a phrase or construction from them. If a reader of the Lucky site could tell you copied a line, rewrite it. "It's better to be lucky" is the tagline and appears only where a tagline belongs.

**Last, always: read it aloud.** Would you say this to a golfer standing next to you? If you would pause, or it sounds announced rather than said, it's not finished.

## When in doubt

The tone guide has one closing line: *"If a piece of Lucky copy sounds like a person talking to a golfer who already knows the game, it's landing. If it sounds like an ad, if it sounds like a brochure, if it sounds like it's straining — start over."*

That's the bar. When any output feels off, ask whether it sounds like a person talking. If not, rewrite.
