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
    HANDED_OVER, RAILED, dress_the_wall, ending, he_steps_in_front, let_go, rail,
    turned, year_is_done,
)
from lines import (
    ASK, BACK_AGAIN, BANKED, CIRCLE, COUNSELOR, HEARTH, LEFT,
    NOOK, NOT_NOW, NOTHING_YET, OUTFITTER, PRINCIPAL, SHEET,
    SHOW_ME, TABLE, THOR, FACE,
)

# ONE FILM PER SITTING, AND THIS IS WHAT COUNTS THE SITTING.
#
# Ash, 2026-09-07, after playing rail-5: the introduction handed the game over
# and the ending started three seconds later, so the bars came down, three lines
# were said, the bars went straight back up and the principal walked back to the
# door to meet a student he had been standing beside all morning. Two films with
# no game in between is not two films.
#
# So the closing never plays in the same sitting as the opening. It plays when
# the student walks BACK IN through the tunnel with the year done, which is the
# shape it will always have once an island exists and he has sailed home. Today
# he only has to walk out to the quay and turn round, and that is the point: the
# handover means the room is his, and the first thing he does with it is leave.
#
# A MODULE VARIABLE IS THE RIGHT SIZE FOR THIS, and it is worth saying why rather
# than reaching for a flag. A flag lives in the save and outlives the tab; this
# must not, because "did the opening play a minute ago" is a fact about THIS
# visit to THIS room. The engine gives an island a fresh MicroPython worker on
# every map load (`src/vine/py/runGrape.ts` opens one per scene), so this list is
# empty again the moment he comes back in, which is exactly the lifetime wanted.
# Do not write a `set_flag` for something this short.
_OPENED_HERE = []


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

    # AND THE PRINCIPAL IS NOT STANDING INSIDE WHOEVER JUST WALKED IN.
    #
    # Ash moved his post to the tunnel mouth in MAPVIS on 2026-09-08, six pixels
    # from the spot the door puts a student on, so on every load that does not
    # start a film the two of them were drawn as one blob and the plaque over it
    # said "Talk to Principal Panther". Measured in a browser on Maw v7.
    #
    # His own note the same day is the fix and not a workaround: the principal
    # "pops up in front of thor at any time, he isnt bound to the entrance of the
    # maw". So the room steps him in front rather than leaving him underfoot, and
    # the films move him from there.
    #
    # AND THEN HE IS HANDED STRAIGHT BACK, which is the difference between
    # dressing a room and holding a body. `place` puts a placement under this
    # island's control and the engine re-asserts its position every frame until
    # somebody lets go, so a room that placed him and kept him made the principal
    # undrivable by anything else for the whole visit. Caught by
    # `scripts/arrival-proof.mjs` on the live deploy: its "a driven body really
    # crosses the room" check moved him fourteen pixels instead of a hundred,
    # because this line had him. He has no wandering of his own on this map, so
    # letting go leaves him exactly where he was put.
    yield from he_steps_in_front()
    yield from let_go()

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
        _OPENED_HERE.append(True)
        yield from rail(walk=True)
        # AND THE SITTING IS SPENT. The opening ends at the handover and that is
        # the end of what a student watches today: the bars come down once, the
        # corner arrives, the panel says what there is to do, and then the room
        # is quiet. Nothing below runs on this load.
        flags = yield get("flags")

    # ---- THE CLOSING FILM ---------------------------------------------------
    #
    # THE TRIGGER IS THE SEQUENCER'S OWN ANSWER, asked at the one moment it is
    # cheap to ask: the room loading. `year_is_done` reads `get("phase")`, so
    # this fires when the whole YEAR is finished rather than when Advisory is;
    # its docstring has why that difference matters.
    #
    # AND IT IS ASKED ON A LOAD THAT DID NOT JUST PLAY THE OPENING. Ash's rule,
    # 2026-09-07: the ending plays on ENTERING the Maw with the year done, and
    # never in the same sitting as the introduction. Both halves matter. Without
    # the first the ending would need a press to start; without the second the
    # handover is undone by the next line of the same handler.
    #
    # TWO ROADS REACH IT now. A student who walked out to the quay and came back
    # in through the tunnel, which is every student today. And one who sailed
    # home with the year done, which is every student the day an island exists.
    # A reload is the same road as the first: the room loads, this handler runs,
    # and no opening played on that load.
    done = yield from year_is_done()
    if done and not _OPENED_HERE:
        yield from ending()
        # AND NOTHING AFTER IT. The ending walks him out of the mountain, so by
        # the time it comes back this map is being torn down and this worker
        # with it. The one road where it returns having done nothing is a
        # student who closed the yearbook without turning the page, and that
        # road went through `step_off`, which has already handed the panel back
        # to the year. Either way the line below is not this handler's to say.
        return

    # ---- AND THE PANEL IS THE YEAR'S, NOT THIS ROOM'S -----------------------
    #
    # Nothing is pinned here any more. The room used to put "Explore. Talk to
    # anyone. Open the Guide." back on the bar on every load once the handover
    # had happened, and an island's word outranks the year's, so the sentence
    # the game START a year with sat on the glass for the rest of the session.
    #
    # Ash, 2026-09-08: the middle of year one is the two classes, and the bar is
    # what names them. `src/game/run/objective.ts` says the right thing at every
    # step of the year on its own, and the one thing this room can do to help is
    # stop talking over it.


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

    # ---- THE ENDING, FOR A STUDENT WHO IS ALREADY STANDING IN THE ROOM -----
    #
    # ASH, 2026-09-08 item 6: *"Walking into the Maw with the year done starts
    # the ending film."* That is the OTHER road (`walking_in`), and it is the one
    # that must never fire on the load the opening played on, because the two
    # films would run back to back. This road is the press, and it is fenced by
    # the HANDOVER instead of by the latch.
    #
    # WHY THE FENCE MOVED, measured on the live deploy 2026-09-08. The year now
    # closes at the CHART TABLE: a student presses Go on his last pick standing
    # ten feet from the man, the bar lights the desk and says "Find the
    # principal", and with the latch on this road pressing him got a hello. He is
    # then told to go back to a room he is standing in, and nothing he can do in
    # that room ends the year. The cold gate sat there for four minutes.
    #
    # AND IT CANNOT RUN THE TWO FILMS TOGETHER, which is what Ash actually ruled
    # out. `HANDED_OVER` is written on the last line of the opening, and between
    # it and this the student has to have finished every pick on his sheet. The
    # opening does not finish a pick, so the year cannot be done when it ends.
    done = yield from year_is_done()
    if done and HANDED_OVER in flags:
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

    ON THE WAY OUT SHE IS THE ENDING'S, NOT HER OWN. When the year has nothing
    left owing she starts the closing film rather than opening the yearbook
    herself: she is IN that film, the cord and the page belong to it, and the
    note at the press below has what pressing her used to cost.
    """
    year = yield get("year")
    flags = yield get("flags")
    # ---- SHE NEVER STARTS THE ENDING ----------------------------------------
    #
    # ASH, 2026-09-08: *"pressing the principal starts the closing film (the
    # counselor never starts it)."*
    #
    # She used to open the yearbook herself, which deleted the ending outright,
    # and then she started the film, which was better and still wrong: the closing
    # is the PRINCIPAL coming to find you, and a student who wanders over to her
    # first should not trigger the man walking up behind him. Two doors into one
    # film is one door too many, and she is in the film anyway.
    #
    # So she says what she always says. The year being over is the objective bar's
    # job to announce and the principal's to act on.
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
        # THE CORDS PAGE, NOT THE ISLANDS ONE (Ash, 2026-09-09). `open("handbook")`
        # always lands on Islands, so the one beat in this game whose whole subject
        # is the cords opened the page about islands.
        yield open("cords")


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
