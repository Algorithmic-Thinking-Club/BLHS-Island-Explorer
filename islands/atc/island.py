"""The Algorithmic Thinking Club, and the island a member copies.

Nothing here calls the functions below. Each one is handed to the engine by its
decorator, and the engine runs it when the student does the matching thing.
Every `yield` takes time. Places are anchor names from the map, never
coordinates, and what anybody says lives in `lines.py`.
"""
from grape import manifest, on_start, on_talk
from vine import (
    actor_face, award, choose, framing, get, guide_to, highlight, island_tasks,
    lead_to, log, objective, play, say, set_flag, sound, task_done, view, wait,
)

from lines import (
    AGAIN, COME_BACK, DESK, FORM, HELLO, HOST, MEDALS, NO,
    SECOND_YEAR, SECOND_YEAR_DESK, SECOND_YEAR_HOW, THE_GAME, TROPHIES,
    WANT_A_GO, WELL_DONE, WHEN_AND_HOW, YES,
)

# the camera shot on the desk, set in MAPVIS
SCREEN = "the_screen"

# the checklist under the objective. A row is a thing the student does, and the
# `id` is what `task_done` is called with. `name` is what they read, `note` says
# where to go.
TASKS = [
    {"id": "meet", "name": "Meet the club president",
     "note": "He is at the top of the stair"},
    {"id": "program", "name": "Fix the half-finished program",
     "note": "On the computer that is switched on"},
]

# how long the camera holds on the machine before the screen opens
SETTLE_MS = 850

# what this island remembers. The engine puts the programme id in front of both,
# so these really are "atc:met" and "atc:built:y1" in the save and no other island
# can read them or collide with them.
MET = "met"


def built(year):
    """The flag name for finishing this island in a given year."""
    return "built:y%d" % year


@on_start
def arriving():
    """Runs every time the island loads, before the student can move.

    It runs again on every re-entry, so anything that speaks sits behind a flag.
    """
    yield log("island_opened", {"island": manifest()["programme"]})

    # `island_tasks` replaces the list rather than adding to it, and which rows are
    # already ticked comes back out of the save
    yield island_tasks(TASKS)

    # the arrow follows what is still owed this year, not whether he has been here before
    year = yield get("year")
    flags = yield get("flags")
    if built(year) in flags:
        return

    # point him at the president, and say nothing until he gets there
    yield objective("Find the club president.")
    yield guide_to(HOST)


@on_talk(HOST)
def the_president():
    """The club president, and the only person on this island.

    `lead_to` walks him over with the student following, and comes back when they
    have both stopped. What he says depends on the year: nothing owed and he just
    says hello, a first visit gets his name, a returning student gets the short
    version and the same walk.
    """
    year = yield get("year")
    flags = yield get("flags")

    if built(year) in flags:
        yield say(AGAIN, who=HOST)
        # meeting him counts even when the program was finished first
        yield task_done("meet")
        return

    # turn the two of them to face each other. A facing is a nicety, so a refusal
    # is logged and the island carries on.
    try:
        yield actor_face(HOST, "thor")
        yield actor_face("thor", HOST)
    except Exception as refused:
        yield log("actor_face_refused", {"why": str(refused)})

    # `get("rank")` answers about your own island: how many earlier years the
    # student finished it, which years, their best grade, and the rung they reached.
    been = yield get("rank")
    returning = bool(been and been.get("taken"))

    known = MET in flags
    if returning:
        yield say(SECOND_YEAR, who=HOST)
    elif known:
        yield say(AGAIN, who=HOST)
    else:
        yield say(HELLO, who=HOST)
        yield set_flag(MET)

    # the joining facts come before the activity, because the scored question asks
    # about them. A returning student gets their own line instead.
    yield say(SECOND_YEAR_HOW if returning else WHEN_AND_HOW, who=HOST)

    # tick the row after he has spoken, not on the way in
    yield task_done("meet")

    yield objective("Follow him to the machine.")
    yield lead_to(HOST, DESK)
    # turn them to face each other again, so the next line is said to a face
    try:
        yield actor_face(HOST, "thor")
        yield actor_face("thor", HOST)
    except Exception as refused:
        yield log("actor_face_refused", {"why": str(refused)})
    if not known:
        yield say(THE_GAME, who=HOST)
    yield from the_offer()


@on_talk(TROPHIES)
def the_medals():
    """The plinth by the stair head. The numbers behind it live in `island.json`."""
    yield say(MEDALS, who=TROPHIES)


@on_talk(DESK)
def the_machine():
    """The machine that is switched on, which is the one you can press."""
    year = yield get("year")
    flags = yield get("flags")
    if built(year) in flags:
        yield say(FORM, who=HOST)
        return
    yield from the_offer()


