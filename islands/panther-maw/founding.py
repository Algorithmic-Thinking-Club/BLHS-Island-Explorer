"""THE FILM, second half: the tunnel mouth to the handover.

BRIEF-INTRO-FILM, Ash 2026-09-07, after playing rail-4: *"The cutscene is the
introduction, for every user: it plays, it ends, and the user is left to play the
actual game."*

IT IS ONE FILM AND IT DOES NOT START HERE. The bars go up on the beach, the
frame the student presses Set Sail in, and the hub's own island
(`islands/the-hub/island.py`) plays the first half of it: the crossing, the
arrival card over the whole island, and the walk up the quay. The tunnel door
does not end it either, because the engine carries the frame through a door the
film walked through. So by the time this file runs, the bars have been up for
about half a minute and `movie(True)` on the first line is already true.

It ends in exactly one place, `the_handover`, and it ends by handing over the
three corner buttons one line each and putting one sentence in the panel.

  1  THE TUNNEL     he is already waiting there and says the one line
  2  THE TABLE      he leads, you follow, your schedule opens, you fill it in
  3  THE FIRE       he leads, you follow, Advisory is three things by hand
  4  THE WALL       he leads, you follow, the wall opens on what you picked
  5  THE COUNSELOR  he leads, she has the cord, the yearbook page turns
  6  THE HANDOVER   the bars come down, the corner arrives, three lines, done

The first rail walked Thor alone from station to station with a line at each, and
nobody could tell why he was standing at a fire. So beats 2 to 5 have the one
thing that makes them make sense: the principal walks AHEAD and the student
follows him, which is what a freshman orientation IS. The person in charge takes
you round, stops, turns to face you, and says the one sentence that says why you
are standing here. Then the thing happens.

AND IT IS WATCHED FROM HIS SHOULDER. `view("close")` is the character point of
view, twice the shot the room opens at: the room is never all on screen at once
and the camera rides him the whole way. It is handed back at the handover.

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
which is the game he had before. Pressing that thing puts him back on the film.
"""
from vine import (  # noqa: A004 (open is the engine's word)
    actor_release, as_a_cutscene, get, guide_to, lead_to, log, movie, objective,
    open, place, play, say, set_flag, show, view,
)

from board import on_the_wall

