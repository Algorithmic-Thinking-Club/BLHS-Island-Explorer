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
FILES = ("vine.py", "grape.py")


def engine_dir(argv):
    if argv:
        return argv[0]
    return os.environ.get("BLHS_GAME") or os.path.join(os.path.dirname(HERE), "AdventureGame")


def main(argv=()):
    game = engine_dir(list(argv))
    src = os.path.join(game, "src", "vine", "py")
    if not os.path.isdir(src):
        print("no engine at %s" % src)
        print()
        print("This only runs on a machine with both repositories. If you are a")
        print("member, you do not need it: the copies in this repo are current.")
        return 1

    changed = 0
    for name in FILES:
        theirs = os.path.join(src, name)
        ours = os.path.join(HERE, name)
        if not os.path.isfile(theirs):
            print("%-9s the engine does not have this file" % name)
            changed += 1
            continue
        with open(theirs, "rb") as f:
            new = f.read()
        old = open(ours, "rb").read() if os.path.isfile(ours) else None
        if new == old:
            print("%-9s already the same" % name)
            continue
        shutil.copyfile(theirs, ours)
        print("%-9s updated" % name)
        changed += 1

    if changed:
        print()
        print("Run `python -m unittest` before you commit: vine.py is deliberately")
        print("nine of the engine's fifteen words, so a copy of the whole file will")
        print("fail the test that says which nine this repo hands members.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