def the_offer():
    """Ask whether they want a go, then run it. Both roads to the desk end here."""
    # take the arrow down, then light the one machine that is on. `guide_to` draws
    # a road to a place; `highlight` only says which thing.
    yield guide_to(None)
    try:
        yield highlight(DESK)
    except Exception as refused:
        yield log("highlight_refused", {"why": str(refused)})

    been = yield get("rank")
    if been and been.get("taken"):
        yield say(SECOND_YEAR_DESK, who=HOST)

    pick = yield choose([YES, NO], prompt=WANT_A_GO)
    # -1 is not an index. It is nobody having answered, because the student left
    # while the buttons were up, and it must never read as the first button.
    if pick != 0:
        # the light goes out with the offer
        yield highlight(None)
        yield say(COME_BACK, who=HOST)
        # clear the objective when he declines
        yield objective(None)
        return

    yield from sit_down()


def sit_down():
    """The camera goes into the monitor, the screen opens, and it is scored."""
    yield highlight(None)
    yield objective("Fix the program.")
    # the click is the machine waking. A sound that refuses is logged and the
    # island carries on.
    try:
        yield sound("click")
    except Exception as refused:
        yield log("sound_refused", {"why": str(refused)})
    yield framing(SCREEN)
    yield wait(SETTLE_MS)

    # `play` refuses an item it cannot draw, so the `finally` puts the camera and
    # the objective back whether it returned or raised.
    score = None
    try:
        score = yield play(
            "the_program",
            title="The half-finished program",
            items=[THE_PROGRAM, HOW_YOU_JOIN],
        )
    finally:
        yield framing(None)
        yield objective(None)
        # let the camera ease back before anybody speaks
        yield view("close", 900)

    # a score of None is the student closing the screen without finishing. Zero is
    # somebody who answered and got it wrong.
    if score is None:
        yield say(COME_BACK, who=HOST)
        return

    yield task_done("program")
    yield say(WELL_DONE, who=HOST)

    # read `programme` off the manifest rather than typing the id a second time
    yield award(
        programme=manifest()["programme"],
        grade=score,
        sticker="first-program",
    )
    year = yield get("year")
    yield set_flag(built(year))
    yield log("program_built", {"grade": score, "year": year})

    # pull the camera out to the whole island for the last line
    try:
        yield view("island", 3200)
    except Exception as refused:
        yield log("view_refused", {"why": str(refused)})
    yield say(FORM, who=HOST)


# two scored items: the maze the club would build, and one question about the club

# `grid` is the board drawn as text, so the puzzle reads the same without pictures
BOARD = "\n".join([
    "   col  0   1   2   3   4   5",
    " row 0  .   .   .   .   .   F",
    " row 1  .   .   .   .   .   .",
    " row 2  .   .   .   #   .   .",
    " row 3  P>  .   .   #   .   .",
])

THE_PROGRAM = {
    "kind": "program",
    "id": "atc-maze",
    "prompt": "Put the program back in order, then press RUN.",
    "grid": BOARD,
    # the instructions are a vocabulary, not a bag: every one of them is offered at
    # every step, which is what makes the form and the screen offer the same answers
    "moves": [
        {"name": "fwd2", "label": "forward 2"},
        {"name": "fwd3", "label": "forward 3"},
        {"name": "left", "label": "turn left"},
        {"name": "right", "label": "turn right"},
    ],
    # scoring keys on the step, so two steps can want the same instruction
    "slots": [
        {"label": "Step 1", "move": "fwd2"},
        {"label": "Step 2", "move": "left"},
        {"label": "Step 3", "move": "fwd3"},
        {"label": "Step 4", "move": "right"},
        {"label": "Step 5", "move": "fwd3"},
    ],
    # the board the body walks. Nothing scores off it.
    "board": {
        "cols": 6,
        "rows": 4,
        "walls": [[3, 2], [3, 3]],
        "flag": [5, 0],
        "start": {"col": 0, "row": 3, "facing": "east"},
    },
    "reply": "The wall is the whole puzzle. The turn has to come before it.",
}

# a `choice` carries a reply on every option, so a wrong pick is told why
HOW_YOU_JOIN = {
    "kind": "choice",
    "id": "atc-join",
    "prompt": "How do you join ATC?",
    "options": [
        {
            "text": "Show up after school and fill out a form",
            "correct": True,
            "reply": "That is it. Room 303, any day after school.",
        },
        {
            "text": "Try out and get picked",
            "reply": "No tryout. Nobody is picked and nobody is cut.",
        },
        {
            "text": "Ask a counselor to sign you up",
            "reply": "You do not need one. You walk in and fill out the form.",
        },
    ],
}
