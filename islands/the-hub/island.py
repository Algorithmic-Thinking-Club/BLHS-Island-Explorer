"""THE HUB: the crossing, the dock and the walk up, as an island.

BRIEF-ARRIVAL, Ash 2026-09-06, after playing it. The whole arrival is one
watched piece, in his order:

  1  the crossing is a CUTSCENE. The ship's own point of view, two black bars,
     no HUD, no plaques, no tiller. He watches.
  2  the ship stops at the dock and Thor hops out.
  3  the moment he is on the dock the camera pulls out to the whole island, for
     a moment. Then the arrival card.
  4  then it comes back in and Thor AUTO-WALKS: the dock, the stone harbor, the
     first stairs, the second stairs, the Panther's Maw door. Clean arrow marks
     on the ground follow the whole route.
  5  at the door a large pointer hangs above the tunnel, and E goes in.

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
    get, guide_to, log, movie, route, say, set_flag, view, wait, walk_to,
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

# how long the whole island stays on screen before anybody is asked to do
# anything. Long enough to read as a held shot and short enough that a fourteen
# year old does not think the game has stopped.
ISLAND_HOLD_MS = 2400

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

    # ---- 1 and 2: the crossing, as a movie -------------------------------
    yield movie(True)
    try:
        yield route(SAIL_LINE, who="ship")
        yield log("crossing_sailed", {"path": SAIL_LINE})
    except Exception as refused:
        yield log("route_refused", {"path": SAIL_LINE, "why": str(refused)})

    # ---- 3: the whole island, held, still inside the frame ---------------
    #
    # The pull-out is the last shot of the crossing rather than the first shot
    # of the walk, which is why it happens before the bars come down: he has
    # just arrived somewhere and the picture says where. The card cannot draw
    # under the bars, so the engine holds it until they lift.
    yield view("island")
    yield wait(ISLAND_HOLD_MS)
    yield movie(False)

    # the arrival card, which the engine owes from the moment he stepped ashore
    # and pays the instant the frame opens. Nothing here raises it; this waits
    # for it, so the walk does not start underneath it.
    yield wait(CARD_MS)

    # ---- 4 and 5: back in, and up the hill -------------------------------
    yield view("walk")
    # the arrow marks on the ground and the big pointer over the tunnel are one
    # word: the engine draws the route he is about to walk and hangs the pointer
    # over the thing at the end of it
    yield guide_to(DOOR)
    yield walk_to(DOOR)
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
