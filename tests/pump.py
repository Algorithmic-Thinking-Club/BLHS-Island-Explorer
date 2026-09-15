"""Run your island with no game and no browser open.

An island is a set of generators that yield dicts, so a plain Python test can
drive one: send it an answer, look at what it asks for next.

    from tests import pump

    pump.load("skeleton")
    seen = pump.run("talk:greeter", lambda intent: 0)
    assert seen[0]["kind"] == "say"

This checks your island's logic only. Nothing here performs a word, so a green
test still leaves the game as the only place your island really runs.
"""
import inspect
import json
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ISLANDS = os.path.join(REPO, "islands")
if REPO not in sys.path:
    sys.path.insert(0, REPO)

import grape  # noqa: E402  (after the path fix above, on purpose)

# stops a handler that keeps yielding instead of hanging the test
MAX_STEPS = 10_000


class Refused(Exception):
    """Raise this from your `answer` to make the engine refuse that word.

    The refusal lands at the line that yielded, so a handler that does not catch
    it stops there, exactly as it would in the game.
    """

# what the last load() brought in, so this one can take it back out again
_loaded = ()


def load(island):
    """Import one island the way the engine will, and return its manifest.

    Only that island's folder is on sys.path, so a file it does not list in
    island.json fails here the same way it fails in the game.
    """
    global _loaded
    folder = os.path.join(ISLANDS, island)
    # utf-8-sig, so a byte order mark from a Windows editor does not break json.load
    with open(os.path.join(folder, "island.json"), encoding="utf-8-sig") as f:
        manifest = json.load(f)

    sys.path[:] = [p for p in sys.path if not p.startswith(ISLANDS)]
    sys.path.insert(0, folder)

    # drop the cached modules of both islands, so an edited file is re-imported
    for name in set(_loaded) | {_module_name(n) for n in manifest["modules"]}:
        sys.modules.pop(name, None)
    _loaded = tuple(_module_name(n) for n in manifest["modules"])

    grape._forget()
    # describe before the import, so a module-level manifest() call works
    grape._describe(manifest)
    __import__(_module_name(manifest["entry"]))
    return manifest


def handlers():
    """Every handler key the loaded island registered."""
    return grape._registered()


def run(handler, answer=None):
    """Drive one handler to the end. Returns every intent it yielded, in order.

    `answer` is called with each intent and returns what the engine would have
    sent back: the index for a choose, the value for a get, None for the rest.
    Leave it out and everything is answered with None.

    Raise `pump.Refused("why")` out of `answer` and it is thrown back into your
    island at the yield that asked for it, the same as a refusal in the game.
    """
    fn = grape._handlers.get(handler)
    if fn is None:
        raise LookupError(
            "no handler called %r. This island registered: %s"
            % (handler, ", ".join(handlers()) or "nothing"))

    # judged on what calling it returns, so a decorated handler still counts
    body = fn()
    if not inspect.isgenerator(body):
        raise TypeError(
            "%s() has no yield in it, so nothing would ever reach the engine. "
            "Put `yield` in front of the things that take time."
            % getattr(fn, "__name__", handler))

    seen = []
    reply = None
    raise_in = None
    for _ in range(MAX_STEPS):
        try:
            intent = body.throw(raise_in) if raise_in else body.send(reply)
        except StopIteration:
            return seen
        raise_in = None
        seen.append(intent)
        if not answer:
            continue
        try:
            reply = answer(intent)
        except Refused as no:
            # the engine raises a RuntimeError at the line that yielded
            reply = None
            raise_in = RuntimeError(str(no))

    raise RuntimeError("%s yielded %d times without finishing" % (handler, MAX_STEPS))


def kinds(seen):
    """Just the words, in order. Reads well in an assertion."""
    return [intent["kind"] for intent in seen]


def only(seen, kind):
    """Every intent of one kind, so a test can look at the questions alone."""
    return [intent for intent in seen if intent["kind"] == kind]


def _module_name(filename):
    return filename[:-3] if filename.endswith(".py") else filename

# the run paths the engine answers, with the values a save nobody has played yet
# gives. Override any of them by keyword in answering(); an unknown path raises
# KeyError.
FRESH_RUN = {
    "year": 1,
    "gpa": 0,
    "tokens": 0,
    "cords": [],
    "cord_board": [],
    "trophies": {"stickers": [], "badges": []},
    "advisory": None,
    "flags": [],
    "planned": False,
    "islands": {},
    "handle": None,
    "graduated": False,
    "mode": "game",
    "phase": None,
    "picks": {"classes": [], "seasons": [], "graded": [], "gpa": None},
    # how many times this island has been taken. a fresh run has never taken it
    "rank": {"taken": 0, "years": [], "best": None, "rung": 0},
}


def answering(refuse=(), choices=(), score=3.4, **state):
    """An engine that answers every question about the run, and refuses on cue.

    `refuse` is the intent kinds this map cannot do, which come back to the island
    as the engine's own refusal at the line that yielded. `choices` is what the
    player presses, in order, and anything past the end of it is the first button.
    `score` is what a scored beat comes back as. Everything else is a run value:
    `answering(year=2, flags=["maw:railed"])`.

    A `set_flag` really lands, so an island can read back a flag it just wrote.
    """
    unknown = [k for k in state if k not in FRESH_RUN]
    if unknown:
        raise KeyError("no such run path: %s" % ", ".join(sorted(unknown)))
    run = dict(FRESH_RUN)
    run.update(state)
    run["flags"] = list(run["flags"])
    queue = list(choices)

    def answer(intent):
        kind = intent["kind"]
        if kind in refuse:
            raise Refused("%s: this map cannot do that" % kind)
        if kind == "get":
            return run[intent["path"]]
        if kind == "set_flag":
            name = intent.get("flag")
            if name and name not in run["flags"]:
                run["flags"].append(name)
            return None
        if kind == "choose":
            return queue.pop(0) if queue else 0
        if kind == "play":
            return score
        return None

    return answer


def askable():
    """Every path `get` documents, read out of vine.py's own docstring.

    It reads that docstring's two-column table: a path, some spaces, then its
    description.
    """
    with open(os.path.join(REPO, "vine.py"), encoding="utf-8") as f:
        src = f.read()
    body = re.search(r'def get\(path\):\n    """(.*?)"""', src, re.S)
    if not body:
        raise AssertionError("vine.py's get() has no docstring to read the paths out of")
    out = set()
    for line in body.group(1).split("\n"):
        # two spaces is enough: `cord_board` has the longest name and only two
        m = re.match(r"    ([a-z_]{2,20})  +\S", line)
        if m:
            out.add(m.group(1))
    if len(out) < 12:
        raise AssertionError("only found %d paths in the docstring: %s" % (len(out), sorted(out)))
    return out
