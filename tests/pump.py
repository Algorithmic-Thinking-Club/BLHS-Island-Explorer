"""Run your island with no game and no browser open.

An island is a set of generators that yield dicts. That means you can drive one
from a plain Python test: send it an answer, look at what it asks for next. This
file is the twenty lines that do that, and it is the same shape as the engine's
own driver, deliberately.

    from tests import pump

    pump.load("skeleton")
    seen = pump.run("talk:greeter", lambda intent: 0)
    assert seen[0]["kind"] == "say"

WHAT THIS PROVES AND WHAT IT DOES NOT. It proves your island's logic: that the
right branch runs, that the score comes out right, that the two arms ask the
same questions. It proves nothing at all about whether the engine will perform a
word, because in here nothing performs anything: the answers are whatever your
test hands back. A green test and a broken island are perfectly compatible. The
game is still the only place your island really runs.
"""
import json
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO not in sys.path:
    sys.path.insert(0, REPO)

import grape  # noqa: E402  (after the path fix above, on purpose)

# not a limit anyone reaches: an island beat is a handful of lines. It is here so
# that a loop which keeps yielding stops the test instead of the machine.
MAX_STEPS = 10_000


def load(island):
    """Import one island the way the engine does, and return its manifest.

    The island's own folder goes on sys.path, which is what lets island.py say
    `from questions import WhatAGrapeIs` about the file sitting next to it.
    """
    folder = os.path.join(REPO, "islands", island)
    with open(os.path.join(folder, "island.json"), encoding="utf-8") as f:
        manifest = json.load(f)

    while folder in sys.path:
        sys.path.remove(folder)
    sys.path.insert(0, folder)

    # every module the island ships, dropped before the import. Without this,
    # editing a sibling file and re-running quietly reuses the cached old one and
    # you watch a bug you already fixed keep happening.
    for name in manifest["modules"]:
        sys.modules.pop(_module_name(name), None)

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

    body = fn()
    if type(body).__name__ != "generator":
        raise TypeError(
            "%s() never yielded, so nothing ran. Put `yield` in front of the "
            "things that take time." % getattr(fn, "__name__", handler))

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
