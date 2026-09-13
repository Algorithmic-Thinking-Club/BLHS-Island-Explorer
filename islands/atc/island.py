"""THE ALGORITHMIC THINKING CLUB, and the island a member copies.

READ THIS ONE FIRST. The Panther's Maw is the complicated example: it reaches
things only the vine's own content is allowed to reach, and you read it to find
out what is underneath. This is the other kind. It is one club, one conversation
and one scored thing, and almost all of it is four words long.

WHAT TO NOTICE ON THE WAY THROUGH:

  - nothing in this file calls the four functions below. Each one is handed to the
    engine by its decorator, and the engine decides when it runs. A student walks
    up to a post, presses E, and the engine looks up whoever claimed that name.
    That inversion is the whole difference between an island and a script.
  - every `yield` is a thing that takes time. Every line without one is ordinary
    Python running instantly, exactly as it looks.
  - the places are NAMES, never coordinates. `host` and `the_desk` are anchors
    somebody dragged onto the painting in MAPVIS. Move the desk and this file does
    not change.
  - what anybody says lives in `lines.py`. What happens and when lives here.

WHAT THIS ISLAND IS ABOUT, so the activity is not a quiz with a costume on: ATC
is where students build the game you are standing in. So the scored thing is
building something and watching it run, and the one question after it is about
the club rather than about programming, because an island that measures only
whether a freshman can solve a maze has not measured whether they learned
anything about ATC.
"""
from grape import manifest, on_start, on_talk
from vine import (
    award, choose, framing, get, guide_to, lead_to, log, objective, play, say,
    set_flag, wait,
)

from lines import (
    AGAIN, COME_BACK, DESK, FORM, HELLO, HOST, MEDALS, NO, THE_GAME, TROPHIES,
    WANT_A_GO, WELL_DONE, WHEN_AND_HOW, YES,
)

# the shot somebody dragged onto the desk in MAPVIS. Naming it here rather than
# in the line that uses it means renaming the shot is a one-word edit.
SCREEN = "the_screen"

# A BREATH AFTER THE CAMERA LANDS, and that is all it is now.
#
# `framing` used to answer the instant it was asked, so this number was the whole
# of the push-in and it was a guess: the camera takes as long as it takes and the
# screen opened somewhere in the middle of the move. The engine's `framing` waits
# for its own camera now, so what is left here is a held moment on the machine
# before the screen takes over, which is a beat rather than a fudge.
SETTLE_MS = 260

# what this island remembers. The engine puts the programme id in front of both,
# so these really are "atc:met" and "atc:built:y1" in the save and no other island
# can read them or collide with them.
MET = "met"


def built(year):
    """Done THIS YEAR, and the year is the whole point.

    A flag lives in the save for the rest of the run and `end_year` does not clear
    it, so a plain "built" would be set for ever the first time somebody finished
    this island. A club takes any season and the rank ladder is three years on one
    track, so a student coming back in year two is the DESIGN and not an edge case:
    with a run-wide flag they would sail here, press the machine, be told where the
    form is, and never be able to finish the pick. The year would hang open with
    nothing on screen saying why.

    The Maw spells its yearbook flag the same way for the same reason.
    """
    return "built:y%d" % year


@on_start
def arriving():
    """Every time the island loads, before the student can move.

    EVERY TIME, which is the thing to design around: walk out and back in and this
    runs again. So anything that speaks sits behind a flag, and what is left is
    the one sentence at the top of the screen saying what there is to do here.
    """
    yield log("island_opened", {"island": manifest()["programme"]})

    # THE ARROW FOLLOWS WHAT IS OWED, not whether he has been here before. A
    # student in their second year has met the president and still has a pick to
    # finish, so gating this on "have we met" left a returning student standing on
    # the jetty with nothing pointing anywhere.
    year = yield get("year")
    flags = yield get("flags")
    if built(year) in flags:
        return

    # THE ARROW AND THE SENTENCE, AND NOTHING ELSE. He has just climbed a long
    # stair and the club president is standing at the top of it. Anything said
    # before he gets there would be said to somebody still walking.
    yield objective("Find the club president.")
    yield guide_to(HOST)


@on_talk(HOST)
def the_president():
    """The club president, who is the only person on this island.

    HE WALKS YOU OVER. `lead_to` sets him off, brings the student along behind him
    and comes back when they have both stopped, with him turned round. Written as
    `actor_move` and then `walk_to` it does not work: `actor_move` waits for him to
    ARRIVE, so the student stands still watching a man cross a terrace and then
    walks the same floor on his own afterwards.

    THREE THINGS HE CAN BE, and the year decides which. Nothing owed this year and
    he just says hello. A student who has never been here gets his name. A student
    who was here last year gets the short version and then the same walk, because
    the year's pick is owed again and the club has to be finished again to close it.
    """
    year = yield get("year")
    flags = yield get("flags")

    if built(year) in flags:
        yield say(AGAIN, who=HOST)
        return

    known = MET in flags
    if known:
        yield say(AGAIN, who=HOST)
    else:
        yield say(HELLO, who=HOST)
        yield set_flag(MET)

    # THE FACTS COME BEFORE THE ACTIVITY AND NOT AFTER IT, every year, including to
    # somebody who heard them last year. The scored question at the end asks how you
    # join, so this is the line that makes it answerable, and an island that grades a
    # fact it did not give this sitting is grading what a student remembered from
    # September.
    yield say(WHEN_AND_HOW, who=HOST)

    yield objective("Follow him to the machine.")
    yield lead_to(HOST, DESK)
    if not known:
        yield say(THE_GAME, who=HOST)
    yield from the_offer()


