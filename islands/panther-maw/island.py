"""THE PANTHER'S MAW: the home base, as an island.

This is the room the game keeps coming back to. The year gets picked here, the
required Advisory is sat here, the cords get read out here, and everything a
student brings back from the water ends up on a wall in here.

READ THIS ONE TO UNDERSTAND THE MACHINE. It is not the file you copy. The one you
copy is the ATC island, which is a member's island about one real thing at the
school; this is the vine's own content, so it reaches things a member's island
does not and should not, and every place it does is marked. What is worth taking
from it is the SHAPE: handlers the engine calls, words that only happen when you
yield them, content in one file and control flow in another, and a scene long
enough to deserve a file of its own.

WHAT A HANDLER IS. Nothing in this file calls the seven functions below. Each one
is handed to the engine by its decorator, and the engine decides when it runs: a
player walks up to a post in the room, presses E, and the engine looks up whoever
claimed that anchor's name. That inversion is the whole difference between an
island and a script. A script runs top to bottom and is over; an island can be
walked away from, come back to on the third visit, and answer differently.

WHICH BEATS OF YEAR ONE LIVE HERE. BRIEF-YEAR-ONE's beat 4, the principal, is
the room's opening the first time in (`founding.py`). Beat 5, Advisory, is the
fire. Beat 8, home, is the counselor opening the yearbook when the year can
close and the wall showing what was earned.

WHICH ANCHORS THIS ROOM ACTUALLY HAS. Eleven, and only six of them can be
pressed. The other five are not oversights and no handler here claims them:

  arrive_maw    a spawn. It is where the tunnel puts you, not something you press.
                It IS where the principal walks to, because it is the one name
                that means "where you are standing when you have just come in".
  the_hall      a region. Regions are logged when you walk into them and there is
                no handler key for one. A trigger fires a handler; a region does
                not, and this room carries no triggers. If the room should ever
                notice you walking into the middle of it, that is a change in
                MAPVIS from `region` to `trigger`, and no line of python can
                substitute for it.
  maw_entrance  a door. A door is a door BEFORE anything else is asked: the
  east_tunnel   engine takes it and changes the map, and `@on_talk` on any of
  west_tunnel   these three would never run. `maw_entrance` already carries the
                anchor to arrive at in the hub. The two galleries point at rooms
                nobody has painted, and the engine says "the way is barred" on
                the plaque, in the world's own words. All three of these work,
                today, with nothing in this file about them.
"""
from grape import on_start, on_talk
from vine import (
    choose, get, log, objective, open, play, say,
)

from board import counsel, on_the_wall, wall_line
from founding import (
    HANDED_OVER, RAILED, dress_the_wall, ending, rail, turned, year_is_done,
)
from lines import (
    ASK, BACK_AGAIN, BANKED, CIRCLE, COUNSELOR, EXPLORE, HEARTH, LEFT,
    NOOK, NOT_NOW, NOTHING_YET, OUTFITTER, PRINCIPAL, SHEET,
    SHOW_ME, TABLE, THOR, FACE, YEAR_DONE,
)


