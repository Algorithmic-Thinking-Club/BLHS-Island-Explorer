"""The hub: the ship sails in, he steps onto the dock, and he walks up to the tunnel.

Named on the map: the sail line `the_hub_approach` and the door `panthers_maw`.
"""
from grape import on_start, on_talk
from vine import (
    ashore, end_run, get, guide_to, log, movie, route, say, set_flag, view, wait,
    walk_to,
)

from lines import DOCK_ONE, DOCK_THREE, DOCK_TWO, HELLO, KEEP_GOING, WAITING

# the line the ship follows in, drawn on the hub in MAPVIS with kind `sail`
SAIL_LINE = "the_hub_approach"

# the tunnel into the mountain, and what the third person points at
DOOR = "panthers_maw"

# set once the arrival is over, so walking back out of the mountain does not replay it
CROSSED = "hub:crossed"

# how long the ship lies at the dock before he steps off her
TIED_UP_HOLD_MS = 900

# how long the arrival card owns the screen, so the walk does not start underneath it
CARD_MS = 3900


def sailing_out():
    """The last beat of the year: the ship sails back out and the title returns."""
    year = yield get("year")

    # he sails home, which is the whole of this beat
    yield log("year_one_over", {"year": year})

    # ---- to black, and the title -------------------------------------------
    # `end_run` is the last word an island can say, and the save it leaves is
    # what the title reads
    yield end_run()


def turned(year):
    """The flag the engine writes the moment a year's page has turned."""
    return "yearbook:y%d" % year


@on_start
def arriving():
    """The one handler the engine calls. A run that has not crossed yet gets the
    arrival; a run whose yearbook page has turned gets the departure and the title.
    """
    year = yield get("year")
    flags = yield get("flags")
    if turned(year) in flags:
        yield from sailing_out()
        return
    yield from putting_in()


def putting_in():
    """The crossing and the walk up, once per run, until he stands at the tunnel.

    `route(..., who="ship")` sails her in and the engine ties her up at the berth
    nearest the end of the line. The bars stay up from the water to the tunnel.
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
    # a beat first, so a student sees her lying at the dock
    yield wait(TIED_UP_HOLD_MS)

    # `ashore()` puts him on the boards and leaves the camera where it is. The
    # card plays on the wide shot below, not here.
    yield ashore()

    # ---- 3: out to the whole island, with the card over it ----------------
    # `view("island")` finishes the move and then plays the card, so the wait
    # below is only the card's own length
    yield view("island")
    yield wait(CARD_MS)

    # ---- 4: and only now does anybody say anything -----------------------
    # said with no speaker, because the post that owns this line is not placed
    # on the map yet
    yield say(WAITING)

    # ---- 5 and 6: in on him, and up the hill ------------------------------
    #
    # He is not playing this stretch, he is being shown the way, and the marks
    # on the ground are what he is being shown.
    yield view("close")
    # `guide_to` draws the arrow marks along the route and hangs the pointer over the door
    yield guide_to(DOOR)
    yield walk_to(DOOR)
    # the frame stays up on purpose: he reaches the tunnel still in the close
    # shot, and the engine hands the controls back when this handler returns

    # the flag is written here, at the tunnel, so a run that reloads halfway up
    # plays the arrival again from wherever he is standing
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
    """Says the line, then lights the way to the tunnel with `guide_to`."""
    yield say(WAITING, who=DOCK_THREE)
    yield guide_to(DOOR)
