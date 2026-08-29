"""THE PACKAGE FORMAT, written down as the thing that refuses.

An island is a folder with an island.json in it. This file is what "a folder
with an island.json in it" actually means, and it is here rather than in a
document because a document does not stop anybody.

Run it on everything in the repo:

    python tools/manifest.py

Every complaint names the field. A loader that says "invalid manifest" has told
you nothing; a loader that says `modules` lists questions.py, which is not in
this folder has told you what to do next.

The engine runs the same rules on the other side, when it fetches your island
off your branch. Failing here means failing there, which is the point: find it
on your own machine in a second instead of in the game in a minute.
"""
import json
import os
import re
import sys

# lower case, digits, single hyphens. The same shape the roster's ids are in,
# and safe as a folder name, a URL segment and a filename on every machine.
SLUG = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")

# THE FORMAT VERSION. It is not decoration. Two repositories ship on different
# days, and the day the format changes this number is how a member finds out
# their island needs an edit instead of watching it fail strangely.
FORMAT = 1

REQUIRED = ("format", "programme", "map", "title", "owner", "entry", "modules")
OPTIONAL = ("season",)
SEASONS = ("Fall", "Winter", "Spring")

# the engine writes its own copy of both of these into the runtime before your
# island is imported. A member shipping one would shadow the real thing with a
# stale copy and spend an afternoon on it.
ENGINE_OWNED = ("vine.py", "grape.py")


def faults(folder):
    """Every reason this folder is not a loadable island. Empty means it is one."""
    out = []
    name = os.path.basename(os.path.normpath(folder))
    if not SLUG.match(name):
        out.append("the folder name %r is not a slug: lower case, digits and single hyphens" % name)

    path = os.path.join(folder, "island.json")
    if not os.path.isfile(path):
        return out + ["there is no island.json here, so nothing knows this is an island"]

    try:
        with open(path, encoding="utf-8") as f:
            m = json.load(f)
    except ValueError as e:
        return out + ["island.json is not valid JSON: %s" % e]
    if not isinstance(m, dict):
        return out + ["island.json has to be an object, not a %s" % type(m).__name__]

    for key in REQUIRED:
        if key not in m:
            out.append("`%s` is missing, and it is required" % key)
    for key in m:
        if key not in REQUIRED and key not in OPTIONAL:
            out.append("`%s` is not a field this format has" % key)
    if out:
        # everything below reads fields; complaining about their contents while
        # the shape is still wrong buries the one line that matters
        return out

    if m["format"] != FORMAT:
        out.append("`format` is %r; this repo speaks format %d" % (m["format"], FORMAT))

    for key in ("programme", "map"):
        if not isinstance(m[key], str) or not SLUG.match(m[key]):
            out.append("`%s` is %r, which is not a slug" % (key, m[key]))
    # THE KEY SPACES STAY DISJOINT. A programme is a thing you do; a map is a
    # painting. The roster refuses an id that is both, so an island that ships
    # one is an island that can never be added to the roster.
    if m["programme"] == m["map"]:
        out.append("`programme` and `map` are both %r; they are different key spaces "
                   "and the roster refuses an id that is in both" % m["map"])

    for key in ("title", "owner"):
        if not isinstance(m[key], str) or not m[key].strip():
            out.append("`%s` is empty, and somebody has to be able to read it" % key)

    if "season" in m and m["season"] not in SEASONS:
        out.append("`season` is %r; it has to be one of %s, or left out when your "
                   "island is not seasonal" % (m["season"], ", ".join(SEASONS)))

    out.extend(_module_faults(folder, m))
    return out


def _module_faults(folder, m):
    out = []
    mods = m["modules"]
    if not isinstance(mods, list) or not mods:
        return ["`modules` has to list every .py file the engine should fetch"]

    for name in mods:
        if not isinstance(name, str) or not name.endswith(".py"):
            out.append("`modules` has %r in it, which is not a .py filename" % name)
        elif "/" in name or "\\" in name:
            out.append("`modules` has %r in it; a module is a filename, and an island "
                       "is one flat folder" % name)
        elif name in ENGINE_OWNED:
            out.append("`modules` lists %s, which the game provides. Yours would be "
                       "ignored at best and shadow the real one at worst" % name)
        elif not os.path.isfile(os.path.join(folder, name)):
            out.append("`modules` lists %s, which is not in this folder" % name)
    if len(set(mods)) != len(mods):
        out.append("`modules` lists the same file twice")

    entry = m["entry"]
    if entry not in mods:
        out.append("`entry` is %r, which is not one of the modules" % entry)

    # A FILE NOBODY LISTED IS A FILE THAT IS NEVER FETCHED. The island imports
    # it, the import fails inside the game and nowhere else, and the traceback
    # points at a line that is correct. Cheapest possible thing to catch here.
    on_disk = sorted(f for f in os.listdir(folder) if f.endswith(".py"))
    for f in on_disk:
        if f not in mods:
            out.append("%s is in this folder but not in `modules`, so the game never "
                       "fetches it and the import fails only inside the game" % f)
    return out


def islands(repo=None):
    """Every island folder in the repo, in order."""
    root = os.path.join(repo or _repo(), "islands")
    if not os.path.isdir(root):
        return []
    return [os.path.join(root, n) for n in sorted(os.listdir(root))
            if os.path.isdir(os.path.join(root, n))]


def collisions(repo=None):
    """Two islands claiming the same programme or the same map."""
    out = []
    for key in ("programme", "map"):
        seen = {}
        for folder in islands(repo):
            path = os.path.join(folder, "island.json")
            if not os.path.isfile(path):
                continue
            with open(path, encoding="utf-8") as f:
                try:
                    value = json.load(f).get(key)
                except ValueError:
                    continue
            if value in seen:
                out.append("%s and %s both claim the %s %r"
                           % (seen[value], os.path.basename(folder), key, value))
            elif value is not None:
                seen[value] = os.path.basename(folder)
    return out


def _repo():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    bad = 0
    for folder in islands():
        problems = faults(folder)
        name = os.path.basename(folder)
        if problems:
            bad += 1
            print("%s" % name)
            for p in problems:
                print("    %s" % p)
        else:
            print("%s  ok" % name)
    for c in collisions():
        bad += 1
        print(c)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