@on_start
def walking_in():
    """The engine calls this every time the room loads, before the player moves.

    EVERY TIME, which is the thing to design around, and it cuts both ways. The
    room gets crossed forty times in an hour, so a room that greets you on the
    fortieth crossing is a room you learn to walk past, and everything that
    speaks sits behind a flag. But anything about how the room LOOKS has to be
    redone on every one of those forty crossings, because a map load draws the
    painting fresh and knows nothing about what happened on the last one. Those
    two live on opposite sides of the early return below, and that is the whole
    shape of this handler.

    THE FILM RUNS HERE, and it is the second half of one that started on the
    beach. `founding.py` has the whole of it. It is one handler on purpose,
    because an open handler is what makes the rest of the room unpressable while
    a student is being walked through it, and it asks the run which beats are
    still owed rather than remembering, so a reload picks up where he was.

    The way he is facing when he gets here is not set in this file either. The
    spawn anchor carries a heading, MAPVIS is where somebody chose it, and the
    engine turns him before this function runs.
    """
    # ---- what the room looks like: every load, before the early return -----
    trophies = yield get("trophies")
    yield from dress_the_wall(on_the_wall(trophies))

    # ---- the film, walked --------------------------------------------------
    #
    # YEAR ONE AND NOT EVERY YEAR. The film is about the first thirty minutes: a
    # student who has met the room once knows where the table and the fire are,
    # and being walked to them again in year two would be the game taking the
    # controls off somebody who has already shown they do not need it. Years two
    # to four are the room with one thing lit, which is the game the objective
    # sequencer has always run.
    flags = yield get("flags")
    year = yield get("year")
    if RAILED not in flags and year == 1:
        yield from rail(walk=True)
        # AND IT FALLS THROUGH RATHER THAN RETURNING, which is the whole of the
        # two-film shape. The opening ends at the handover, and today the
        # closing's own trigger is already true on that frame, because there are
        # no islands and Advisory is therefore the last thing the year owes. So
        # the two play back to back with no reload in between. The day one
        # island exists the trigger below is false here and the middle of the
        # year happens instead, with no edit to this file.
        flags = yield get("flags")

    # ---- THE CLOSING FILM ---------------------------------------------------
    #
    # THE TRIGGER IS THE SEQUENCER'S OWN ANSWER, asked at the one moment it is
    # cheap to ask: the room loading. `year_is_done` reads `get("phase")`, so
    # this fires when the whole YEAR is finished rather than when Advisory is;
    # its docstring has why that difference matters.
    #
    # THREE ROADS REACH IT and they are all this line. The opening falling
    # through above. A student who sailed home with the year done, because the
    # room loads when he walks in through the tunnel. And a reload, because this
    # handler runs on every load and the phase is read fresh each time.
    done = yield from year_is_done()
    if done:
        yield from ending()
        flags = yield get("flags")

    # ---- and after it, the room is his, and the panel says so ---------------
    #
    # BRIEF-INTRO-FILM section 4: once the film has handed over, the panel reads
    # "Explore. Talk to anyone. Open the Guide." The handover says it too, and
    # this is the OTHER road to the same sentence: a student who walked out to
    # the hub and came back, or who reloaded the tab, arrives with the island's
    # word forgotten (it is dropped whenever the bars come down) and this puts it
    # back on the first frame of the room.
    #
    # `src/game/run/objective.ts` answers the same words when nobody says
    # anything at all, so the panel cannot flicker between two endings; this line
    # is what makes the sentence the ISLAND'S, which is where a member would put
    # their own.
    if HANDED_OVER in flags:
        yield objective(EXPLORE)


@on_talk("principal_desk")
def the_principal():
    """Whichever film the run still owes; then one line.

    A student who closed the pick cards or left Advisory half answered has the
    year's own light still on this desk to come back to, and so does one who
    closed the yearbook without turning the page. Pressing him puts the student
    back on the film he stepped off, which is the whole reason a film that lets
    go leaves the room with one thing lit.

    The walk is False on the opening because he is standing in front of the
    principal already, and walking him to the tunnel to say hello would be
    walking him away from the man he just pressed.
    """
    flags = yield get("flags")
    year = yield get("year")
    if RAILED not in flags and year == 1:
        yield from rail(walk=False)
        return

    # the ending, for a student who closed the yearbook without turning the page
    # and walked away. The year's own light is on this desk while it is owed.
    done = yield from year_is_done()
    if done:
        yield from ending()
        return

    yield say(BACK_AGAIN, who=PRINCIPAL, portrait=FACE)


@on_talk("chart_table")
def the_chart_table():
    """The year sheet. A panel, and the pick is the mechanic.

    ONE OF THE THINGS IN THIS ROOM THAT IS A PANEL RATHER THAN A SCENE. The
    first year is picked off big drawn cards, and every year after is a paper
    sheet; the engine decides which, and this opens whichever it is.
    """
    # NO `log("planner_opened")` HERE, and the TypeScript station this replaces
    # had one. `Planner.tsx` fires that same event itself when the panel mounts,
    # so the station's copy wrote a second row for one press and every count of
    # how often a student opened the year sheet was doubled. The press is already
    # on the record: the engine logs `station_used` with this anchor's name.
    yield say(SHEET, who=TABLE)
    yield open("planner")


