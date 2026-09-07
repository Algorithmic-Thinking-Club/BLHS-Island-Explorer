"""THE RAIL: year one in the Maw, tunnel mouth to "Year two, next time".

BRIEF-MAW-RAIL-2, 2026-09-06, after Ash played the first rail: *"Still many UI
glitches, and still unclear game overall. Everything inside the cutscene should
disable the three boxes in the corner and have the two black rectangles
throughout the cutscene until it ends. Everything in the cutscene should be
clear and easy to follow and make sense WHY it is happening. I have no idea what
is going on: a fire, click two classes, it makes no sense. And if you think more
text is the answer, we are doomed."*

The first rail walked Thor alone from station to station with a line at each, and
nobody could tell why he was standing at a fire. So this is the same five beats
with the one thing that makes them make sense: the principal walks AHEAD and the
student follows him, which is what a freshman orientation IS. The person in
charge takes you round, stops, turns to face you, and says the one sentence that
says why you are standing here. Then the thing happens.

  1  THE TUNNEL      he is already waiting there and says the one line
  2  THE TABLE       he leads, you follow, your schedule opens, you fill it in
  3  THE FIRE        he leads, you follow, Advisory is three things by hand
  4  THE WALL        he leads, you follow, the wall opens on what you picked
  5  THE COUNSELOR   he leads, she has the cord, the page turns, year two

IT IS ONE MOVIE FROM END TO END, and that is the other half of what he asked
for. The bars go up when the painting appears and come down once, after "Year
two, next time". The first rail raised them for each two second walk and dropped
them for each screen, and those four seams in the middle are the glitches he saw.
While they are up the corner is gone, the plaques are gone, the task line is
gone, and every press in the room is dropped, so a wrong click does nothing,
which is what a rail is.

AND IT IS WATCHED FROM HIS SHOULDER. `view("close")` is the character point of
view, twice the shot the room opens at: it is never all on screen at once and the
camera rides him the whole way. It is handed back at the end.

THERE IS NO WAY OUT OF IT EITHER, which Ash ruled after playing: no "Leave this
for now" on Advisory, no "Close for now" on the schedule, no Escape, no doors and
no stations. The engine reads the bars being up as the statement that something
else is directing, so every panel raised inside them loses its dismiss.

IT IS RESUMABLE AT EVERY BEAT, which is the other half of being one handler. It
does not remember where it got to; it ASKS the run, the same way `objective.ts`
does, so a student who reloads the tab mid-year is picked up at the beat they
were standing in rather than walked through four they have already done.

AND IT LETS GO WHEN THE STUDENT DOES. A beat that ends without its decision being
made goes through `step_off` rather than walking him on with an empty sheet: the
camera comes back, the principal is his own again, the bars come down in
`as_a_cutscene`'s own `finally`, and what he gets is the room with one thing lit,
which is the game he had before the rail. Pressing that thing puts him back on
it. With nothing pickable on the schedule today that road is only reachable by
leaving Advisory, and Advisory has no way out while the bars are up.
"""
from vine import (  # noqa: A004 (open is the engine's word)
    actor_release, as_a_cutscene, get, guide_to, lead_to, log, open, place, play,
    say, set_flag, view,
)

