"""THE PACKAGE FORMAT, written down as the thing that refuses.

An island is a folder with an island.json in it. This file is what "a folder
with an island.json in it" actually means, and it is here rather than in a
document because a document does not stop anybody.

Check your own island:

    python tools/manifest.py islands/my-island

Check everything in the repo:

    python tools/manifest.py

Every complaint names the field. A checker that says "invalid manifest" has told
you nothing; one that says `modules` lists questions.py, which is not in this
folder has told you what to do next.

The game runs these same rules on what it fetched, in
AdventureGame/src/vine/py/grape-source.ts, so failing here means failing there.
Two of them are only checkable on this side, because over HTTP there is no folder
to look in: a .py file on disk that nobody listed, and a name in `modules` whose
capitals do not match the file. Both are the kind that only break in the game.
"""
import json
import os
import re
import sys

# lower case, digits, single hyphens. The same shape the roster's ids are in,
# and safe as a folder name, a URL segment and a filename on every machine.
#
# MATCHED WITH fullmatch AND NEVER match. Python's `$` also matches just before a
# trailing newline, so `"robotics\n"` passed this and was then refused by the
# game, whose JavaScript `$` does not. That is the worst direction for a rule to
# be wrong in: the local checker says yes and the thing that matters says no.
SLUG = re.compile(r"[a-z0-9]+(-[a-z0-9]+)*")

# what `import questions` can actually spell. A dot, a space or a capital in a
# filename passes every other check here and then cannot be imported at all.
STEM = re.compile(r"[a-z_][a-z0-9_]*")

# THE FORMAT VERSION. It is not decoration. Two repositories ship on different
# days, and the day the format changes this number is how a member finds out
# their island needs an edit instead of watching it fail strangely.
FORMAT = 1

REQUIRED = ("format", "programme", "map", "title", "owner", "entry", "modules", "content")
OPTIONAL = ("season",)
SEASONS = ("Fall", "Winter", "Spring")

# P18. What a student needs to know to walk into this thing on a Tuesday, which
# is not the same as what makes a good island and is the half a builder skips.
FACTS = ("what", "when", "how_to_join")
CONTENT_OPTIONAL = ("blurb", "sticker", "meets")
# a blurb is a line in a list, not a paragraph
BLURB_WORDS = (4, 6)
# the explicit marker. An absent source is a member who did not think about it;
# this is a member who did, and the game can render the difference.
UNKNOWN = "unknown"

# the string a person reads. One line, and short enough to sit in a dialogue box
# or a roster row without pushing anything off the edge.
TEXT_MAX = 80

# an island is a handful of small text files, and the game fetches all of them at
# once. The same number is in grape-source.ts.
MAX_MODULES = 24

# the engine writes its own copy of both of these into the runtime before your
# island is imported. A member shipping one would shadow the real thing with a
# stale copy and spend an afternoon on it.
ENGINE_OWNED = ("vine.py", "grape.py")

# names Python already uses. An island shipping random.py does not get a warning,
# it replaces the real one for everything running in that runtime.
TAKEN = (
    "abc", "array", "asyncio", "binascii", "builtins", "collections", "copy",
    "enum", "errno", "functools", "gc", "grape", "hashlib", "heapq", "inspect",
    "io", "itertools", "json", "math", "os", "random", "re", "select", "socket",
    "ssl", "string", "struct", "sys", "test", "time", "types", "uasyncio", "vine",
)


def faults(folder):
    """Every reason this folder is not a loadable island. Empty means it is one."""
    out = []
    name = os.path.basename(os.path.normpath(folder))
    if not SLUG.fullmatch(name):
        out.append("the folder name %r is not a slug: lower case, digits and single hyphens" % name)

    path = os.path.join(folder, "island.json")
    if not os.path.isfile(path):
        return out + ["there is no island.json here, so nothing knows this is an island"]

    m = _read(path)
    if isinstance(m, str):
        return out + [m]

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

    # `is not int` and not `!= FORMAT`, because in Python True == 1, so a
    # `"format": true` typo would sail through the one check that exists to stop
    # a mis-versioned island, and then fail on the engine's `format === 1`
    if isinstance(m["format"], bool) or not isinstance(m["format"], int):
        out.append("`format` is %r, which is not a whole number" % (m["format"],))
    elif m["format"] != FORMAT:
        out.append("`format` is %r; this repo speaks format %d" % (m["format"], FORMAT))

    for key in ("programme", "map"):
        if not isinstance(m[key], str) or not SLUG.fullmatch(m[key]):
            out.append("`%s` is %r, which is not a slug" % (key, m[key]))
    # THE KEY SPACES STAY DISJOINT. A programme is a thing you do; a map is a
    # painting. The roster refuses an id that is both, so an island that ships
    # one is an island that can never be added to the roster.
    if m["programme"] == m["map"]:
        out.append("`programme` and `map` are both %r; they are different key spaces "
                   "and the roster refuses an id that is in both" % m["map"])

    out.extend(_text_faults(m))

    if "season" in m and m["season"] not in SEASONS:
        out.append("`season` is %r; it has to be one of %s, or left out when your "
                   "island is not seasonal" % (m["season"], ", ".join(SEASONS)))

    out.extend(_module_faults(folder, m))
    out.extend(_content_faults(m["content"]))
    return out