@on_talk(TROPHIES)
def the_medals():
    """The plinth by the stair head. One line, and the wall says the rest.

    A place that shows you its medals is better than a person listing them, which
    is why this is one sentence and not a paragraph. Every number behind it is
    real and its source is in the island's own manifest.
    """
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
    """Ask, and then run it. Shared, because two roads reach the same moment.

    A student who follows the president gets here at the end of his walk, and one
    who wanders over to the lit machine on his own gets here by pressing it. Both
    are the same beat and neither should be a different island.
    """
    pick = yield choose([YES, NO], prompt=WANT_A_GO)
    # -1 is not an index. It is nobody having answered, because the student left
    # while the buttons were up, and it must never read as the first button.
    if pick != 0:
        yield say(COME_BACK, who=HOST)
        return

    yield from sit_down()


def sit_down():
    """The camera goes into the monitor, the screen opens, and it is scored.

    THE WAIT IS A BEAT AND NOT A FUDGE. `framing` comes back when the camera has
    arrived, so what the wait buys is a held moment looking at the machine before
    the screen takes the whole window.
    """
    yield objective("Fix the program.")
    yield framing(SCREEN)
    yield wait(SETTLE_MS)

    score = yield play(
        "the_program",
        title="The half-finished program",
        items=[THE_PROGRAM, HOW_YOU_JOIN],
    )

    # THE CAMERA COMES BACK WHATEVER HAPPENED. A shot raised and never lowered
    # leaves a student locked at 6.78 times zoom on a desk with the controls back
    # in their hands, which looks like the game has broken.
    yield framing(None)
    yield objective(None)

    # None is the student closing the screen without finishing, which is NOT a
    # zero. A zero is somebody who answered and got everything wrong, and writing
    # them down as the same thing is a lie on a transcript.
    if score is None:
        yield say(COME_BACK, who=HOST)
        return

    yield say(WELL_DONE, who=HOST)

    # ONE ROW ON THE RECORD, and `programme` is read out of the manifest rather
    # than typed again here. Two copies of one id drift, and the day they do a
    # student's grade lands on somebody else's row.
    yield award(
        programme=manifest()["programme"],
        grade=score,
        sticker="first-program",
    )
    year = yield get("year")
    yield set_flag(built(year))
    yield log("program_built", {"grade": score, "year": year})

    # THE LAST THING SAID ON THE ISLAND, and there is nothing to press. The student
    # committed a season to ATC on the year sheet before the ship ever sailed, so
    # asking whether they want to join would be asking about a decision the game
    # watched them make. What this does instead is name the step the game cannot
    # take for them.
    yield say(FORM, who=HOST)


# ---- WHAT IS ACTUALLY SCORED -------------------------------------------------
#
# Two items. The first is the club's own work and the second is about the club,
# and the island needs both: a maze on its own measures whether a fourteen year
# old can solve a maze.
#
# BOTH HALVES OF THE CLASS SEE THE SAME TWO ITEMS. One gets a screen with a body
# walking on it and one gets the same questions as a form. Same items, same order,
# same marks available. That is the whole study, and it only works if the
# difference between the two is the frame and never the content.

# THE GRID GOES WITH IT. Without the board drawn beside them, the form asks a
# student to put five instructions in order with no problem to solve, which stops
# being reasoning and becomes remembering. That is a different thing to measure,
# not a different way of showing it.
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
    # FIVE STEPS, AND `fwd3` IS THE ANSWER AT TWO OF THEM. That repeat is the
    # reason this is its own kind of item: scoring keys on the step and never on
    # the card, so two steps that want the same instruction still answer apart.
    "slots": [
        {"label": "Step 1", "move": "fwd2"},
        {"label": "Step 2", "move": "left"},
        {"label": "Step 3", "move": "fwd3"},
        {"label": "Step 4", "move": "right"},
        {"label": "Step 5", "move": "fwd3"},
    ],
    # the board the body walks. Read by the screen and by nothing that scores,
    # which is what keeps the walk a thing to watch rather than a second test.
    "board": {
        "cols": 6,
        "rows": 4,
        "walls": [[3, 2], [3, 3]],
        "flag": [5, 0],
        "start": {"col": 0, "row": 3, "facing": "east"},
    },
    "reply": "The wall is the whole puzzle. The turn has to come before it.",
}

# A `choice` AND NOT A `quiz`, because a choice carries a reply on every option.
# A student who picks the wrong one is told why it is wrong, which is worth more
# than being told they were wrong.
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
