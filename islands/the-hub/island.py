"""THE HUB: the crossing, the dock and the walk up, as an island.

BRIEF-ARRIVAL, Ash 2026-09-06, and then again after he played the first build.
The whole arrival is one watched piece, in his second order:

  1  the crossing is a CUTSCENE and it is CLOSE. The camera rides with the ship,
     at the scale a ship is a ship, behind two black bars. No HUD, no plaques,
     no tiller. He watches her sail in.
  2  she reaches the dock. The camera pulls OUT to the whole island, and the
     arrival card plays there. The bars do not come down for it: they are up
     for the whole arrival, from the first frame to the tunnel.
  3  THEN Thor hops out.
  4  THEN the camera comes in CLOSE on him, in ONE move and not two, and he
     AUTO-WALKS with the corner away: the dock, the stone harbor, the first
     stairs, the second stairs, the Panther's Maw door, with drawn arrows on the
     ground the whole way. He is being shown the road, not walking it.
  5  at the door a large drawn pointer hangs above the tunnel, and E goes in.

THE HOP-OUT USED TO BE WELDED TO THE ARRIVAL and that is why the order above
could not be written before. Berthing put the body on the dock in the same call,
so there was nowhere to put the pull-out or the card. `ashore()` is the second
half, said here at the moment this island means it.

THIS IS THE VINE'S OWN CONTENT and it runs unscoped, like the Maw: the flag it
writes is a bare name. A member's island is scoped and should be. Read
`islands/panther-maw/island.py` for the whole argument; read this one for what
an arrival looks like when the engine is doing the directing and the island is
doing the deciding.

WHY THERE IS ONE `walk_to` AND NOT FOUR. Ash's list names four stages, and the
temptation is four calls. Four calls is a body that stops dead at every corner,
turns, and starts again, because each one is its own arrival. `walk_to` searches
the level mask with the same law the body walks by, so it finds the dock, the
harbor and both stairways by itself and walks them as one movement. Measured on
hub v15: 557,507 to the door in about seven seconds, up both flights, no stops.
The four stages are in the painting, not in this file.

EVERY PLACE HERE IS A NAME ON THE MAP. The sail line `the_hub_approach`, which
the engine reads off the ocean page when the painting does not carry it, and the
door `panthers_maw`. The three dock posts are named but not yet placed, so those
handlers simply never fire and the engine says so by name when the island loads.
"""
from grape import on_start, on_talk
from vine import (
    ashore, get, guide_to, log, movie, route, say, set_flag, view, wait, walk_to,
)

from lines import DOCK_ONE, DOCK_THREE, DOCK_TWO, HELLO, KEEP_GOING, WAITING

# the line the ship follows in, drawn on the hub in MAPVIS with kind `sail`
SAIL_LINE = "the_hub_approach"

# the tunnel into the mountain, and what the third person points at
DOOR = "panthers_maw"

# this run has already been sailed in. Bare, because this island is unscoped;
# see the note at the top. Without it the hub would put him back in the boat
# every time he walked out of the mountain.
CROSSED = "hub:crossed"

# how long the wide shot holds AFTER he has stepped off, so that a student sees
# a person appear on the dock rather than a cut. Short: the shot has already had
# the card's length before this.
ISLAND_HOLD_MS = 1400

# and how long the engine's own arrival card owns the bottom of the screen. It
# dwells for 3.2 seconds and takes another 0.7 to leave; this waits out both
# rather than starting the walk underneath it.
CARD_MS = 3900


