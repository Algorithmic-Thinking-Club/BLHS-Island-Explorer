"""THE RAIL: year one in the Maw, tunnel mouth to "Year two, next time".

BRIEF-MAW-RAIL, 2026-09-06, after Ash played the Maw: *"the entire panther maw
cutscene is broken, and the game itself is extremely confusing, a bunch of words,
a bunch of instructions that open to read more words. A student doesn't know what
the hell is going on. It needs to feel like Prodigy."*

Prodigy is never a menu. It is a RAIL with choices on it: the game walks you to
the next thing, one character says one line, you do one thing with your hands,
something pops, and the game walks you to the next thing. You are never lost
because you are never asked where to go. This file is that, in five beats:

  1  THE TUNNEL      the cover lifts, he is at the mouth, the principal walks to
                     him at walking pace and says one line
  2  THE TABLE       it lights, the camera goes to it, he walks himself there,
                     the pick screen opens, the stamp pops
  3  THE FIRE        it lights, he walks himself there, Advisory is three things
                     done by hand and the pop is the result
  4  THE WALL        he walks himself to it, the wall opens, nothing to read
  5  THE COUNSELOR   one line, the cord, the page turns, "Year two, next time"

Then the Maw is his to walk.

WHY THIS IS ONE HANDLER AND NOT FIVE. Between beat 1 and beat 5 nothing in the
room may be pressed: not the outfitter, not the desk, not the doors. That is what
a rail IS, and an open handler already gives it. The engine drops every press in
a room while an island is inside one, so the lock costs no engine word at all,
and the walking stretches, which are the only part of the rail with no panel
holding the controls, are covered by `movie` for the same reason the arrival's
walk up the hub is (`islands/the-hub/island.py`).

IT IS RESUMABLE AT EVERY BEAT, which is the other half of being one handler. It
does not remember where it got to; it ASKS the run, the same way `objective.ts`
does, so a student who reloads the tab mid-year is picked up at the beat they
were standing in rather than walked through four they have already done. Every
beat's doneness is a fact about the run: the founding flag, `get("planned")`,
`get("advisory")`, a flag for the wall, and the yearbook's own page flag.

AND IT LETS GO WHEN THE STUDENT DOES. A beat that ends without its decision
being made, the cards closed unstamped or Advisory left half answered, RETURNS
rather than walking him on with an empty sheet. The year's own light is already
on that station, so what he gets is the game he had before the rail, which is a
menu with one thing lit, and pressing that thing puts him back on the rail.
"""
from vine import (  # noqa: A004 (open is the engine's word)
    actor_move, actor_release, get, guide_to, log, look_at, movie, open, play,
    say, set_flag, walk_to,
)

from lines import (
    COME_BACK, CORD, COUNSELOR, FACE, GUIDE_IS_YOURS, NEXT_TIME, PRINCIPAL,
    STAMP_IT, WELCOME, YEAR_SET,
)

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

# THE HANDOVER. The corner shows Map, Guide and My Year from the first frame, and
# `src/game/hud/inventory.ts` fires an arrival flourish on each the first time it
# is really handed over, hung on these two flags. This is the beat that hands
# them over. The strings belong to `inventory.ts`.
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

# beat 4 has no other trace in the run. Everything else the rail does is written
# somewhere the save already keeps, and looking at a wall is not.
WALL_SHOWN = "maw:wall_shown"

# and the whole thing is over. Read by `island.py` so the room stops opening on a
# rail once the year has turned.
RAILED = "maw:railed"

# the last line of the thirty minutes has been said
NEXT_TIME_SAID = "maw:next_time"

# where he walks to in beat 1: the spot the tunnel puts a student on. The one
# name on this map that means "where you are standing when you have just come in".
MEET = "arrive_maw"

# the four places the rail walks him to, in order
TABLE = "chart_table"
FIRE = "hearth"
WALL = "trophy_wall"
DESK = "counselor"

# how long the camera holds on a thing before he sets off for it. Long enough to
# see it light and to see where it is, short enough that nobody is waiting.
LOOK_MS = 1000

# how many times the rail will offer the same screen again before it lets go. A
# student who closes the pick cards twice has told you something.
OFFERS = 3


def turned(year):
    """The flag the engine writes the moment a year's page has turned."""
    return "yearbook:y%d" % year