def _content_faults(c):
    """The section that is about a real school, and where each fact came from."""
    if not isinstance(c, dict):
        return ["`content` has to be an object: what, when, how_to_join and a blurb"]
    out = []

    for key in c:
        if key not in FACTS and key not in CONTENT_OPTIONAL:
            out.append("`content.%s` is not a field this format has" % key)

    for key in FACTS:
        f = c.get(key)
        if not isinstance(f, dict):
            out.append("`content.%s` is missing. It is {\"text\": \"...\", \"source\": \"...\"}" % key)
            continue
        if not isinstance(f.get("text"), str) or not f["text"].strip():
            out.append("`content.%s.text` is empty" % key)
        # THE WHOLE POINT OF THE SECTION. A sentence about BLHS with nothing
        # behind it is a sentence the game tells a student as though it were true.
        if not isinstance(f.get("source"), str) or not f["source"].strip():
            out.append("`content.%s.source` is missing. Cite where the fact came from, "
                       "or put \"%s\", which means you checked and nobody has "
                       "published it" % (key, UNKNOWN))

    blurb = c.get("blurb")
    if not isinstance(blurb, str) or not blurb.strip():
        out.append("`content.blurb` is missing. Four to six words, for a list.")
    else:
        words = len(blurb.split())
        if words < BLURB_WORDS[0] or words > BLURB_WORDS[1]:
            out.append("`content.blurb` is %d words; it goes in a list, so %d to %d"
                       % (words, BLURB_WORDS[0], BLURB_WORDS[1]))

    if "sticker" in c and (not isinstance(c["sticker"], str) or not SLUG.fullmatch(c["sticker"])):
        out.append("`content.sticker` is %r, which is not a slug" % (c.get("sticker"),))

    if "meets" in c:
        if not isinstance(c["meets"], list):
            out.append("`content.meets` is a list of {day, time, room, source}")
        else:
            for i, meet in enumerate(c["meets"]):
                for k in ("day", "time", "room", "source"):
                    v = meet.get(k) if isinstance(meet, dict) else None
                    if not isinstance(v, str) or not v.strip():
                        out.append("`content.meets[%d].%s` is missing. A meeting time "
                                   "nobody sourced is a student standing outside the "
                                   "wrong room." % (i, k))
    return out


def _text_faults(m):
    out = []
    for key in ("title", "owner"):
        value = m[key]
        if not isinstance(value, str) or not value.strip():
            out.append("`%s` is empty, and somebody has to be able to read it" % key)
        elif "\n" in value or "\r" in value or "\x00" in value:
            # `title` lands in a dialogue box and on a roster row with nothing
            # between the manifest and the render
            out.append("`%s` has a line break or a control character in it, and it is "
                       "rendered as one line" % key)
        elif len(value) > TEXT_MAX:
            out.append("`%s` is %d characters; keep it to %d so it fits where it "
                       "is drawn" % (key, len(value), TEXT_MAX))
    return out