from lines import (
    ADVISORY_IS_MONDAY, COME_BACK, CORD, COUNSELOR, FACE, NEXT_TIME, PRINCIPAL,
    SCHEDULE_IS_YOURS, STAMP_IT, WALL_IS_YOURS, WELCOME,
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

# THE CORNER, HANDED OVER WHEN THE BARS COME DOWN AND NOT BEFORE.
#
# `src/game/hud/inventory.ts` fires an arrival flourish on each of the three
# corner buttons the first time it is really granted, hung on these two flags.
# They used to be written in beat 1, which is now inside the movie: the corner is
# hidden for the whole of it, so the one moment those buttons are supposed to
# arrive was a moment nobody could see. Written at the end instead, on the frame
# the student gets the room. The strings belong to `inventory.ts`.
CHART = "chart:granted"
HANDBOOK = "handbook:granted"

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
# The engine stops him a body length short of it rather than on top of the
# student, because a person walking over to meet you stops in front of you.
MEET = "arrive_maw"

# the four places the rail leads him to, in order
TABLE = "chart_table"
FIRE = "hearth"
WALL = "trophy_wall"
DESK = "counselor"

# how many times the rail will offer the same screen again before it lets go. A
# student who closes the schedule twice has told you something.
OFFERS = 3


def vignette(year):
    """The engine's own year-start card for a year, once it has been seen.

    THE YEAR'S OPENING SPEECH IS BEAT 1, IN PERSON. `src/game/run/YearStart.tsx`
    mounts a three-line card from Principal Panther the moment the world is quiet
    and this flag is not set. After his one line and the schedule, that card is a
    second principal saying three more things before the student is allowed to
    walk, which is the constant dialogue Ash ruled out.
    """
    return "vignette:y%d" % year


def turned(year):
    """The flag the engine writes the moment a year's page has turned."""
    return "yearbook:y%d" % year


def waiting_at_the_door():
    """He is ALREADY at the tunnel mouth when the student walks in.

    Ash, 2026-09-06, watching it: *"THE PRINCIPAL DOES NOT WALK TO THOR ANY MORE.
    He is ALREADY WAITING at the tunnel mouth when Thor comes in."* And on the
    walk that used to be here: *"he flies upward, across the edge."* That walk was
    `actor_move`, which carries a body in a straight line at its target, so on a
    room with a gap between the bridge and the floor he crossed the gap. It is cut
    rather than fixed: a person who is already there when you arrive is the better
    picture anyway, and it is what a real orientation looks like.

    `place` is a word this island could not say until today. It puts a body at an
    anchor with no walk in it, beside the player rather than on top of him, turned
    to look at him. It is the first thing the rail does, before the camera moves,
    so there is no frame with him standing anywhere else.

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
        yield place(PRINCIPAL, MEET)
        return True
    except Exception as refused:
        yield log("place_refused", {"actor": PRINCIPAL, "at": MEET, "why": str(refused)})
        return False


def let_go():
    """He is his own again, and he stays where the rail left him.

    HE DOES NOT WALK HOME, AND THAT IS A MISSING WORD, NOT A CHOICE. `actor_move`
    goes to an anchor's stand point, and a bound anchor's stand point travels with
    the body, so "walk to your own desk" walks him twelve pixels to his own stand
    offset and stops. Every name bound to him moves with him, the room carries no
    unbound point at the desk, and a name the room does not carry is refused. So
    there is no way to say "back to where you started" today; one point anchor at
    the desk in MAPVIS, or one engine word, would give it.

    Until then he is back at his desk the next time the room loads.
    """
    try:
        yield actor_release(PRINCIPAL)
    except Exception as refused:
        yield log("actor_release_refused", {"actor": PRINCIPAL, "why": str(refused)})


def take_him(anchor):
    """The rail's one move: he leads, the student follows, and nobody is told to.

    THE ORDER IS THE WHOLE BEAT AND IT IS DELIBERATE.

    `guide_to` puts the light on the floor, the drawn arrows along the route and
    the big pointer over the thing at the end of it. Then `lead_to` walks the
    principal there with the student two body lengths behind him, and turns him
    round to face the student when they both stop, which is the frame the line is
    said on.

    NO `look_at` ANY MORE. The first rail sent the camera to each station for a
    second before setting off, and this one is watched from the student's own
    shoulder the whole way: a second of the camera somewhere he is not is a cut in
    the middle of a cutscene, and Ash asked for character point of view
    everywhere. The thing he is walking towards lights up and he walks towards it,
    and that is the teaching.

    NO `movie` HERE EITHER. The bars are up for the whole rail and this is inside
    it, which is the difference between this and the first version: they used to
    go up and come down around each walk, and those seams are what he saw.

    AND NO FACING IS NAMED. `lead_to` turns the two of them to look at each other
    when they stop, because which way "at him" is depends on where they both ended
    up and no compass point written here would survive somebody moving a table.

    EVERY WORD IS CAUGHT. A refusal in the middle of a beat would take the rest of
    year one with it, and the beat after this one is a screen that can still be
    filled in from a standstill.
    """
    try:
        yield guide_to(anchor)
    except Exception as refused:
        yield log("guide_refused", {"anchor": anchor, "why": str(refused)})

    try:
        yield lead_to(PRINCIPAL, anchor, pace="walk")
    except Exception as refused:
        yield log("lead_to_refused", {"anchor": anchor, "why": str(refused)})


def step_off():
    """The rail lets go: arrow down, camera back, the principal his own again.

    Every road out of `year_one` runs through here. The BARS are not here and that
    is the point of `as_a_cutscene`: they come down in its `finally`, so they come
    down on a road nobody wrote as well as on the four that are written.
    """
    yield guide_to(None)
    yield from let_go()
    yield view("walk")


# ---- the five beats ----------------------------------------------------------


def the_tunnel(walk):
    """BEAT 1. He is at the mouth, the principal is already there, one line."""
    yield say(WELCOME, who=PRINCIPAL, portrait=FACE)

    # the year has begun, which is what lights the table. Two bare flags and no
    # `guide_to`: the year's own sequencer reads these and puts its light on the
    # table, and `take_him` raises the rail's own on top of it a moment later.
    year = yield get("year")
    yield set_flag(FOUNDING)
    yield set_flag(vignette(year))
    yield log("founding_seen", {"where": MEET if walk else PRINCIPAL})


def the_table():
    """BEAT 2. He leads him to the table and his schedule opens.

    Comes back True when the schedule is really stamped. The screen is offered
    again when it is closed unstamped, because closing it is not a decision and
    walking him to the fire with an empty schedule would be the rail losing the
    one thing it walked him here for. Three times, and then it lets go: a student
    who has shut the same screen three times is telling you to leave them alone,
    and the year's own light is still on this table when they change their mind.
    """
    yield from take_him(TABLE)
    yield say(SCHEDULE_IS_YOURS, who=PRINCIPAL, portrait=FACE)

    planned = False
    for _ in range(OFFERS):
        yield open("planner", wait=True)
        planned = yield get("planned")
        if planned:
            break
        yield say(STAMP_IT, who=PRINCIPAL, portrait=FACE)

    # NOTHING IS SAID AFTER THE STAMP. It pops in the world naming what he chose,
    # which is the answer, and the line that used to be here handed over a corner
    # button that is not on the screen while the bars are up.
    return planned


def the_fire(beat):
    """BEAT 3. He leads him to the fire and Advisory is three things by hand.

    ONE LINE, AND IT IS THE WHY. "This is Advisory. Every Monday starts here" is
    the whole of what a freshman needs before the questions: it names the real
    thing and says when it happens. The activity has one short line before each of
    its three items and pops right or wrong on the spot, and the grade pops over
    the map instead of opening a card of a hundred words.

    NO `award` HERE, DELIBERATELY, and this is the one place this island breaks
    the rule your own island must keep. A member's island scores its own content
    and has to write the row itself. A core beat is the ENGINE'S content: the
    runner already wrote the grade, the credit, the tags and the facts before this
    line ran, and awarding again would put a second row for the same year on the
    transcript and move the GPA twice.
    """
    yield from take_him(FIRE)
    yield say(ADVISORY_IS_MONDAY, who=PRINCIPAL, portrait=FACE)

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
    return True


def the_wall():
    """BEAT 4. He leads him to the wall and it opens on what he picked.

    The panel is the readout: one frame per thing he chose, filled where he has
    earned it and honestly empty where he has not, in his own picks' names. The
    one line says why he is looking at it and nothing else.
    """
    yield from take_him(WALL)
    yield say(WALL_IS_YOURS, who=PRINCIPAL, portrait=FACE)
    yield open("wall", wait=True)
    yield set_flag(WALL_SHOWN)


def the_counselor(year):
    """BEAT 5. He leads him to her, the cord, the page turns, "Year two, next time".

    THE PRINCIPAL LEADS AND THE COUNSELOR SPEAKS, which is the one beat with two
    people in it and is right: he has walked the student round all morning and she
    is the person who closes a year at a school.

    The yearbook is where the page turns, in school words, and where the cord is
    draped; both of those are the engine's own screens, raised here by name. It
    comes back True only when the page really turned, because a student who opened
    the book and closed it again has not finished year one and the rail must not
    say he has.
    """
    yield from take_him(DESK)
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


def year_one(walk):
    """Every beat the run still owes, in order. Read top to bottom.

    It is the same shape `objective.ts` uses to decide what the one lit thing is,
    asked of the same facts, and that is on purpose: the sequencer and the rail
    cannot disagree about where a student is in the year because they are reading
    the same run.
    """
    flags = yield get("flags")
    first = FOUNDING not in flags

    # HE IS PLACED BEFORE THE CAMERA MOVES, so there is no frame of him standing
    # at his desk while the shot travels in.
    if first and walk:
        yield from waiting_at_the_door()

    # THE SHOT IS THE STUDENT'S OWN SHOULDER for the whole of what follows.
    yield view("close")

    if first:
        yield from the_tunnel(walk)

    planned = yield get("planned")
    if not planned:
        planned = yield from the_table()
        if not planned:
            yield from step_off()
            return

    beat = yield get("advisory")
    if beat is not None:
        sat = yield from the_fire(beat)
        if not sat:
            yield from step_off()
            return

    flags = yield get("flags")
    if WALL_SHOWN not in flags:
        yield from the_wall()

    year = yield get("year")
    flags = yield get("flags")
    if turned(year) not in flags:
        closed = yield from the_counselor(year)
        if not closed:
            yield from step_off()
            return

    # YEAR TWO DOES NOT OPEN WITH A SPEECH. The page has just turned, the run is
    # now in year two, and the engine's own year-start card would mount the moment
    # the world went quiet and say three more things over the top of "Year two,
    # next time". BRIEF-MAW-RAIL-2: that line is the last one a student reads.
    # Written here rather than left to the engine because the principal really has
    # opened both years in person, standing in front of him.
    year = yield get("year")
    yield set_flag(vignette(year))

    # AND THE CORNER ARRIVES. The three buttons have been hidden for the whole
    # cutscene; these two flags are what makes them swing down on their hooks on
    # the frame the bars come off, which is the moment the room becomes his.
    yield set_flag(CHART)
    yield set_flag(HANDBOOK)
    yield set_flag(RAILED)
    yield from step_off()
    yield log("rail_done", {"year": year})


def rail(walk=True):
    """Year one, run inside the bars, which come down whatever happens.

    `as_a_cutscene` is `movie(True)`, the scene, and `movie(False)` in a `finally`.
    It is the shape a member should copy for anything a student WATCHES, and it
    exists because the gap between those two lines is the one place in this API
    where forgetting leaves somebody behind two black bars with no controls. Here
    the scene is six or seven minutes long with four screens inside it, and any
    word in it can refuse; the bars still come down.
    """
    yield from as_a_cutscene(year_one(walk))