from lines import (
    ADVISORY_IS_MONDAY, ANSWER, COME_BACK, CORD, COUNSELOR, EXPLORE, FACE,
    FILL_IT_IN, FOLLOW, GUIDE_IS, LOOK_AT_WALL, MAP_IS, MY_YEAR_IS,
    PRINCIPAL, SCHEDULE_IS_YOURS, SOMEBODY, STAMP_IT, TALK_TO_HER, WALL,
    WALL_IS_YOURS, WELCOME, WELL_DONE, WELL_DONE_BARE, WELL_DONE_GRADED,
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

# THE FILM HAS PLAYED. Read by `island.py` so the room stops opening on it. The
# name is the old one on purpose: a run saved under rail-4 carries this string,
# and renaming it would play the whole introduction again at a student who had
# already sat through it.
RAILED = "maw:railed"

# AND THE ROOM HAS BEEN HANDED OVER: the bars are down, the three corner buttons
# have arrived and the principal has said what each one is. It is a separate flag
# from RAILED because RAILED is written one line BEFORE the bars come down, so
# that the corner is already granted on the frame they lift; a student who
# reloads between those two lines should hear the handover rather than be left
# with three buttons nobody introduced.
#
# IT REPLACES `maw:next_time`, which recorded that "Year two, next time." had
# been said. BRIEF-INTRO-FILM section 4: *"No 'Year two' wording anywhere; the
# intro does not end with a promise about next time."*
HANDED_OVER = "maw:handed_over"

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


def dress_the_wall(count):
    """The case is furniture. It is on the wall, and it stays on the wall.

    ASH, 2026-09-07, AFTER PLAYING RAIL-5: *"The 'what you earn goes up here'
    asset is still nonexistent."* It was, and nothing in the engine was wrong.
    The published Maw v6 binds `trophy_wall` to the placement `the_trophy_wall`,
    the asset row carries that name, `assets/trophy-shelf.png` is 64x80 and
    serves 200 off the platform, and `show` found all of it. This function then
    hid it, on the first frame of the room, on every load, because `count` is the
    number of stickers and badges the run is holding and NOTHING IN YEAR ONE
    AWARDS EITHER: Advisory writes a grade and a credit and no trophy, so the
    count is zero from the title screen to the handover and the case was never
    once drawn.

    THE OLD RULE WAS THE WRONG RULE and it is worth writing down rather than
    quietly deleting. It came from a real complaint: a first-year student with
    nothing earned walked in to a case that LOOKED full, because the painting has
    things on its shelves. The answer taken was to hide the case, which trades a
    case that overstates for a wall with a hole in it, and a hole is worse. A
    trophy case in a school is empty in September and is still a trophy case; a
    student is supposed to see it, want it filled, and read what is in it off the
    panel. That is the whole of "what you earn goes up here" and it needs the
    case ON THE WALL to say it.

    SO THE COUNT NO LONGER DECIDES ANYTHING HERE, and the panel is where the
    honest number lives: `open("wall")` draws one frame per thing picked this
    year, filled where it is filled and empty where it is not, and `wall_line`
    says whether there is anything up there yet. The argument is kept because
    every caller has it to hand and the logged line is worth having.

    Guarded for the same reason the walk is: `show` is a hard refusal on a room
    whose `trophy_wall` is not bound to a placement, and a bundle that predates
    the binding is exactly that. A refusal here would take the founding with it,
    and the engine has already said the sentence an author needs in the console.
    """
    try:
        yield show(WALL, True)
    except Exception as refused:
        yield log("show_refused", {"anchor": WALL, "why": str(refused), "on": count})


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

    AND THE PANEL SAYS WHAT HE IS DOING. BRIEF-MAW-RAIL-3 A: the line at the top
    of the screen is the student's own step, and for the whole of a led walk his
    step is following the man in front of him. The year's own sentence would say
    "Go to the table and pick your year" over a student who is being taken there,
    which is the game telling him to do the thing it is doing for him.

    EVERY WORD IS CAUGHT. A refusal in the middle of a beat would take the rest of
    year one with it, and the beat after this one is a screen that can still be
    filled in from a standstill.
    """
    yield objective(FOLLOW)

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
    # AND THE PANEL GOES BACK TO THE YEAR, which is what a student who has
    # stepped off the film is owed: the sentence naming the one thing still lit
    # in the room. The bars coming down would do this on their own; it is said
    # out loud because every road out of the film runs through this function.
    #
    # THE HANDOVER DOES NOT USE THIS FUNCTION for exactly that reason. It ends
    # with a sentence of its own and handing the panel back mid-handover would
    # print the year's errand over the top of it.
    yield objective(None)


# ---- the five beats ----------------------------------------------------------


def the_tunnel(walk):
    """BEAT 1. He is at the mouth, the principal is already there, one line."""
    yield objective(FOLLOW)
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
    yield objective(FILL_IT_IN)
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
    yield objective(ANSWER)
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
    yield objective(LOOK_AT_WALL)
    yield say(WALL_IS_YOURS, who=PRINCIPAL, portrait=FACE)
    # THE CASE IS ON THE WALL BEFORE THE PANEL OPENS, said again here rather
    # than trusted. The room dressed itself when the map loaded and nothing
    # since then can have taken the case down, so this is a no-op on every
    # ordinary road; it stays because it is the one line that would put the
    # room right if some later beat ever hid something.
    trophies = yield get("trophies")
    yield from dress_the_wall(on_the_wall(trophies))
    yield open("wall", wait=True)
    yield set_flag(WALL_SHOWN)


def the_counselor(year):
    """BEAT 5. He leads him to her, the cord, and the page turns.

    THE PRINCIPAL LEADS AND THE COUNSELOR SPEAKS, which is the one beat with two
    people in it and is right: he has walked the student round all morning and she
    is the person who closes a year at a school.

    The yearbook is where the page turns, in school words, and where the cord is
    draped; both of those are the engine's own screens, raised here by name. It
    comes back True only when the page really turned, because a student who opened
    the book and closed it again has not finished year one and the film must not
    say he has.

    AND NOTHING IS SAID AFTER THE PAGE TURNS. There used to be a last line here,
    "Year two, next time", and it is CUT. BRIEF-INTRO-FILM section 4: *"No 'Year
    two' wording anywhere; the intro does not end with a promise about next
    time."* What follows the page is the handover, which is about the three
    buttons the student is holding rather than about a year nobody has designed.
    """
    yield from take_him(DESK)
    yield objective(TALK_TO_HER)
    yield say(CORD, who=COUNSELOR)
    yield open("yearbook", wait=True)

    flags = yield get("flags")
    if turned(year) not in flags:
        return False

    yield log("year_one_closed", {"year": year})
    return True


def the_handover():
    """THE END OF THE FILM: the bars come down and the game becomes his.

    BRIEF-INTRO-FILM section 4, in Ash's words: *"the bars come down, the corner
    appears one plaque at a time with one line each said by the principal, 'My
    Year is what you picked. The Guide is every club and class at Bonney Lake.
    The Map is where you sail.' Then the objective bar reads 'Explore. Talk to
    anyone. Open the Guide.' and the game is his."*

    THE ORDER OF THESE LINES IS THE WHOLE BEAT. `movie(False)` is what puts the
    corner on the screen at all, because the frame HIDES it rather than dimming
    it, so the bars have to come off before the first plaque can arrive. Then a
    flag, then the line about the thing that has just swung down. This is the
    only place in the game where anybody explains a control, and it is allowed to
    be, because every control it names is visibly arriving as it is read.

    ONE MOVIE(FALSE) AND IT IS THIS ONE. `as_a_cutscene` says the same word in
    its own `finally` a beat later, and that is the net rather than the
    mechanism: this line is what MEANS the introduction is over, and it is the
    only place on the road the bars come down between Set Sail and here.

    ONE FLAG SHORT OF ONE PLAQUE AT A TIME, said plainly. `src/game/hud/
    inventory.ts` hangs both My Year and the Guide on `handbook:granted`, so
    those two arrive together on the first flag and the Map arrives on its own.
    The lines are still said in Ash's order, each with its own plaque already on
    the glass; splitting that grant is another session's file.

    AND THE PANEL IS PINNED RATHER THAN HANDED BACK. `objective(None)` gives the
    sentence to the year, and the year says the same words from here on
    (`src/game/run/objective.ts`, the terminal clause), so the two agree; this
    says it out loud anyway because a student who reloads gets the year's copy
    and a student who does not gets this one, and they must not differ.
    """
    yield set_flag(RAILED)
    yield movie(False)
    # AND THE PANEL SAYS THE ENDING BEFORE HE SPEAKS, not after. `movie(False)`
    # drops the island's word, so for the length of these three lines the panel
    # falls back to the year, and the year knows an ending is still owing: it
    # printed "The principal is waiting" over the top of the principal, who was
    # standing right there talking to him. Measured on the cold run.
    yield objective(EXPLORE)

    yield set_flag(HANDBOOK)
    yield say(MY_YEAR_IS, who=PRINCIPAL, portrait=FACE)
    yield say(GUIDE_IS, who=PRINCIPAL, portrait=FACE)

    yield set_flag(CHART)
    yield say(MAP_IS, who=PRINCIPAL, portrait=FACE)

    # the camera and the arrow come off him, the principal is his own again, and
    # the panel says the one thing there is to do. `step_off` is not used here
    # because its last line hands the panel back to the year mid-sentence.
    yield guide_to(None)
    yield from let_go()
    yield view("walk")
    yield set_flag(HANDED_OVER)
    yield log("handover", {})


def name_list(names):
    """"A", "A and B", "A, B and C". Nobody in this game says "and B, C"."""
    if not names:
        return ""
    if len(names) == 1:
        return names[0]
    return "%s and %s" % (", ".join(names[:-1]), names[-1])


def well_done(handle, picks):
    """The principal's congratulation, built out of the save and nothing else.

    Ash's shape for the ending, 2026-09-07: he congratulates the student BY NAME
    on what he ACTUALLY did. So there is no written sentence that would be true
    of everybody; there are three shapes in `lines.py` and the run decides which
    one it has earned.

    `picks` is already masked by the engine (`roster/placeholders`), so a
    programme nobody has built prints as its Example name here as well and this
    line can never congratulate a freshman on a football season that does not
    exist.
    """
    who = handle or SOMEBODY
    chose = [c["name"] for c in (picks.get("classes") or [])]
    chose += [p["name"] for p in (picks.get("seasons") or [])]

    # the Advisory row, which is the only thing in year one that carries a grade
    grade = None
    for row in picks.get("graded") or []:
        if row.get("kind") == "core":
            grade = row.get("grade")

    if chose and grade:
        return WELL_DONE_GRADED % (who, name_list(chose), grade)
    if chose:
        return WELL_DONE % (who, name_list(chose))
    return WELL_DONE_BARE % who


def year_is_done():
    """Has this year anything left owing. THE CLOSING FILM'S TRIGGER.

    ASKED OF THE SEQUENCER AND NEVER SPELLED OUT HERE. `get("phase")` is
    `src/game/run/objective.ts`'s own answer, the same one that decides which
    station in this room lights up, and "yearbook" is its word for a year with
    the sheet stamped, the core beat sat and no voyage left to sail.

    THE VERSION THAT WOULD HAVE BEEN WRONG is `get("advisory") is None`, which is
    what this file could ask before today. It is true the moment the fire is
    answered, and TODAY that is the end of the year because nothing can be sailed
    to. The first island a member builds makes it false: a stamped sheet with a
    season token on it owes a voyage, the phase says "voyage", and an ending
    written the other way would play in the middle of the student's year with the
    island he chose still out there unvisited.
    """
    phase = yield get("phase")
    return phase == "yearbook"


# ---- THE OPENING FILM --------------------------------------------------------


def opening(walk):
    """The tunnel, the schedule, Advisory, and then the handover.

    It is the same shape `objective.ts` uses to decide what the one lit thing is,
    asked of the same facts, and that is on purpose: the sequencer and the film
    cannot disagree about where a student is in the year because they are reading
    the same run.

    IT ENDS AT THE HANDOVER AND NOT AT THE YEARBOOK. The wall and the counselor
    moved out of here into `closing`, which is a film of its own with a trigger of
    its own. Today those two run back to back with nothing in between, because
    there are no islands and Advisory is therefore the last thing the year owes;
    the day the first island lands, the middle of the year appears between them
    and not one line of this function changes.
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

    yield from the_handover()


# ---- THE CLOSING FILM --------------------------------------------------------


def closing():
    """The ending: one line naming what he did, the wall, the cord, the page.

    Ash's shape, 2026-09-07: *"the principal meets him and congratulates him BY
    NAME on what he actually did (the picks and grades from the save, one line),
    the wall shows it, the counselor drapes the cord, the yearbook card, bars
    down, the end."*

    HE IS PLACED FIRST, so the film opens on a man already standing in front of
    the student rather than on a man crossing a room to reach him. That matters
    on both roads in: straight off the end of the opening, where he is standing
    at the fire beside him, and a student who sailed home with the year finished,
    where he is back at his own desk across the hall.

    NOTHING PROMISES A YEAR TWO. The page turning is the ending.
    """
    yield view("close")
    yield from waiting_at_the_door()

    # THE PANEL SAYS WHAT HE IS DOING, and for the length of the ending that is
    # following the man who came to find him. FOLLOW rather than a sentence of
    # its own, because the very next thing after the line is being led to the
    # wall, and each beat sets its own step after that.
    yield objective(FOLLOW)

    handle = yield get("handle")
    picks = yield get("picks")
    yield say(well_done(handle, picks), who=PRINCIPAL, portrait=FACE)

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

    # AND THE GAME IS HANDED BACK. The corner is already his, so what is left is
    # the camera, the arrow and the sentence. `objective.ts` says the same words
    # from here on, so nothing changes under him when the island's word is
    # dropped as the bars come down one line later.
    yield guide_to(None)
    yield from let_go()
    yield view("walk")
    # THE BARS COME DOWN HERE AND NOT IN THE `finally`, the same way the
    # handover does it, and for the same reason: `movie(False)` DROPS the
    # island's word off the panel, so saying the last sentence first and then
    # letting the wrapper lower them wiped it and left the room to say it again
    # a frame later. This order means the sentence a student ends on is written
    # once and never blinks.
    yield movie(False)
    yield objective(EXPLORE)
    yield log("closing_done", {"year": year})


# ---- the two of them, each inside its own frame ------------------------------


def rail(walk=True):
    """THE INTRODUCTION, run inside the bars, which come down whatever happens.

    `as_a_cutscene` is `movie(True)`, the scene, and `movie(False)` in a `finally`.
    It is the shape a member should copy for anything a student WATCHES, and it
    exists because the gap between those two lines is the one place in this API
    where forgetting leaves somebody behind two black bars with no controls. Here
    the scene is minutes long with four screens inside it, and any word in it can
    refuse; the bars still come down.

    IT IS THE SECOND HALF OF ONE FILM AND NOT A FILM OF ITS OWN. The bars went up
    when the student pressed Set Sail on the beach; the hub's island sailed him
    in and walked him up the quay inside them, and the engine carried the frame
    through the tunnel door with him rather than tearing it down with the map. So
    `movie(True)` on the first line here is already true, and the first time it
    goes false is `the_handover`.
    """
    yield from as_a_cutscene(opening(walk))


def ending():
    """THE CLOSING FILM, inside its own frame.

    Its trigger is `year_is_done()` and both callers are in `island.py`: the room
    opening with the year finished, which is the road every student takes, and
    the principal being pressed by one who walked out of the middle of it.
    """
    yield from as_a_cutscene(closing())
