"""
VOICE AUDIT — the measurable half of "does a person sound like they wrote this".

Cole, 2026-08-25: "Overall copy still doesn't sound like somebody is talking and
writing this, it sounds like you are following rules again. Be a PERSON and talk."

Judgement can't be automated. Two of its symptoms can:

  1. CONTRACTION DENSITY. The approved Our Story page runs about one contraction
     per 30 words. Copy that reads like a rulebook runs "that is not", "it is",
     "we do not" and lands nearer one per 200. This is the loudest single tell
     and it is trivially countable.

  2. STIFF FORMS. The specific pairs a person would always contract in speech.

What this CANNOT do is tell a good plain line from a dead one. That was tried
and it flagged 106 of 166 headings, most of them wrongly ("The stuff that wears
out first" is a fine line). Headings still need a human read; this script only
tells you which FILES to go and read.

    python tools/voice-audit.py            # every copy file, worst first
    python tools/voice-audit.py --stiff    # list the stiff phrases to fix
"""
import json, io, glob, os, re, sys

TARGET = 45          # words per contraction; approved Our Story sits near 30
FLOOR  = 60          # above this, a file reads stiff

STIFF = [
    (r"\bit is\b", "it's"), (r"\bthat is\b", "that's"), (r"\bthere is\b", "there's"),
    (r"\bhere is\b", "here's"), (r"\bwhat is\b", "what's"), (r"\byou are\b", "you're"),
    (r"\bthey are\b", "they're"), (r"\bwe are\b", "we're"), (r"\byou will\b", "you'll"),
    (r"\bwe will\b", "we'll"), (r"\byou have\b", "you've"), (r"\bdo not\b", "don't"),
    (r"\bdoes not\b", "doesn't"), (r"\bwill not\b", "won't"), (r"\bis not\b", "isn't"),
    (r"\bare not\b", "aren't"), (r"\bcannot\b|\bcan not\b", "can't"),
    (r"\bwas not\b", "wasn't"), (r"\bhave not\b", "haven't"), (r"\bwould not\b", "wouldn't"),
]
GUARD = r"(?=\s+(?!to\b)[a-z0-9$])"   # never before "to": "you have to" must not contract
CONTR = re.compile(r"\b\w+['\u2019](?:s|t|re|ve|ll|d|m)\b")
# strings that are markup, tokens, briefs or spec values, not prose
SKIP_KEY = re.compile(r"(brief|photo|src|alt|href|sku|img|code|k$|^id$|slug|label|cta)", re.I)


def prose(path):
    """Every editorial string in a copy file, minus underscore keys and non-prose."""
    d = json.load(io.open(path, encoding="utf8"))
    out = []

    def walk(o, key=""):
        if isinstance(o, dict):
            for k, v in o.items():
                if k.startswith("_"):
                    continue
                walk(v, k)
        elif isinstance(o, list):
            for v in o:
                walk(v, key)
        elif isinstance(o, str):
            if SKIP_KEY.search(key or ""):
                return
            if o.startswith(("{{", "http", "<")) or len(o.split()) < 6:
                return
            out.append(o)
    walk(d)
    return out


def report():
    rows = []
    for p in sorted(glob.glob("_src/data/copy/*.json")):
        txt = " ".join(prose(p))
        w = len(txt.split())
        if w < 60:
            continue
        c = len(CONTR.findall(txt))
        # Guarded exactly like the lister and the fixer: a stiff pair only
        # counts when a real word follows it. Sentence-final "the gap under
        # it is." is correct English and must never be counted as a fault.
        stiff = sum(len(re.findall(pat + GUARD, txt, re.I)) for pat, _ in STIFF)
        rows.append((round(w / max(c, 1)), w, c, stiff, os.path.basename(p)[:-5]))
    rows.sort(reverse=True)

    print("VOICE AUDIT — words per contraction, stiffest first")
    print("target %d or below, flagged above %d\n" % (TARGET, FLOOR))
    print("  %-30s %6s %6s %7s  %s" % ("file", "w/contr", "words", "stiff", ""))
    bad = 0
    for dens, w, c, stiff, name in rows:
        if stiff:
            flag, bad = "FIX  <- %d stiff forms" % stiff, bad + 1
        elif dens > FLOOR:
            flag = "read it"
        else:
            flag = ""
        print("  %-30s %6d %6d %7d  %s" % (name, dens, w, stiff, flag))
    print("")
    print("%d file(s) carry stiff forms and need fixing." % bad)
    print("Files marked 'read it' have no stiff forms but little contracted speech;")
    print("that is usually fine for spec copy. Go and read them, do not bulk-edit them.")
    return bad


def stiff_list():
    print("STIFF FORMS, by file\n")
    for p in sorted(glob.glob("_src/data/copy/*.json")):
        hits = []
        for s in prose(p):
            for pat, better in STIFF:
                # Same guard the fixer uses: only a real hit when a word follows.
                # Sentence-final "the gap under it is." must NOT be contracted,
                # and listing it as a hit just teaches people to ignore the tool.
                guarded = pat + GUARD
                for m in re.finditer(guarded, s, re.I):
                    hits.append((m.group(0), better, s[max(0, m.start()-40):m.end()+40]))
        if hits:
            print("### " + os.path.basename(p)[:-5] + "  (%d)" % len(hits))
            for was, better, ctx in hits[:6]:
                print('   %-10s -> %-9s ...%s...' % (was, better, re.sub(r"\s+", " ", ctx)))


if __name__ == "__main__":
    if "--stiff" in sys.argv:
        stiff_list()
    else:
        sys.exit(1 if report() else 0)
