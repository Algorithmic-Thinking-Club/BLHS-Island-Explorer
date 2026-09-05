"""The founding event: the first time a run walks into the Maw.

BRIEF-YEAR-ONE beat 4, word for word: "He walks in. The principal walks TO him.
One line: 'Welcome. Pick what you'll do this year.' The table lights. One screen
of big drawn cards. He picks."

It is here rather than in island.py because it is the only thing in this room
that DIRECTS: it moves a body that is standing on the map and hands the student
a screen. Every other handler is somebody saying a sentence or a panel opening.

READ THE SHAPE, NOT THE WORDS. A scene is small beats with air between them, and
the air is as much a part of it as the line.

WHY IT IS A `yield from` AND NOT A HANDLER. Nothing decorates the function below,
so the engine never calls it. `island.py` calls it with `yield from`, from two
places: the room's own opening, which is where a freshman meets it, and the
desk, for a run that walked off before it finished. That pipes every intent this
file yields out through the handler that asked, and the engine's answers back in.

WHAT THIS REPLACED. The first version of this scene was a station tour: three
lines pointing the room out with the camera, then an authored cutscene with two
speeches. Ash played it and ruled it constant dialogue that nobody reads
(BRIEF-SELF-EVIDENT). This is the same beat with the words taken out of it. The
tour is in this repository's history if anybody wants to read what a camera
tour looks like in these words.
"""
from vine import actor_move, actor_release, log, open, say, set_flag, wait

from lines import FACE, PRINCIPAL, WELCOME

# THE FLAG THE REST OF THE GAME READS, AND IT IS A BARE NAME.
#
# `src/game/run/objective.ts` sequences the whole of year one off this exact
# string, and the light that tells a student what to do next is on this desk
# until it is written. If it were written under this island's own programme id
# the founding would play, the flag would land as `the-maw:founding`, and the
# light would stay on the desk for four years with nothing saying why.
#
# It is bare because this island is the VINE'S OWN content and the engine runs it
# unscoped (`src/game/roster/vine-islands.ts` has the whole argument). YOUR
# island is scoped, and should be: you write `set_flag("met")` and the save holds
# `<your programme>:met`, so nobody else's island can collide with yours or read
# it. Do not copy these lines into a member island. You cannot make them work
# there and you would not want to.
FOUNDING = "maw:founding"

# THE HANDOVER. The corner shows the chart, the binder and the season pips from
# the first frame, and `src/game/hud/inventory.ts` fires an arrival flourish on
# each the first time it is really handed over, hung on these two flags. This is
# the beat that hands them over. The strings belong to `inventory.ts`.
CHART = "chart:granted"
HANDBOOK = "handbook:granted"

# THE YEAR'S OPENING SPEECH IS THIS LINE, IN PERSON.
#
# The engine carries a three-line year-start card from Principal Panther
# (`src/game/run/YearStart.tsx`) that mounts the moment the world is quiet and
# this flag is not set. After his one line and the pick screen, that card is a
# second principal saying three more things before the student is allowed to
# walk, which is the constant dialogue Ash ruled out. The principal has already
# opened the year, standing in front of you; this says so to the engine, and the
# year's own light moves straight to the table.
VIGNETTE = "vignette:y1"

# where he walks to: the spot the tunnel puts a student on. The one name on
# this map that means "where you are standing when you have just walked in".
MEET = "arrive_maw"

# how long the light sits on the table before the cards come up over it. Long
# enough to be SEEN lighting, which is the whole of what the light is for.
TABLE_LIT_MS = 900


def come_over():
    """The principal walks to where the student came in, and says so if he cannot.

    ONE OF THE PLACES THIS ISLAND CATCHES A REFUSAL, AND IT IS DECORATION. A word
    the engine cannot perform does not come back as a False you can test. It is
    RAISED at the line that yielded it, and if nothing catches it, it takes the
    rest of your handler with it. That is the right default for most words: an
    island whose beat silently never played is the failure the whole vocabulary
    exists to prevent, and a traceback with your own line number in it is the fix.

    So the question is never "should I catch refusals", it is "is this beat worth
    the scene". The walk is the beat's picture and the flag is its meaning. The
    flag is what the rest of the game reads to stop lighting this desk, and a
    room cut without a body bound to the desk is real: the game falls back to
    the copy of this room committed in the engine when it cannot reach the
    platform, and that copy binds no placements at all. There, he says the line
    from his desk.

    It still SAYS what refused. Swallowing it silently would be the other half of
    the same mistake.
    """
    try:
        yield actor_move(PRINCIPAL, MEET, facing="south-west")
        return True
    except Exception as refused:
        yield log("actor_move_refused", {"actor": PRINCIPAL, "to": MEET, "why": str(refused)})
        return False


def go_back():
    """Give him back to himself, walking to his desk first so he does not snap there.

    Letting a body go starts its own life up again from wherever the clock has
    got to, which for a man who breathes at a desk is the desk. Released where
    he stands he would be there in one frame. Walked back first, the snap is a
    step, and it happens under the cards.
    """
    try:
        yield actor_move(PRINCIPAL, PRINCIPAL)
        yield actor_release(PRINCIPAL)
    except Exception as refused:
        yield log("actor_release_refused", {"actor": PRINCIPAL, "why": str(refused)})


def founding_event(walk=True):
    """Everything from him noticing you to the cards being on screen.

    `walk` is False from the desk: a student who pressed E on the principal is
    standing in front of him already, and walking him to the door to say hello
    would be walking him away.
    """
    # ---- he comes to you ---------------------------------------------------
    came = True
    if walk:
        came = yield from come_over()

    # ---- one line --------------------------------------------------------------
    yield say(WELCOME, who=PRINCIPAL, portrait=FACE)

    # ---- the year begins, which is what lights the table ----------------------
    #
    # Four bare flags and no `guide_to`. The year's own sequencer reads these and
    # puts its light on the table, then on the fire once the sheet is stamped,
    # then on the way out. An arrow raised here would sit on the table after the
    # pick and hide the fire, because nothing after `open` below can take it down.
    yield set_flag(FOUNDING)
    yield set_flag(CHART)
    yield set_flag(HANDBOOK)
    yield set_flag(VIGNETTE)
    yield wait(TABLE_LIT_MS)

    # ---- and the cards ---------------------------------------------------------
    #
    # `open` comes back the instant the screen is up, not when it closes. So
    # this is the last thing the beat does that a student sees: the screen is
    # the pick, the pick stamps the sheet, and the year's light moves to the
    # fire on its own.
    yield open("planner")
    yield log("founding_seen", {"where": MEET if walk else PRINCIPAL, "walked": came})

    # under the cards, he goes back to his desk
    if walk and came:
        yield from go_back()
