#!/usr/bin/env python3
"""One Word From Grandma — score candidate words, write the winner.

The bounty asks for exactly one word: the word a grandma would text
about AI. The gate is strict — /output/entry.txt must be UTF-8 text of
1 to 30 characters, not only white space, and a single word. The judge
weighs, most important first: (1) reads as the single word a grandma
would text about AI, (2) sounds like a real grandmother's texting
voice, warm and a little baffled, (3) funny in one word, (4) tied to
AI, robots or machines, (5) a fresh pick, still instantly readable.

Each candidate is scored 0-5 on each criterion, weighted 5/4/3/2/1 in
the brief's own order. The highest total wins; ties break toward the
shorter word, then the earlier candidate.
"""

import os

# (word, c1 grandma-word, c2 grandma-voice, c3 funny, c4 AI-tied, c5 fresh)
CANDIDATES = [
    # "Robit": the typo a grandma actually makes typing "robot" on a
    # phone keyboard — warm, baffled, unmistakably about a machine,
    # and not the obvious straight spelling of "robot".
    ("Robit", 5, 5, 5, 5, 4),
    # "Doohickey": a classic grandma word for a gadget she cannot
    # name — great voice, but it would fit any gadget, not just AI.
    ("Doohickey", 4, 5, 4, 2, 3),
    # "Computery": grandma turning a noun into an adjective because
    # she is not sure what the thing is called — decent, but flat.
    ("Computery", 4, 4, 3, 4, 3),
    # "Thingamajig": pure grandma vocabulary, but it names nothing
    # about AI at all — fails the tied-to-AI criterion.
    ("Thingamajig", 4, 5, 3, 1, 2),
    # "Siri": a real AI name a grandma might text, but it is the
    # obvious pick and carries no joke on its own.
    ("Siri", 4, 2, 2, 5, 2),
    # "Beepboop": a robot sound, not a word a grandma would text;
    # cute, but it sounds like the machine, not like grandma.
    ("Beepboop", 3, 2, 4, 4, 3),
    # "Gizmo": grandma-adjacent gadget word, but it is the kind of
    # word a grandchild says, not one grandma texts about AI — and
    # it names no machine in particular.
    ("Gizmo", 3, 3, 2, 2, 3),
]

WEIGHTS = (5, 4, 3, 2, 1)


def score(candidate):
    word, *marks = candidate
    return sum(m * w for m, w in zip(marks, WEIGHTS))


def gate(word):
    """The brief's gate: 1-30 chars, UTF-8, not only whitespace, one word."""
    if not word or len(word) > 30:
        return False
    if word != word.strip() or not word.strip():
        return False
    if any(ch.isspace() for ch in word):
        return False
    word.encode("utf-8")
    return True


def main():
    ranked = []
    for cand in CANDIDATES:
        word = cand[0]
        assert gate(word), f"candidate fails gate: {word!r}"
        ranked.append((score(cand), -len(word), cand))
    # Highest score wins; ties break toward the shorter word.
    ranked.sort(key=lambda item: (item[0], item[1]), reverse=True)
    winner = ranked[0][2][0]
    assert gate(winner)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "entry.txt"), "w", encoding="utf-8") as fh:
        fh.write(winner)
    print(f"winner: {winner} (score {ranked[0][0]})")
    for total, _neglen, cand in ranked:
        print(f"  {total:3d}  {cand[0]}")


if __name__ == "__main__":
    main()
