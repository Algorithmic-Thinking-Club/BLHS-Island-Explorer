"""Run your island with no game and no browser open.

An island is a set of generators that yield dicts. That means you can drive one
from a plain Python test: send it an answer, look at what it asks for next. This
file is the twenty lines that do that.

    from tests import pump

    pump.load("skeleton")
    seen = pump.run("talk:greeter", lambda intent: 0)
    assert seen[0]["kind"] == "say"

WHAT THIS PROVES AND WHAT IT DOES NOT. It proves your island's logic: that the
right branch runs, that the score comes out right, that the two arms ask the
same questions. It proves nothing about whether the engine will perform a word,
because in here nothing performs anything and the answers are whatever your test
hands back. A green test and a broken island are perfectly compatible. The game
is still the only place your island really runs.
"""
import inspect
import json
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ISLANDS = os.path.join(REPO, "islands")
if REPO not in sys.path:
    sys.path.insert(0, REPO)

import grape  # noqa: E402  (after the path fix above, on purpose)

# not a limit anyone reaches: an island beat is a handful of lines. It is here so
# that a loop which keeps yielding stops the test instead of the machine.
MAX_STEPS = 10_000

# what the last load() brought in, so this one can take it back out again
_loaded = ()


def load(island):
    """Import one island the way the engine will, and return its manifest.

    The island's own folder goes on sys.path, which is what lets island.py say
    `from questions import WhatAGrapeIs` about the file sitting next to it.

    AND EVERY OTHER ISLAND'S FOLDER COMES BACK OFF IT. This is not tidiness. The
    engine fetches one island's listed modules and nothing else, so an island
    that imports a file it does not ship fails there and only there. Leave the
    last island's folder on the path and this harness quietly supplies the
    missing file, the suite reports OK, and the member finds out in the game.
    Which is the worst place, and is the exact bug tools/manifest.py exists to
    catch one folder over.
    """
    global _loaded
    folder = os.path.join(ISLANDS, island)
    # utf-8-sig, not utf-8: every Windows editor will happily put a byte order
    # mark on the front of a JSON file and json.load chokes on it
    with open(os.path.join(folder, "island.json"), encoding="utf-8-sig") as f:
        manifest = json.load(f)

    sys.path[:] = [p for p in sys.path if not p.startswith(ISLANDS)]
    sys.path.insert(0, folder)

    # every module the last island shipped and every module this one ships,
    # dropped before the import. Without the second, editing a sibling file and
    # re-running quietly reuses the cached old one and you watch a bug you have
    # already fixed keep happening. Without the first, you import somebody else's.
    for name in set(_loaded) | {_module_name(n) for n in manifest["modules"]}:
        sys.modules.pop(name, None)
    _loaded = tuple(_module_name(n) for n in manifest["modules"])

    grape._forget()
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
    """
    fn = grape._handlers.get(handler)
    if fn is None:
        raise LookupError(
            "no handler called %r. This island registered: %s"
            % (handler, ", ".join(handlers()) or "nothing"))

    # CHECKED BEFORE IT IS CALLED. A handler with no `yield` anywhere in it is an
    # ordinary function, and calling it to find that out runs the whole body
    # first, which for a member means every side effect happens and then they are
    # told nothing ran.
    if not inspect.isgeneratorfunction(fn):
        raise TypeError(
            "%s() has no yield in it, so nothing would ever reach the engine. "
            "Put `yield` in front of the things that take time."
            % getattr(fn, "__name__", handler))

    body = fn()
    seen = []
    reply = None
    for _ in range(MAX_STEPS):
        try:
            intent = body.send(reply)
        except StopIteration:
            return seen
        seen.append(intent)
        reply = answer(intent) if answer else None

    raise RuntimeError("%s yielded %d times without finishing" % (handler, MAX_STEPS))


def kinds(seen):
    """Just the words, in order. Reads well in an assertion."""
    return [intent["kind"] for intent in seen]


def only(seen, kind):
    """Every intent of one kind, so a test can look at the questions alone."""
    return [intent for intent in seen if intent["kind"] == kind]


def _module_name(filename):
    return filename[:-3] if filename.endswith(".py") else filename