@on_talk("hearth")
def the_fire():
    """The required Advisory beat for this year, or a banked fire.

    WHICH BEAT, ASKED RATHER THAN SPELLED. `get("advisory")` answers with the id
    of the beat this year still owes, or None when the year has no content or
    the student already sat it. Writing "core:y%d" here instead would be a typed
    constant that goes wrong the first time the beats are renumbered, and
    yielding `play` without asking would run a beat that is already on the
    transcript and grade the same year twice.
    """
    beat = yield get("advisory")
    if beat is None:
        yield say(BANKED, who=HEARTH)
        return

    yield say(CIRCLE, who=HEARTH)
    # BOTH ARMS OF THE STUDY RUN THROUGH THIS ONE WORD, and the arm is not this
    # island's to choose. Left alone, `play` renders whichever arm the student
    # was assigned when they joined: the game arm gets Principal Panther asking
    # the questions, the plain arm gets the same questions as a form with nobody
    # saying them. Same items, same order, same score. Passing as_plain=True here
    # would force the plain rendering on everybody, which is a real thing to want
    # for a moment that should read identically, and is not this one.
    score = yield play(beat)

    # None is the player closing the panel, which is not a zero. A zero is a
    # student who answered and got everything wrong, and the two must never be
    # written down as the same thing.
    if score is None:
        yield say(LEFT, who=HEARTH)
        return

    # NO `award` HERE, DELIBERATELY, and this is the one place this island breaks
    # the rule your own island must keep. A member's island scores its own
    # content and has to write the row itself. A core beat is the ENGINE'S
    # content: the runner already wrote the grade, the credit, the tags and the
    # facts before this line ran, and awarding again would put a second row for
    # the same year on the transcript and move the GPA twice.
    #
    # AND NOTHING IS SAID AFTERWARDS. The grade pops over the map naming what was
    # finished and what it was worth, which is the result (BRIEF-MAW-RAIL). A
    # line here as well was the same fact said twice, in the slower of the two
    # places.
    yield log("advisory_sat", {"beat": beat, "grade": score})


@on_talk("counselor")
def the_counselor():
    """The cords, said out loud by somebody, off the live table. And beat 8.

    A person rather than a board, because §8.4's whole ask was to surface the
    hidden earnable things, and a list on a wall is the thing a student already
    scrolls past. What she says changes with the run: on the way in during year
    one she has nothing, and on the way out she has the first cord that moved.

    ON THE WAY OUT SHE IS HOME. When Advisory is done and this year's page has
    not turned, she opens the yearbook. The yearbook is where the page turns,
    in school words, and where she drapes the cord he is closest to; both of
    those are the engine's own screens, raised here by name. A yearbook opened
    before the sheet is stamped says the year is still open, honestly, and does
    not turn.
    """
    year = yield get("year")
    flags = yield get("flags")
    advisory = yield get("advisory")
    if advisory is None and turned(year) not in flags:
        yield say(YEAR_DONE, who=COUNSELOR)
        yield open("yearbook")
        return

    board = yield get("cord_board")
    lines = counsel(board)

    if not lines:
        yield say(NOTHING_YET, who=COUNSELOR)
    else:
        for line in lines:
            yield say(line, who=COUNSELOR)

    pick = yield choose([SHOW_ME, NOT_NOW], prompt=ASK)
    # -1 is not an index. It is nobody having answered, because the player left
    # while the buttons were up, and it must not read as the first button.
    if pick == 0:
        yield open("handbook")


@on_talk("outfitter")
def the_outfitter():
    """The wardrobe. Revisitable, and nothing in it is bought."""
    yield say(NOOK, who=OUTFITTER)
    yield open("wardrobe")


@on_talk("trophy_wall")
def the_wall():
    """What the year put on a shelf, counted rather than promised, then shown.

    The wall itself is the readout, and everything on it got there because of
    something the student did somewhere else. A thing you walk up to that
    changed because of a voyage you took two years ago is worth more than a
    list of the same information.

    AND THEN THE PANEL. The engine's wall has a frame for every thing picked
    this year, empty and saying what would fill it until it is filled, which is
    the outline that makes a student want the year (BRIEF-YEAR-ONE beat 4) and
    the thing that shows what he earned at the end of it (beat 8). `open("wall")`
    is that panel, raised by name.

    WHAT `show` CAN AND CANNOT DO HERE, said plainly because it is the honest
    limit. The engine can hide or reveal any placement an anchor is bound to, by
    the anchor's name. This wall is bound to ONE placement, a drawn shelf, so
    what `show` can express is a shelf that is there or a shelf that is not.
    Filling it trophy by trophy on the painting needs one placement per trophy,
    drawn and bound in MAPVIS; until those exist the panel carries the frames.

    AND THE PICTURE IS NOT SET HERE. `walking_in` did it when the room loaded, so
    the shelf was already telling the truth before the player walked over. It
    is synced again anyway, because a sticker can be earned and brought back
    without the room reloading in between.
    """
    trophies = yield get("trophies")
    count = on_the_wall(trophies)

    # Thor says it either way: a wall is furniture, and the line carries no
    # count, so nothing he says can disagree with the panel's own numbers
    yield say(wall_line(count), who=THOR)

    yield from dress_the_wall(count)
    yield open("wall")
