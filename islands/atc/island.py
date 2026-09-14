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
    actor_face, award, choose, framing, get, guide_to, highlight, island_tasks,
    lead_to, log, objective, play, say, set_flag, sound, task_done, view, wait,
)

from lines import (
    AGAIN, COME_BACK, DESK, FORM, HELLO, HOST, MEDALS, NO,
    SECOND_YEAR, SECOND_YEAR_DESK, SECOND_YEAR_HOW, THE_GAME, TROPHIES,
    WANT_A_GO, WELL_DONE, WHEN_AND_HOW, YES,
)

# the shot somebody dragged onto the desk in MAPVIS. Naming it here rather than
# in the line that uses it means renaming the shot is a one-word edit.
SCREEN = "the_screen"

# ---- WHAT THIS ISLAND IS ASKING FOR, AS A LIST --------------------------------
#
# `objective` is the one line saying what to do NOW. This is the whole of it, drawn
# in the sheet under that line, and it is the thing that tells a student how much of
# your island is left. Ash asked for it by name: islands should always have tasks to
# do, and finishing them is what finishing the island means.
#
# TWO ROWS, BECAUSE THERE ARE TWO THINGS TO DO HERE. Resist the urge to write one
# row per line of dialogue: a row is a thing a student DOES, and being talked to is
# not one. When every row is ticked the game offers him the way back to the dock on
# its own, so the list is also how an island says it is over.
#
# The ids are what `task_done` is called with. The names are what a fourteen year
# old reads, and the notes say WHERE rather than how.
TASKS = [
    {"id": "meet", "name": "Meet the club president",
     "note": "He is at the top of the stair"},
    {"id": "program", "name": "Fix the half-finished program",
     "note": "On the computer that is switched on"},
]

# A BREATH AFTER THE CAMERA LANDS, and that is all it is now.
#
# `framing` used to answer the instant it was asked, so this number was the whole
# of the push-in and it was a guess: the camera takes as long as it takes and the
# screen opened somewhere in the middle of the move. The engine's `framing` waits
# for its own camera now, so what is left here is a held moment on the machine
# before the screen takes over, which is a beat rather than a fudge.
# 260 was a blink. Ash, on playing it: "the zoom in shot was meant to go from a 3d
# view to a smooth 2d view of the computer, then the screen shows up as a panel." The
# push lands and then the panel arrives almost on the same frame, so there is no shot
# of the machine to see, only a camera move that is interrupted. Long enough to read
# the thing the camera has stopped on, short enough that nobody is waiting.
SETTLE_MS = 850

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

    # THE LIST GOES UP EVERY TIME AND THAT IS CORRECT. `island_tasks` replaces
    # whatever was declared rather than adding to it, and which rows are already
    # ticked comes back out of the save, so saying it on every load is the plainest
    # thing to write and also the right thing.
    yield island_tasks(TASKS)

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
        # AND MEETING HIM STILL COUNTS, WHENEVER IT HAPPENS. The machine can be
        # pressed without ever speaking to him, so a student who walks up to the lit
        # computer first finishes the program and then finds him afterwards. Without
        # this line that student left "Meet the club president" unticked for the rest
        # of the year: the row could only be ticked below, and below is unreachable
        # once the club is finished. The island sat at one of two for ever and the
        # way back never appeared.
        yield task_done("meet")
        return

    # ---- THEY LOOK AT EACH OTHER BEFORE EITHER OF THEM SPEAKS -------------
    #
    # ASH, after playing: *"his stops + facings + positions are goofy"* and, of the
    # player, *"thor's facings in cutscenes"*. `actor_face` has existed for both of
    # them since engine wave 4 and no island had ever called it once, so every
    # conversation in this game was two people talking past each other at whatever
    # angle they happened to stop on. It is two lines.
    #
    # CAUGHT, BOTH OF THEM. A facing is a nicety and a refusal must never cost a
    # student the club: an anchor that has moved, art with no such heading, or a body
    # somebody else is driving all come back here as an exception.
    try:
        yield actor_face(HOST, "thor")
        yield actor_face("thor", HOST)
    except Exception as refused:
        yield log("actor_face_refused", {"why": str(refused)})

    # ---- WHICH TIME IS THIS -----------------------------------------------
    #
    # ASH: *"we can do a club again over years? is it meant to play different stuff?"*
    #
    # `get("rank")` is about YOUR island and you never name it: it comes back with how
    # many EARLIER years a student has finished this programme, which years they were,
    # the best grade they got, and the rung of any ladder the club keeps. A member
    # writing their own island gets the same question for free.
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

    # THE FACTS COME BEFORE THE ACTIVITY AND NOT AFTER IT, every year, including to
    # somebody who heard them last year. The scored question at the end asks how you
    # join, so this is the line that makes it answerable, and an island that grades a
    # fact it did not give this sitting is grading what a student remembered from
    # September.
    # AND HE IS NOT TOLD WHERE 303 IS TWICE. The scored question at the end asks how
    # you join, so a first-year has to hear it this sitting; somebody on their second
    # year answered it last year and gets the line that belongs to having come back.
    yield say(SECOND_YEAR_HOW if returning else WHEN_AND_HOW, who=HOST)

    # TICKED WHERE IT BECOMES TRUE, which is after he has spoken and not before.
    # A row that ticks itself on the way in is a list that lies about how far along
    # somebody is. Said again at the top of this handler for the student who pressed
    # the machine before he ever spoke to anybody.
    yield task_done("meet")

    yield objective("Follow him to the machine.")
    yield lead_to(HOST, DESK)
    # AND HE TURNS ROUND AT THE END OF IT, so the next line is said to a face.
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
    # ---- THE ARROW COMES DOWN, AND THE MACHINE LIGHTS UP ------------------
    #
    # `guide_to(HOST)` is raised on every load with the club still owed, and nothing
    # ever took it back down: a student standing at the machine being asked whether
    # he wants a go had a floating arrow and a road of marks across the floor still
    # pointing at a man two feet away. Both roads into this beat pass through here.
    #
    # AND THEN THE RIGHT ONE IS LIT. There are eight computers on this terrace and
    # exactly one of them is switched on. `guide_to` would be the wrong word for that:
    # it shouts GO THERE and draws a road across a floor he is already standing on.
    # `highlight` is the quiet half of the same idea and says only WHICH ONE.
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
        # and the light goes out with the offer, because a lit machine he has just
        # said no to is the island still asking
        yield highlight(None)
        yield say(COME_BACK, who=HOST)
        # AND THE PANEL GOES BACK TO THE YEAR. "Follow him to the machine." was left
        # on the glass for ever by a student who followed him to the machine and then
        # said not right now: a sentence telling him to do the thing he is standing in
        # front of and has just declined.
        yield objective(None)
        return

    yield from sit_down()


