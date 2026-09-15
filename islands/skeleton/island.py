"""The island you copy. Take this folder, rename it, and start deleting.

An island is a folder: island.json says who you are, this file says what happens
and when, lines.py holds what it says and asks.

Three things to notice on the way through:

  - nothing here calls the two functions below. A decorator hands each one to the
    game, and the game calls it when the player does something.
  - every `yield` is a thing that takes time. A line without one is ordinary
    Python, running instantly.
  - places are anchor names somebody typed in MAPVIS, never an x and a y.

Nothing in here is a claim about Bonney Lake High School. Yours keeps that
promise a different way: every fact about the school needs a source in your
island.json.
"""
from grape import manifest, on_start, on_talk
from vine import (
    award, choose, get, guide_to, island_tasks, log, objective, play, say,
    set_flag, task_done,
)

from lines import (
    AGAIN, GREETER, HELLO, NO, NOT_NOW, WANT_A_GO, WELL_DONE, WHAT_WE_DO,
    WHERE_WE_MEET, YES,
)

# one row per thing a student DOES, and being talked to is not one. `id` is what
# `task_done` ticks, `name` is what a fourteen year old reads, `note` says where.
TASKS = [
    {"id": "meet", "name": "Find the greeter", "note": "At the top of the path"},
    {"id": "answer", "name": "Answer her question", "note": "She asks it herself"},
]


def finished(year):
    """The flag this island sets when it is done, carrying the year.

    A flag stays in the save for the rest of the run, and a student can come back
    in a later year, so the year has to be part of the name.
    """
    return "finished:y%d" % year


@on_start
def arriving():
    """Runs every time the island loads, before the player can move."""
    yield log("island_opened", {"island": manifest()["programme"]})
    # this replaces the list rather than adding to it, and the ticks come back
    # out of the save, so declaring it on every load is right
    yield island_tasks(TASKS)

    year = yield get("year")
    if finished(year) in (yield get("flags")):
        return
    yield objective("Find the greeter.")
    yield guide_to(GREETER)


@on_talk(GREETER)
def the_greeter():
    """Runs when the player presses E on the anchor named `greeter`."""
    year = yield get("year")
    if finished(year) in (yield get("flags")):
        yield say(AGAIN, who=GREETER)
        yield task_done("meet")     # reachable down every road, or the list lies
        return

    yield say(HELLO, who=GREETER)
    # said before the activity, or the island grades a fact it never gave
    yield say(WHAT_WE_DO, who=GREETER)
    yield task_done("meet")
    # the arrow comes down, or it points at somebody two feet in front of him
    yield guide_to(None)

    # -1 is nobody answering, because the player left while the buttons were up
    if (yield choose([YES, NO], prompt=WANT_A_GO)) != 0:
        yield say(NOT_NOW, who=GREETER)
        yield objective(None)
        return

    # the line at the top comes back even when `play` refuses, which a typo does
    try:
        yield objective("Answer her question.")
        score = yield play("the_question", title="One question", items=[WHERE_WE_MEET])
    finally:
        yield objective(None)

    # None is the player closing the activity without finishing, which is not a zero
    if score is None:
        yield say(NOT_NOW, who=GREETER)
        return

    yield task_done("answer")
    yield say(WELL_DONE, who=GREETER)
    # read out of your own island.json, so the programme id is written once
    yield award(programme=manifest()["programme"], grade=score)
    yield set_flag(finished(year))
