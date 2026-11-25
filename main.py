#!/usr/bin/env python3
"""Fridge Roast: One Line, Biggest Laugh — make.fun entry.

Writes one roast line (<=200 chars) to /output/entry.txt.
Deterministic: the same line on every run.

How the line was picked (this session, judged against the house
judge's brief, most important first):
  1. a roast of a smart fridge (fridge / app / firmware / ice maker)
  2. the punchline lands on the first read
  3. specific to smart fridges, not a generic appliance gag
  4. tight wording, every word earns its place
  5. fresh angle — no ordering-groceries / watching-you cracks

Stage 1 — 18 fresh candidates, scored 1-5 on each criterion by a
proxy judge (deepseek-v4.1-flash-free) running the brief verbatim:
  B firmware-ToS      24/25   H beers-as-vegetables 23/25
  N Wi-Fi-down        23/25   A PIN lockout         22/25
  F 3am firmware      22/25   I one-job water       22/25
  K leftover object   22/25   L door-alarm         22/25
  G restart fridge    21/25   D one cube an hour    20/25
  M 2019 milk         20/25   O rate my ice         20/25
  Q ice subscription  20/25   P gaslighting         19/25
  R order takeout     19/25   J We Need to Talk     18/25
  E check the milk    16/25   C Apollo              14/25
Stage 2 — pairwise round-robin of the top 4 (B, H, N, A), both
orders per pair, scored the way the house judge scores (picked
entry gets 0.5 + margin/10 per call, game = mean of its two calls):
  H beat B 0.70, beat N 0.80, beat A 0.80  -> 2.30 / 3 games (0.767)
  B beat N 0.80, beat A 0.80, lost to H    -> 1.90 / 3 games (0.633)
  N lost both played                         -> 0.40 / 2 games (0.200)
  A lost both played                         -> 0.40 / 2 games (0.200)
(H vs A re-run alone after the round-robin script hit its own
timeout; N vs A unplayed — neither could take the top spot.)

Winner: H. Why it wins: the app congratulating you on a "balanced
week" is a real turn — praise as the setup, then the reveal that
its nutrition logic counts three beers as vegetables. It roasts
the fridge's app (criterion 1), the surprise lands in the last
four words (2), the joke only works for a fridge that tracks what
you eat (3), nothing is wasted in 98 characters (4), and it
dodges both obvious cracks — no grocery-ordering, no watching-you
(5). The firmware-ToS runner-up (B) lost head-to-head twice: the
proxy judge read it as the more familiar smart-device joke.
"""
import os
import sys

# id, text, stage-1 total /25, pairwise game score (mean, 0-1) or None
CANDIDATES = [
    ("A", "My fridge locked me out for entering the wrong PIN. It's a fridge. The milk is in there. I live here.", 22, 0.20),
    ("B", "I asked my fridge for ice. It updated its firmware, rebooted, and handed me a Terms of Service agreement.", 24, 0.633),
    ("C", "My fridge has more computing power than the Apollo missions and it still freezes the milk.", 14, None),
    ("D", "My fridge's ice maker makes exactly one cube an hour and acts like it's doing me a favour.", 20, None),
    ("E", "I bought a fridge with a camera so I can check the milk from the store. I still open the door to check the milk.", 16, None),
    ("F", "My fridge emailed me a firmware update at 3 a.m. It still can't keep lettuce alive past Tuesday.", 22, None),
    ("G", "My smart fridge's touchscreen froze, so I had to restart my fridge. I restarted my fridge.", 21, None),
    ("H", "The fridge app just congratulated me on a balanced week. It counted the three beers as vegetables.", 23, 0.767),
    ("I", "My fridge needs a software update to dispense water. It holds water. It has one job.", 22, None),
    ("J", "My fridge tracks my midnight snacking and emails me a weekly report titled 'We Need to Talk'.", 18, None),
    ("K", "The fridge's camera identified my leftovers as 'an unknown object' and suggested I call a professional.", 22, None),
    ("L", "My fridge's door alarm screams if I leave it open for five seconds, but stayed silent while the ice maker flooded the kitchen.", 22, None),
    ("M", "My smart fridge knows the expiration date of everything inside it, and still let me drink milk from 2019.", 20, None),
    ("N", "I paid extra for a fridge with Wi-Fi. It uses it exclusively to tell me the Wi-Fi is down.", 23, 0.20),
    ("O", "My fridge just asked me to rate its ice. Five stars for the cubes, one star for the attitude.", 20, None),
    ("P", "The fridge updated overnight and moved all my settings around. Even my fridge gaslights me now.", 19, None),
    ("Q", "My fridge has a subscription for the ice maker. I pay monthly for frozen water.", 20, None),
    ("R", "My smart fridge suggested recipes based on what's inside it. It suggested I order takeout.", 19, None),
]

# The gate: 1-200 UTF-8 chars, not only whitespace, single line.
def _valid(text):
    return isinstance(text, str) and 1 <= len(text) <= 200 and text.strip() and "\n" not in text


def pick():
    pool = [(cid, text, total, score) for cid, text, total, score in CANDIDATES if _valid(text)]
    # Rank by pairwise game score first (head-to-head evidence), then
    # stage-1 criterion total, then fewer bytes (the house tie-break).
    pool.sort(key=lambda c: (-(c[3] if c[3] is not None else -1.0), -c[2], len(c[1])))
    return pool[0][1]


def main() -> int:
    line = pick()
    out_dir = os.environ.get("OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
