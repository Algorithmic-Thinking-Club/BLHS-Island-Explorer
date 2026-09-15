"""Copy the engine's `vine.py` and `grape.py` into this repo.

Run it on a machine that has both repositories, then run the tests.

    python tools/sync.py                     the engine next door
    python tools/sync.py C:\\path\\to\\engine   somewhere else
    BLHS_GAME=... python tools/sync.py       or by environment
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# the engine's, copied here so an editor and an offline test can see the names
FROM_ENGINE = (("vine.py", "vine.py"), ("grape.py", "grape.py"))
# and the one that goes the other way: `islands.json` here is the roster the
# engine reads as `member-islands.json`, and it is edited here
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
        print("Run `python -m unittest` before you commit. The tests here compare")
        print("both copies of every one of these byte for byte, so a half-finished")
        print("sync fails loudly instead of sitting there looking done.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