@on_start
def putting_in():
    """The crossing and the walk up, the first time the hub loads and never again.

    `route(..., who="ship")` is how a voyage starts. On a sea arrival the hull
    is already on the water where the beach left it, the ship runs the line, and
    the ENGINE ties her up at the berth nearest the line's end and hands the
    body back on the dock. Nothing here says the island's name; the card does,
    where he lands.

    THE BARS GO UP FIRST AND COME DOWN BEFORE THE WALK. The crossing is watched
    and the walk is not: the arrow marks, the light on the door and the card are
    all things a student is meant to look at and act on, and none of them draw
    inside the movie frame. So the frame ends where the watching ends.

    THE REFUSAL IS CAUGHT, AND THAT IS UNUSUAL. Almost every word in an island
    should be allowed to raise: a refusal on your own line is how you find out a
    name is wrong. The crossing is caught because it has a fallback the engine
    already performs, and because a refusal there must not take the walk up with
    it: losing the boat is a beat, losing the way to the school is the game. It
    is still LOGGED with the engine's own sentence, because a silent refusal is
    a name nobody fixes.
    """
    flags = yield get("flags")
    if CROSSED in flags:
        return

    # ---- 1: the crossing, close, behind the bars -------------------------
    yield movie(True)
    yield view("ship")
    try:
        yield route(SAIL_LINE, who="ship")
        yield log("crossing_sailed", {"path": SAIL_LINE})
    except Exception as refused:
        yield log("route_refused", {"path": SAIL_LINE, "why": str(refused)})

    # ---- 2: she is at the dock ------------------------------------------
    #
    # THE BARS STAY UP FOR ALL OF IT, ruled by Ash after watching: "The black
    # rectangle should be there throughout the entire thing." They used to come
    # down here and go back up for the walk, and the two seams in the middle
    # were the glitches he saw. The card draws inside the frame now, which is
    # where a title card belongs.
    yield view("island")
    yield wait(CARD_MS)

    # and the one line anybody has written about this moment. It belongs to
    # `dock_three`, a post MAPVIS has not placed, so nobody on this map can say
    # it and it has never been heard. Said here with no speaker until the post
    # exists, the way the card speaks without one.
    yield say(WAITING)

    # ---- 3: and NOW he hops out ------------------------------------------
    #
    # NOTHING ELSE MOVES THE CAMERA HERE. Stepping ashore has always pulled to
    # the walking shot, so the island shot travelled to it and then this island
    # travelled again to the close one: full island, half island, then him.
    # `ashore()` leaves the shot alone and the next line is the only move.
    yield ashore()
    yield wait(ISLAND_HOLD_MS)

    # ---- 4 and 5: in on him, and up the hill ------------------------------
    #
    # He is not playing this stretch, he is being shown the way, and the marks
    # on the ground are what he is being shown.
    yield view("close")
    # the arrow marks on the ground and the big pointer over the tunnel are one
    # word: the engine draws the route he is about to walk and hangs the pointer
    # over the thing at the end of it
    yield guide_to(DOOR)
    yield walk_to(DOOR)
    # NO `view("walk")` AND NO `movie(False)` HERE, AND BOTH ARE A RULING RATHER
    # THAN AN OVERSIGHT. Ash, 2026-09-06, watching this exact moment: "after the
    # auto walk ends and thor has 'Go to panther's maw' the black boxes
    # disappear, and it zoomed out, and the three buttons are back. none of that
    # should happen." He arrives at the tunnel still inside the frame, at the
    # close shot, with the corner still away.
    #
    # HE CAN STILL PRESS THE DOOR, because the engine hands the controls back
    # when this handler returns and leaves the frame standing: the bars are the
    # picture and the lock is a lease on it. The door takes the frame with it.
    yield log("walked_to_the_maw")

    # written whether she sailed or not: the crossing happens once, at arrival,
    # or it does not happen. A second try on the next load would put a student
    # who had just walked out of the mountain back onto the water.
    yield set_flag(CROSSED)


@on_talk(DOCK_ONE)
def the_first_person():
    yield say(HELLO, who=DOCK_ONE)


@on_talk(DOCK_TWO)
def the_second_person():
    yield say(KEEP_GOING, who=DOCK_TWO)


@on_talk(DOCK_THREE)
def the_third_person():
    """The line the brief wrote, and then the door lights.

    `guide_to` raises the arrow, the marks along the route and the pointer over
    the door. The year's own objective is already pointing there from another
    map ("go into the mountain and find the principal"), so this is the same
    target said at the moment he is told about it, and the door itself takes the
    arrow down when he goes through: a door tears the scene down and nothing
    survives it.
    """
    yield say(WAITING, who=DOCK_THREE)
    yield guide_to(DOOR)