def come_over():
    """The principal walks to where the student came in, and says so if he cannot.

    AT WALKING PACE, WITH HIS LEGS MOVING, which is BRIEF-ARRIVAL item 6 and Ash's
    own reading of the first build: *"The principal sprints out, glitched."* A
    driven body travels at the MAP's speed, which is the player's own sprint, so
    he crossed the room in four seconds. `pace` is the word for it and this is the
    only place in the game that needed it.

    ONE OF THE PLACES THIS ISLAND CATCHES A REFUSAL, AND IT IS DECORATION. A word
    the engine cannot perform does not come back as a False you can test. It is
    RAISED at the line that yielded it, and if nothing catches it, it takes the
    rest of your handler with it. That is the right default for most words: an
    island whose beat silently never played is the failure the whole vocabulary
    exists to prevent, and a traceback with your own line number in it is the fix.

    So the question is never "should I catch refusals", it is "is this beat worth
    the scene". The walk is the beat's picture and the flag is its meaning, and
    here the flag is the rest of year one. A room cut without a body bound to the
    desk is real: the game falls back to the copy of this room committed in the
    engine when it cannot reach the platform, and that copy binds no placements at
    all. There, he says the line from his desk and the rail carries on.

    It still SAYS what refused. Swallowing it silently would be the other half of
    the same mistake.
    """
    try:
        yield actor_move(PRINCIPAL, MEET, facing="south-west", pace="walk")
        return True
    except Exception as refused:
        yield log("actor_move_refused", {"actor": PRINCIPAL, "to": MEET, "why": str(refused)})
        return False


def let_go():
    """He is his own again, and he stays where he came to.

    HE DOES NOT WALK HOME, AND THAT IS A MISSING WORD, NOT A CHOICE. `actor_move`
    goes to an anchor's stand point, and a bound anchor's stand point travels with
    the body, so "walk to your own desk" walks him twelve pixels to his own stand
    offset and stops. Every name bound to him moves with him, the room carries no
    unbound point at the desk, and a name the room does not carry is refused. So
    there is no way to say "back to where you started" today; one point anchor at
    the desk in MAPVIS, or one engine word, would give it.

    Until then he stays by the door, where he came to meet the student, and is
    back at his desk the next time the room loads.
    """
    try:
        yield actor_release(PRINCIPAL)
    except Exception as refused:
        yield log("actor_release_refused", {"actor": PRINCIPAL, "why": str(refused)})


def show_the_way(anchor):
    """Light a place, look at it, and walk him to it. The rail's one move.

    THE ORDER IS THE WHOLE BEAT AND IT IS DELIBERATE.

    `guide_to` puts the light on the floor, the chevron over the thing and the
    drawn marks along the route. `look_at` takes the camera there for a second,
    so the student SEES the thing light before anybody moves: that second is the
    only teaching in the beat and it is worth its own line.

    Then the bars go up and he walks. The bars are not decoration here, they are
    the lock: a walking stretch is the one part of the rail with no panel holding
    the controls, and without them a click on the floor re-aims the walk, a click
    on a door leaves the room, and the rail carries on talking to somebody who is
    somewhere else. `movie` is the shipped word for hands off, it is what the
    arrival up the hub already walks behind, and the marks and the light stay
    drawn underneath it because the engine keeps them up for a walk somebody is
    watching.

    EVERY WORD HERE IS CAUGHT AND THE BARS COME DOWN EITHER WAY. A refusal
    between `movie(True)` and `movie(False)` would leave a student behind two
    black bars with no controls, which is a dead session that looks like a dead
    laptop. The engine has a ceiling for that and it should never be reached.
    """
    try:
        yield guide_to(anchor)
        yield look_at(anchor, LOOK_MS)
    except Exception as refused:
        yield log("guide_refused", {"anchor": anchor, "why": str(refused)})

    yield movie(True)
    try:
        yield walk_to(anchor)
    except Exception as refused:
        yield log("walk_to_refused", {"anchor": anchor, "why": str(refused)})
    yield movie(False)


# ---- the five beats ----------------------------------------------------------


def the_tunnel(walk):
    """BEAT 1. He is at the mouth, the principal comes to him, one line.

    `walk` is False from the desk: a student who pressed E on the principal is
    standing in front of him already, and walking him to the door to say hello
    would be walking him away.
    """
    came = True
    if walk:
        came = yield from come_over()

    yield say(WELCOME, who=PRINCIPAL, portrait=FACE)

    # the year has begun, which is what lights the table. Four bare flags and no
    # `guide_to`: the year's own sequencer reads these and puts its light on the
    # table, and `show_the_way` raises the rail's own on top of it a moment later.
    yield set_flag(FOUNDING)
    yield set_flag(CHART)
    yield set_flag(HANDBOOK)
    yield set_flag(VIGNETTE)
    yield log("founding_seen", {"where": MEET if walk else PRINCIPAL, "walked": came})

    if walk and came:
        yield from let_go()