def sit_down():
    """The camera goes into the monitor, the screen opens, and it is scored.

    THE WAIT IS A BEAT AND NOT A FUDGE. `framing` comes back when the camera has
    arrived, so what the wait buys is a held moment looking at the machine before
    the screen takes the whole window.
    """
    yield highlight(None)
    yield objective("Fix the program.")
    # ---- HE SITS DOWN, AND THE ROOM GOES AWAY ----------------------------
    #
    # ASH: *"the zoom in shot was meant to go from a 3d view to a smooth 2d view of
    # the computer, then the screen shows up as a panel."*
    #
    # Inside the bars, so the corner, the plaque and the arrow all stand down for the
    # length of it and come back afterwards even if the screen below refuses. The
    # click is the machine waking: a beat with a sound in it is a beat, and a beat
    # with nothing in it is a wait.
    try:
        yield sound("click")
    except Exception as refused:
        yield log("sound_refused", {"why": str(refused)})
    yield framing(SCREEN)
    yield wait(SETTLE_MS)

    # THE CAMERA COMES BACK WHATEVER HAPPENED, AND THAT NEEDS A try/finally.
    #
    # It used to be two plain lines after `play`, which only run when `play` RETURNS.
    # `play` can also REFUSE: the engine checks every question before it will draw one,
    # so a step naming an instruction that does not exist, two questions sharing an id,
    # or a misspelt kind all arrive here as an exception at this line. And this is the
    # island a member copies, so a typo in the list below is the most likely thing that
    # will ever happen to this file.
    #
    # Without the finally, that typo left a student at eight times zoom staring at a
    # desk with the controls back in his hands and "Fix the program." across the top of
    # the screen, which looks exactly like the game breaking. With it, he gets the room
    # back and the engine says what was wrong at the member's own line.
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
        # AND THE ROOM COMES BACK BEFORE ANYBODY SPEAKS IN IT. `framing(None)` hands
        # the camera back to the follow law, which eases; a line said on the frame
        # after it is a line said over a camera still travelling.
        yield view("close", 900)

    # None is the student closing the screen without finishing, which is NOT a
    # zero. A zero is somebody who answered and got everything wrong, and writing
    # them down as the same thing is a lie on a transcript.
    if score is None:
        yield say(COME_BACK, who=HOST)
        return

    yield task_done("program")
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
