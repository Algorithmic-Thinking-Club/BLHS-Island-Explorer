"""Check an island folder against the package format.

Check your own island:

    python tools/manifest.py islands/my-island

Check everything in the repo:

    python tools/manifest.py

Every complaint names the field it is about. The game runs these same rules on
what it fetches, so passing here means passing there.
"""
import json
import os
import re
import sys

# lower case, digits, single hyphens. The same shape the roster's ids are in,
# and safe as a folder name, a URL segment and a filename on every machine.
SLUG = re.compile(r"[a-z0-9]+(-[a-z0-9]+)*")

# what `import questions` can actually spell. A dot, a space or a capital in a
# filename passes every other check here and then cannot be imported at all.
STEM = re.compile(r"[a-z_][a-z0-9_]*")

# the format version every island.json declares.
FORMAT = 1

REQUIRED = ("format", "programme", "map", "title", "owner", "entry", "modules", "content")
OPTIONAL = ("season",)
SEASONS = ("Fall", "Winter", "Spring")

# what a student needs to walk in: what it is, when it meets, how to join.
FACTS = ("what", "when", "how_to_join")
CONTENT_OPTIONAL = ("blurb", "sticker", "meets")
# a blurb is a line in a list, not a paragraph
BLURB_WORDS = (4, 6)
# put this in a source field when you checked and nobody has published the fact.
UNKNOWN = "unknown"

# the string a person reads. One line, and short enough to sit in a dialogue box
# or a roster row without pushing anything off the edge.
TEXT_MAX = 80

# the most .py files one island can list; the game fetches them all at once.
MAX_MODULES = 24

# the engine provides these two, so an island must not ship its own copy.
ENGINE_OWNED = ("vine.py", "grape.py")

# islands the vine ships itself. read them, do not edit them, and do not add a
# row in islands.json for one.
VINE_OWNED = ("panther-maw", "castaway", "the-hub")

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
        # the checks below all read fields, so stop while the shape is wrong
        return out

    # in python True == 1, so a bool has to be refused before the number check
    if isinstance(m["format"], bool) or not isinstance(m["format"], int):
        out.append("`format` is %r, which is not a whole number" % (m["format"],))
    elif m["format"] != FORMAT:
        out.append("`format` is %r; this repo speaks format %d" % (m["format"], FORMAT))

    for key in ("programme", "map"):
        if not isinstance(m[key], str) or not SLUG.fullmatch(m[key]):
            out.append("`%s` is %r, which is not a slug" % (key, m[key]))
    # a programme is a thing you do and a map is a painting, so the two ids differ
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

    # a .py file nobody listed is never fetched, so the import fails in the game
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


def registry_faults(repo=None):
    """islands.json against the folders that actually exist.

    A row here is how an island reaches the roster, so a row naming a folder
    nobody wrote is an island the game cannot find.
    """
    root = repo or _repo()
    path = os.path.join(root, "islands.json")
    if not os.path.isfile(path):
        return ["there is no islands.json, so no island can reach the roster"]

    doc = _read(path)
    if isinstance(doc, str):
        return [doc.replace("island.json", "islands.json")]
    rows = doc.get("islands")
    if not isinstance(rows, list):
        return ["`islands` in islands.json has to be a list of rows"]

    out = []
    folders = {os.path.basename(f) for f in islands(root)}
    for i, row in enumerate(rows):
        where = (row or {}).get("programme") or "row %d" % (i + 1)
        if not isinstance(row, dict):
            out.append("%s is not an object" % where)
            continue
        for key in ("programme", "map", "folder", "name", "place", "blurb", "source"):
            if not isinstance(row.get(key), str) or not row[key].strip():
                out.append("%s: `%s` is missing" % (where, key))
        if row.get("kind") not in ("sport", "club"):
            out.append("%s: `kind` is sport or club" % where)
        if not isinstance(row.get("playable"), bool):
            out.append("%s: `playable` is true or false" % where)
        if not isinstance(row.get("tags"), list):
            out.append("%s: `tags` is a list, empty if none" % where)
        folder = row.get("folder")
        if isinstance(folder, str):
            if folder not in folders:
                out.append("%s: names the folder %r, which is not in islands/"
                           % (where, folder))
            else:
                # the row and the manifest are two statements about one island
                m = _read(os.path.join(root, "islands", folder, "island.json"))
                if isinstance(m, dict):
                    for key in ("programme", "map"):
                        if m.get(key) != row.get(key):
                            out.append("%s: `%s` is %r here and %r in %s/island.json"
                                       % (where, key, row.get(key), m.get(key), folder))

    return out


def unregistered(repo=None):
    """Folders with no row in islands.json yet. Not broken, just not shipped.

    An island with no row is one the game cannot see, which is the right state
    for yours until you are ready.
    """
    root = repo or _repo()
    doc = _read(os.path.join(root, "islands.json"))
    rows = doc.get("islands") if isinstance(doc, dict) else []
    claimed = {r.get("folder") for r in rows if isinstance(r, dict)}
    # the vine's own islands are bound inside the engine, so they need no row
    claimed |= set(VINE_OWNED)
    return [os.path.basename(f) for f in islands(root) if os.path.basename(f) not in claimed]


def islands(repo=None):
    """Every island folder in the repo, in order."""
    root = os.path.join(repo or _repo(), "islands")
    if not os.path.isdir(root):
        return []
    return [os.path.join(root, n) for n in sorted(os.listdir(root))
            if os.path.isdir(os.path.join(root, n))]


def collisions(repo=None):
    """Two islands claiming the same id.

    Programme ids and map ids are one key space, so one island's programme
    cannot be another island's map.
    """
    out = []
    seen = {}
    for folder in islands(repo):
        path = os.path.join(folder, "island.json")
        if not os.path.isfile(path):
            continue
        m = _read(path)
        # faults() has already refused this folder, and its fields cannot be read
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
        for c in registry_faults():
            bad += 1
            print(c)
        for name in unregistered():
            print("%s  no row in islands.json yet, so the game cannot see it" % name)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
