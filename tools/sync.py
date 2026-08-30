"""Pull the engine's `vine.py` and `grape.py` into this repo.

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

    if changed:
        print()
        print("Run `python -m unittest` before you commit: vine.py is deliberately")
        print("nine of the engine's fifteen words, so a copy of the whole file will")
        print("fail the test that says which nine this repo hands members.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
