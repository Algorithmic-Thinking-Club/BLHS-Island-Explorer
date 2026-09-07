"""THE HUB: the crossing, the dock and the walk up, as an island.

BRIEF-ARRIVAL, Ash 2026-09-06, and then again after each build he has played.
The whole arrival is one watched piece, in his third order, 2026-09-07:

  1  the crossing is a CUTSCENE and it is CLOSE. The camera rides with the ship,
     at the scale a ship is a ship, behind two black bars. No HUD, no plaques,
     no tiller. He watches her sail in.
  2  she ties up at the dock, and THEN Thor hops out. His words: the card plays
     "after the ship has landed", and landing is a person standing on the boards
     rather than a boat touching them.
  3  THEN the camera pulls OUT to the whole island, and the THE HUB card plays
     over that shot. The bars do not come down for it: they are up for the whole
     arrival, from the first frame to the tunnel.
  4  THEN, and not before, any line anybody says on the hub. The card is what
     names the place, and a line that beat it to the screen was talking about
     somewhere the student had not been told the name of yet.
  5  THEN the camera comes in CLOSE on him, in ONE move and not two, and he
     AUTO-WALKS with the corner away: the dock, the stone harbor, the first
     stairs, the second stairs, the Panther's Maw door, with drawn arrows on the
     ground the whole way. He is being shown the road, not walking it.
  6  at the door a large drawn pointer hangs above the tunnel, and E goes in.

THE HOP-OUT USED TO BE WELDED TO THE ARRIVAL and that is why the order above
could not be written before. Berthing put the body on the dock in the same call,
so there was nowhere to put the pull-out or the card. `ashore()` is the second
half, said here at the moment this island means it.

WHAT MOVED ON 2026-09-07, AND IT IS TWO LINES. `ashore()` came UP, above the
pull-out, because the engine pays the arrival card at the hop-out and Ash wants
the card after the landing. And `set_flag(CROSSED)` went DOWN, all the way to
the tunnel, because a student who reloads halfway through the arrival has not
had the arrival: see the note at the flag itself.

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

# this run has already been WALKED in, which is not the same as sailed in. Bare,
# because this island is unscoped; see the note at the top. Without it the hub
# would put him back in the boat every time he walked out of the mountain.
CROSSED = "hub:crossed"

# how long the ship lies at the dock before he steps off her, so that tying up
# and hopping out read as two things and not one movement.
TIED_UP_HOLD_MS = 900

# and how long the engine's own arrival card owns the bottom of the screen. It
# dwells for 3.2 seconds and takes another 0.7 to leave; this waits out both
# rather than starting the walk underneath it.
CARD_MS = 3900


@on_start
def putting_in():
    """The crossing and the walk up, once per run, until he stands at the tunnel.

    `route(..., who="ship")` is how a voyage starts. On a sea arrival the hull
    is already on the water where the beach left it, the ship runs the line, and
    the ENGINE ties her up at the berth nearest the line's end. Nothing here
    says the island's name; the card does, on the line that lands him.

    THE BARS GO UP FIRST AND DO NOT COME DOWN. The whole stretch from the water
    to the tunnel is watched, so the frame is one frame and not three, and the
    card, the line and the ground marks all draw inside it. The engine hands the
    controls back when this handler returns and leaves the frame standing.

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

    # ---- 2: she is tied up, and he steps off her -------------------------
    #
    # A BEAT FIRST, so that a student sees her lying at the dock. Tying up and
    # hopping out in the same frame is one movement and reads as a teleport.
    yield wait(TIED_UP_HOLD_MS)

    # AND THIS IS THE LANDING, which is what Ash's order hangs on. `ashore()`
    # puts him on the boards. The card does NOT play on this line: the engine
    # holds it for the wide shot below, because a card that opens here opens over
    # a picture of the dock. It used to play a line EARLIER still, at the tie-up,
    # naming the island over a boy who was still sitting in the boat.
    #
    # NOTHING ELSE MOVES THE CAMERA HERE. Stepping ashore has always pulled to
    # the walking shot, so the island shot travelled to it and then this island
    # travelled again to the close one: full island, half island, then him.
    # `ashore()` leaves the shot alone and the next line is the only move.
    yield ashore()

    # ---- 3: out to the whole island, with the card over it ----------------
    #
    # THE BARS STAY UP FOR ALL OF IT, ruled by Ash after watching: "The black
    # rectangle should be there throughout the entire thing." They used to come
    # down here and go back up for the walk, and the two seams in the middle
    # were the glitches he saw. The card draws inside the frame now, which is
    # where a title card belongs.
    #
    # `view("island")` AWAITS THE MOVE AND THEN PLAYS THE CARD. That is the
    # engine's rule and not this island's: the wide shot is where a place gets
    # its name. So the wait below is the card's own length on a camera that has
    # already arrived, and not a race between the two.
    yield view("island")
    yield wait(CARD_MS)

    # ---- 4: and only now does anybody say anything -----------------------
    #
    # The one line anybody has written about this moment. It belongs to
    # `dock_three`, a post MAPVIS has not placed, so nobody on this map can say
    # it and it has never been heard. Said here with no speaker until the post
    # exists, the way the card speaks without one. It comes AFTER the card by
    # Ash's ruling: the card names the place and the line answers it.
    yield say(WAITING)

    # ---- 5 and 6: in on him, and up the hill ------------------------------
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

    # WRITTEN HERE, AT THE TUNNEL, and nowhere earlier. Ash, 2026-09-07: a saved
    # run that has not finished the arrival plays the arrival. It sat at the top
    # for a day, one line after the crossing, on the argument that the crossing
    # happens once; the cost of that was a student who reloaded halfway up the
    # quay getting the flag, no handler, no bars and the tiller in his hands on
    # a boat already tied up. The arrival is the whole piece from the water to
    # the tunnel, so the piece being OVER is what gets written down.
    #
    # A RELOAD IN THE MIDDLE IS THEREFORE A REPLAY, and it is a safe one. The
    # engine drops `aboard` from the address the moment he steps off, so a
    # resumed run has no hull, `route(who="ship")` refuses onto the line below,
    # the refusal is caught, and everything after it -- the shot, the card the
    # session has already spent, the line, the marks and the walk -- runs from
    # wherever he is standing and ends at the same door.
    yield set_flag(CROSSED)
    yield log("walked_to_the_maw")


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