def _module_faults(folder, m):
    out = []
    mods = m["modules"]
    if not isinstance(mods, list) or not mods:
        return ["`modules` has to list every .py file the engine should fetch"]
    if len(mods) > MAX_MODULES:
        return ["`modules` lists %d files. An island is a handful, and every one of "
                "them is fetched at once, so the limit is %d." % (len(mods), MAX_MODULES)]

    on_disk = os.listdir(folder)
    lowered = {f.lower(): f for f in on_disk}

    for name in mods:
        if not isinstance(name, str) or not name.endswith(".py"):
            out.append("`modules` has %r in it, which is not a .py filename. The "
                       "extension is lower case, because that is what you type after "
                       "`import`" % (name,))
            continue
        if "/" in name or "\\" in name:
            out.append("`modules` has %r in it; a module is a filename, and an island "
                       "is one flat folder" % name)
            continue
        if name.lower() in ENGINE_OWNED:
            out.append("`modules` lists %s, which the game provides. Yours would be "
                       "ignored at best and shadow the real one at worst" % name)
            continue

        stem = name[:-3]
        if not STEM.fullmatch(stem):
            out.append("`modules` has %s in it. A module name is lower case letters, "
                       "digits and underscores, because the file name is what you type "
                       "after `import`" % name)
            continue
        if stem in TAKEN:
            out.append("`modules` lists %s, which is a name Python already uses. Yours "
                       "would replace the real one for everything running beside it" % name)
        if name not in on_disk:
            real = lowered.get(name.lower())
            if real:
                # works on Windows, 404s on raw.githubusercontent.com, which is
                # where the engine fetches it from
                out.append("`modules` says %s and the file is %s. The game fetches over "
                           "HTTP and that is case-sensitive" % (name, real))
            else:
                out.append("`modules` lists %s, which is not in this folder" % name)

    names = [n for n in mods if isinstance(n, str)]
    if len({n.lower() for n in names}) != len(names):
        out.append("`modules` lists the same file twice")

    entry = m["entry"]
    if not isinstance(entry, str) or entry not in mods:
        out.append("`entry` is %r, which is not one of the modules" % (entry,))

    # A FILE NOBODY LISTED IS A FILE THAT IS NEVER FETCHED. The island imports
    # it, the import fails inside the game and nowhere else, and the traceback
    # points at a line that is correct. Cheapest possible thing to catch here.
    for f in sorted(on_disk):
        full = os.path.join(folder, f)
        if os.path.isdir(full):
            if f != "__pycache__":
                out.append("%s/ is a folder. An island is one flat folder, and the game "
                           "only ever fetches the files named in `modules`" % f)
        elif f.lower().endswith(".py") and f not in mods:
            out.append("%s is in this folder but not in `modules`, so the game never "
                       "fetches it and the import fails only inside the game" % f)
    return out


def _read(path):
    """The manifest, or one sentence saying why there isn't one."""
    try:
        # utf-8-sig reads a file with or without the byte order mark that every
        # Windows editor is happy to add and that json.load will not accept
        with open(path, encoding="utf-8-sig") as f:
            m = json.load(f)
    except ValueError as e:
        return "island.json is not valid JSON: %s" % e
    if not isinstance(m, dict):
        return "island.json has to be an object, not a %s" % type(m).__name__
    return m


def islands(repo=None):
    """Every island folder in the repo, in order."""
    root = os.path.join(repo or _repo(), "islands")
    if not os.path.isdir(root):
        return []
    return [os.path.join(root, n) for n in sorted(os.listdir(root))
            if os.path.isdir(os.path.join(root, n))]


def collisions(repo=None):
    """Two islands claiming the same id.

    ONE key space, not one per field. The roster refuses an id that is both a
    programme and a map, so two islands where one's programme is the other's map
    are as broken as two islands with the same programme.
    """
    out = []
    seen = {}
    for folder in islands(repo):
        path = os.path.join(folder, "island.json")
        if not os.path.isfile(path):
            continue
        m = _read(path)
        # a manifest faults() has already refused; complaining twice about the
        # same folder helps nobody, and reading its fields would raise
        if isinstance(m, str):
            continue
        name = os.path.basename(folder)
        for key in ("programme", "map"):
            value = m.get(key)
            if not isinstance(value, str):
                continue
            if value in seen:
                who, what = seen[value]
                if who != name or what != key:
                    out.append("%s claims the %s %r and %s claims the %s %r; they are "
                               "one key space" % (name, key, value, who, what, value))
            else:
                seen[value] = (name, key)
    return out


def _repo():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main(argv=()):
    folders = [os.path.abspath(a) for a in argv] or islands()
    if not folders:
        print("no islands yet")
        return 0

    bad = 0
    for folder in folders:
        problems = faults(folder)
        name = os.path.basename(os.path.normpath(folder))
        if problems:
            bad += 1
            print("%s" % name)
            for p in problems:
                print("    %s" % p)
        else:
            print("%s  ok" % name)

    # only when sweeping the whole repo: one member should not be told about
    # another member's id clash while they are checking their own folder
    if not argv:
        for c in collisions():
            bad += 1
            print(c)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