def the_table():
    """BEAT 2. The table lights, he walks to it, he picks his year.

    Comes back True when the sheet is really stamped. The screen is offered again
    when it is closed unstamped, because closing it is not a decision and walking
    him to the fire with an empty sheet would be the rail losing the one thing it
    walked him here for. Three times, and then it lets go: a student who has shut
    the same screen three times is telling you to leave them alone, and the year's
    own light is still on this table when they change their mind.
    """
    yield from show_the_way(TABLE)

    planned = False
    for _ in range(OFFERS):
        yield open("planner", wait=True)
        planned = yield get("planned")
        if planned:
            break
        yield say(STAMP_IT, who=PRINCIPAL, portrait=FACE)

    if not planned:
        return False

    # the stamp has already popped, in the world, naming what he chose. This is
    # the one line of the beat and it hands over the corner's middle button.
    yield say(YEAR_SET, who=PRINCIPAL, portrait=FACE)
    return True


def the_fire(beat):
    """BEAT 3. The fire lights, he walks to it, Advisory is three things by hand.

    NO SPEECH AROUND IT. What used to be here was a line before and a line after,
    on top of six inside the activity itself. The activity is three items with one
    short line each now, every answer pops right or wrong on the spot, and the
    grade pops over the map instead of opening a card of a hundred words. So the
    only thing this beat says is the Guide's handover, once, on the way out.

    NO `award` HERE, DELIBERATELY, and this is the one place this island breaks
    the rule your own island must keep. A member's island scores its own content
    and has to write the row itself. A core beat is the ENGINE'S content: the
    runner already wrote the grade, the credit, the tags and the facts before this
    line ran, and awarding again would put a second row for the same year on the
    transcript and move the GPA twice.
    """
    yield from show_the_way(FIRE)

    # BOTH ARMS OF THE STUDY RUN THROUGH THIS ONE WORD, and the arm is not this
    # island's to choose. Left alone, `play` renders whichever arm the student was
    # assigned when they joined: the game arm answers with a pop, the plain arm
    # with the same questions as a form and a printed result. Same items, same
    # order, same score.
    score = yield play(beat)

    # None is the player closing the panel, which is not a zero. A zero is a
    # student who answered and got everything wrong, and the two must never be
    # written down as the same thing.
    if score is None:
        yield say(COME_BACK, who=PRINCIPAL, portrait=FACE)
        return False

    yield log("advisory_sat", {"beat": beat, "grade": score})
    yield say(GUIDE_IS_YOURS, who=PRINCIPAL, portrait=FACE)
    return True


def the_wall():
    """BEAT 4. He walks to the wall and looks at what filled. Nothing to read.

    The panel is the readout: one frame per thing he picked, filled where he has
    earned it and honestly empty where he has not, in his own picks' names. There
    is no line here because there is nothing a person could say that the frames
    are not already saying better.
    """
    yield from show_the_way(WALL)
    yield open("wall", wait=True)
    yield set_flag(WALL_SHOWN)


def the_counselor(year):
    """BEAT 5. One line, the cord, the page turns, "Year two, next time".

    The yearbook is where the page turns, in school words, and where the cord is
    draped; both of those are the engine's own screens, raised here by name. It
    comes back True only when the page really turned, because a student who opened
    the book and closed it again has not finished year one and the rail must not
    say he has.
    """
    yield from show_the_way(DESK)
    yield say(CORD, who=COUNSELOR)
    yield open("yearbook", wait=True)

    flags = yield get("flags")
    if turned(year) not in flags:
        return False

    yield say(NEXT_TIME, who=COUNSELOR)
    yield set_flag(NEXT_TIME_SAID)
    yield log("year_two_next_time")
    return True


# ---- the rail ----------------------------------------------------------------


def rail(walk=True):
    """Every beat the run still owes, in order, as one handler.

    Read top to bottom: it is the same shape `objective.ts` uses to decide what
    the one lit thing is, asked of the same facts, and that is on purpose. The
    sequencer and the rail cannot disagree about where a student is in the year
    because they are reading the same run.
    """
    flags = yield get("flags")
    if FOUNDING not in flags:
        yield from the_tunnel(walk)

    planned = yield get("planned")
    if not planned:
        planned = yield from the_table()
        if not planned:
            yield guide_to(None)
            return

    beat = yield get("advisory")
    if beat is not None:
        sat = yield from the_fire(beat)
        if not sat:
            yield guide_to(None)
            return

    flags = yield get("flags")
    if WALL_SHOWN not in flags:
        yield from the_wall()

    year = yield get("year")
    flags = yield get("flags")
    if turned(year) not in flags:
        closed = yield from the_counselor(year)
        if not closed:
            yield guide_to(None)
            return

    # THE ARROW COMES DOWN AND THE ROOM IS HIS. `guide_to` is set by this file and
    # cleared by nothing else, so without this line the last thing the rail
    # pointed at keeps an arrow over it for the rest of the visit, outranking the
    # year's own next step the whole time.
    yield guide_to(None)
    yield set_flag(RAILED)
    yield log("rail_done", {"year": year})
