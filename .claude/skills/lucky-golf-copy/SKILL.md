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

## Before you hand it back

The voice lives in `references/how-we-write.md`. Its hard rules are not optional. Beyond those, check five things:

1. **Would the buddy say it out loud?** Pumped, loose, a little dumb. If it sounds like a brochure, a manual or a clever writer, redo it.
2. **Is it hype or explanation?** "Grabs the ball and checks it up like it hit a wall" is hype. "It's micro-grooved, so it creates more friction" is a manual. Say the result with energy; don't walk through the mechanism.
3. **Is the bit new?** One bit per product, done a different way from every other page on the site. Gold-gets-looks and big-names-charge-too-much are not the go-to joke.
4. **Does it flow?** One opener, a hyped middle in sentences that join up, maybe a light close. Not a joke in every line, not a two-word kicker after every sentence, not a stack of fragments.
5. **Is every fact in the Product Reference Guide?** If not, cut it or ask.

The approved lines in the tone guide are calibration. Hear them, don't reuse them. "It's better to be lucky" is the tagline and only goes where a tagline belongs.

## When in doubt

The tone guide has one closing line: *"If a piece of Lucky copy sounds like a person talking to a golfer who already knows the game, it's landing. If it sounds like an ad, if it sounds like a brochure, if it sounds like it's straining — start over."*

That's the bar. When any output feels off, ask whether it sounds like a person talking. If not, rewrite.
