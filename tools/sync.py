"""Pull the engine's `vine.py` and `grape.py` into this repo.

The islands do NOT come through here any more. They are written in this repo and
the engine vendors them at build time; see FROM_ENGINE_FOLDERS below.

    python tools/sync.py

Both files at the root of this repo are copies. The game writes its own into the
Python runtime before your island is imported, so at runtime the engine always
wins and a stale copy here cannot reach a player. What it CAN do is waste your
afternoon: you write `say(text, portrait=...)` against a copy that has an
argument the engine does not, your test goes green, and the game raises a
TypeError on a line that looks correct. That happened, on `say`, in this repo's
first commit.

So this copies them over, and `tests/test_vine_matches_the_engine.py` fails
when they differ, which is what turns "somebody remembers" into a check.

WHERE IT COPIES FROM. A checkout of the engine next door, which is Ash's
machine. A member has no engine checkout and does not need one: the copies in
this repo are already current when they clone it, and the only person who has to
run this is whoever just changed the engine.

    python tools/sync.py                     ../AdventureGame
    python tools/sync.py C:\\path\\to\\engine   somewhere else
    BLHS_GAME=... python tools/sync.py       or by environment
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# the engine's, copied here so an editor and an offline test can see the names
FROM_ENGINE = (("vine.py", "vine.py"), ("grape.py", "grape.py"))
# and the one that goes the other way. `islands.json` is the roster row a
# member's pull request adds, and it is edited HERE, in the repository a member
# actually opens. The engine reads its own copy at boot rather than asking GitHub
# for a roster on a school network, so the row has to cross, and this is the
# crossing. Ash runs it when he merges.
TO_ENGINE = (("islands.json", "src/game/roster/member-islands.json"),)

# THE ISLANDS THE VINE ITSELF WROTE NOW LIVE HERE, AND THE ARROW HAS TURNED.
#
# Ruled by Ash 2026-09-04 (the engine's docs/ops/BRIEF-YEAR-ONE.md, WHERE IT
# LIVES): "I wanted the entire continuation of the beach cutscene to be written
# in the 3rd repo, including all the maw work." So `islands/panther-maw` and
# `islands/castaway` are the ORIGINALS. This file used to copy panther-maw the
# other way and its comment claimed the engine was the master. It was, and it is
# not any more, and a stale comment saying otherwise is how somebody edits the
# wrong copy for an afternoon.
#
# They still have to reach the game, because a bound island is fetched from the
# game's own origin at `/grapes/<folder>/` rather than from GitHub on a school
# Chromebook. That crossing is no longer this script's job: the engine pulls
# them in at `npm run build` with `scripts/vendor-islands.mjs`, straight from
# this repository or from GitHub when there is no checkout beside it. Nothing
# here pushes an island into the engine, and nothing in the engine is edited.
#
# What that means for you day to day: commit and PUSH an island change here
# before you build the engine on Vercel, or the deploy reads a branch that does
# not have it yet and fails saying so.
FROM_ENGINE_FOLDERS = ()


def engine_dir(argv):
    if argv:
        return argv[0]
    return os.environ.get("BLHS_GAME") or os.path.join(os.path.dirname(HERE), "AdventureGame")


def copy(src, dst, label, arrow):
    """One file across, and one line saying whether it moved. Returns 1 if it did."""
    if not os.path.isfile(src):
        print("%-13s %s  the source is not there: %s" % (label, arrow, src))
        return 1
    with open(src, "rb") as f:
        new = f.read()
    old = open(dst, "rb").read() if os.path.isfile(dst) else None
    if new == old:
        print("%-13s %s  already the same" % (label, arrow))
        return 0
    shutil.copyfile(src, dst)
    print("%-13s %s  updated" % (label, arrow))
    return 1


def copy_folder(src, dst, label):
    """A whole island across. Returns 1 if anything moved.

    Every file that is in the source, and every file that is in the destination
    and NOT in the source goes. A stale module left behind is worse than a
    missing one: `tools/manifest.py` refuses a `.py` on disk that the manifest
    does not list, so a file this forgot to delete would fail the checker in this
    repo over a file nobody here wrote.
    """
    if not os.path.isdir(src):
        print("%-13s <-  the source is not there: %s" % (label, src))
        return 1
    if not os.path.isdir(dst):
        os.makedirs(dst)
    moved = 0
    want = sorted(n for n in os.listdir(src) if os.path.isfile(os.path.join(src, n)))
    for name in want:
        s, d = os.path.join(src, name), os.path.join(dst, name)
        new = open(s, "rb").read()
        old = open(d, "rb").read() if os.path.isfile(d) else None
        if new != old:
            shutil.copyfile(s, d)
            moved += 1
    for name in sorted(os.listdir(dst)):
        if name in want or name == "__pycache__":
            continue
        path = os.path.join(dst, name)
        if os.path.isfile(path):
            os.remove(path)
            moved += 1
    print("%-13s <-  %s" % (label, "updated" if moved else "already the same"))
    return 1 if moved else 0


def main(argv=()):
    game = engine_dir(list(argv))
    if not os.path.isdir(os.path.join(game, "src", "vine", "py")):
        print("no engine at %s" % game)
        print()
        print("This only runs on a machine with both repositories. If you are a")
        print("member, you do not need it: the copies in this repo are current.")
        return 1

    changed = 0
    for ours_name, theirs_rel in FROM_ENGINE:
        changed += copy(os.path.join(game, "src", "vine", "py", theirs_rel),
                        os.path.join(HERE, ours_name), ours_name, "<-")
    for ours_name, theirs_rel in TO_ENGINE:
        changed += copy(os.path.join(HERE, ours_name),
                        os.path.join(game, *theirs_rel.split("/")), ours_name, "->")
    for folder, theirs_rel in FROM_ENGINE_FOLDERS:  # empty since 2026-09-05, see above
        changed += copy_folder(os.path.join(game, *theirs_rel.split("/")),
                               os.path.join(HERE, "islands", folder), folder)

    if changed:
        print()
        print("Run `python -m unittest` before you commit. The tests here compare")
        print("both copies of every one of these byte for byte, so a half-finished")
        print("sync fails loudly instead of sitting there looking done.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
