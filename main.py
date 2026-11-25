#!/usr/bin/env python3
"""One-line office joke entry.

Writes a single original one-line joke about office life (at most
200 characters) to /output/entry.txt.

How it picks the line: twelve original candidate jokes, each written
for this entry, are scored against the judge's five criteria, in the
judge's own order of importance:

  1. it is a one-line joke about office life (setup + punchline)
  2. it is funny (the punchline surprises and pays off)
  3. it is one line (a single sentence, no rambling)
  4. it is fresh (a specific detail, not a joke everyone has heard)
  5. it is clear on first read (tight wording, no explanation needed)

Each criterion is rated 0-5 and weighted 3, 4, 2, 3, 2, matching the
judge's priority order. The highest total wins; ties go to the
earliest candidate in the list, so the choice is fully deterministic.

Freshness is not only hand-rated: any candidate that leans on a
tired office-joke trope loses one freshness point per trope phrase
found in its own text (clamped at zero), so a line everyone has
already heard cannot win on a generous hand rating alone.

No network, no external input, no randomness. The program verifies
its own output (1-200 characters, a single line, UTF-8) and prints
the SHA-256 of the file it wrote.
"""

from hashlib import sha256
from os import environ, makedirs
from sys import exit as finish, stderr

# Weights for the five judge criteria, in the judge's priority order:
# joke, funny, one-line, fresh, clear.
WEIGHTS = (3, 4, 2, 3, 2)

# Overused office-joke tropes. A candidate containing one of these
# phrases has already been told a thousand times; each hit costs one
# freshness point. Matched case-insensitively against the text itself.
CLICHES = (
    "could have been an email",
    "drowning in work",
    "per my last email",
    "reply all",
)

# Each candidate: (text, (joke, funny, one-line, fresh, clear)).
# All twelve lines are original, written for this entry.
CANDIDATES = [
    (
        "Our team building exercise was trust falls, which is fitting, "
        "because since the reorg nobody trusts anyone and we are all "
        "falling behind.",
        (4, 3, 3, 3, 3),
    ),
    (
        "The printer only jams when I am already late, which I now list "
        "on my CV under reliable colleagues.",
        (4, 3, 4, 2, 4),
    ),
    (
        "I asked IT for a second monitor and got a second ticket number "
        "instead.",
        (5, 4, 5, 4, 5),
    ),
    (
        "My out-of-office reply is the only email I write that anyone "
        "actually reads.",
        (4, 3, 5, 3, 5),
    ),
    (
        "The office plants died, so facilities replaced them with a "
        "poster of a plant and a form to request watering the poster.",
        (5, 4, 3, 5, 3),
    ),
    (
        "I put excellent multitasker on my CV because I can attend a "
        "meeting, answer emails, and quietly panic all at once.",
        (5, 4, 4, 3, 4),
    ),
    (
        "Our boss said the door is always open, so I asked for a raise "
        "through it and he closed it for a quick sync.",
        (5, 4, 4, 3, 4),
    ),
    (
        "The Wi-Fi password changes every month, but the password to get "
        "anyone to reply to an email remains unsolved.",
        (4, 3, 4, 3, 4),
    ),
    (
        "I joined the meeting five minutes early just to watch the little "
        "squares fill up like a very boring advent calendar.",
        (4, 4, 4, 4, 3),
    ),
    (
        "HR called my burnout an engagement opportunity and offered me a "
        "webinar about resilience instead of a holiday.",
        (5, 4, 3, 4, 4),
    ),
    (
        "My keyboard's escape key is worn out, which feels like the most "
        "honest performance review this company has ever given me.",
        (5, 4, 4, 5, 4),
    ),
    (
        "The meeting could have been an email, the email could have been "
        "a Slack message, and the Slack message could have been silence.",
        (4, 3, 4, 1, 5),
    ),
]


def rate(text, ratings):
    """Weighted total for one candidate's five criterion ratings.

    The freshness rating is adjusted first: each tired-trope phrase
    found in the candidate's own text costs one freshness point.
    """
    joke, funny, one_line, fresh, clear = ratings
    lowered = text.lower()
    hits = sum(1 for phrase in CLICHES if phrase in lowered)
    fresh = max(0, fresh - hits)
    adjusted = (joke, funny, one_line, fresh, clear)
    return sum(w * r for w, r in zip(WEIGHTS, adjusted))


def choose(candidates):
    """Return (index, text, total) of the best candidate.

    Deterministic: strictly greater totals replace the leader, so the
    earliest candidate wins any tie.
    """
    best_index, best_text, best_total = -1, "", -1
    for index, (text, ratings) in enumerate(candidates):
        total = rate(text, ratings)
        if total > best_total:
            best_index, best_text, best_total = index, text, total
    return best_index, best_text, best_total


def gate(text):
    """Gate the chosen line the way the sealed scorer does."""
    if not (1 <= len(text) <= 200):
        return "length %d is outside 1..200 characters" % len(text)
    if text.strip() != text or not text.strip():
        return "entry is blank or has surrounding whitespace"
    if "\n" in text or "\r" in text:
        return "entry is not a single line"
    return None


def run():
    index, text, total = choose(CANDIDATES)
    problem = gate(text)
    if problem is not None:
        print("self-check failed: %s" % problem, file=stderr)
        return 1

    out_path = environ.get("OUTPUT_PATH", "/output/entry.txt")
    out_dir = out_path.rsplit("/", 1)[0] if "/" in out_path else ""
    if out_dir:
        makedirs(out_dir, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as handle:
        handle.write(text)
    digest = sha256(text.encode("utf-8")).hexdigest()
    print("candidate %d of %d, score %d" % (index + 1, len(CANDIDATES), total))
    print("entry: %s" % text)
    print("sha256: %s" % digest)
    return 0


finish(run())
