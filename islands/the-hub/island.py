"""THE HUB: the crossing and the dock, as an island.

BRIEF-YEAR-ONE beats 2 and 3. The ship sails itself in and the student watches
the island get bigger. He steps off. Three people on the way up say one line
each; the third says the principal is waiting up there, and the tunnel lights.

THIS IS THE VINE'S OWN CONTENT and it runs unscoped, like the Maw: the flag it
writes is a bare name. A member's island is scoped and should be. Read
`islands/panther-maw/island.py` for the whole argument; read this one for the
smallest honest shape of an island that does something on arrival and answers
three posts.

EVERY NAME HERE IS ONE ASH IS PLACING IN MAPVIS (docs/ops/ARC-MANIFEST.md): the
sail line `the_hub_approach`, the three posts `dock_one`, `dock_two` and
`dock_three`, and the door `panthers_maw`, which the hub already carries. Until
the hub is republished with them, the engine says so by name the moment this
island loads, listing the anchors the map really has, and the handlers below
simply never fire. Nothing crashes and the map keeps working: the student sails
in and walks up exactly as before, with the year's own light on the door.
"""
from grape import on_start, on_talk
from vine import get, guide_to, log, route, say, set_flag

from lines import DOCK_ONE, DOCK_THREE, DOCK_TWO, HELLO, KEEP_GOING, WAITING

# the line the ship follows in, drawn on the hub in MAPVIS with kind `sail`
SAIL_LINE = "the_hub_approach"

# the tunnel into the mountain, and what the third person points at
DOOR = "panthers_maw"

# this run has already been sailed in. Bare, because this island is unscoped;
# see the note at the top. Without it the hub would put him back in the boat
# every time he walked out of the mountain.
CROSSED = "hub:crossed"


@on_start
def putting_in():
    """The crossing, the first time the hub loads and never again.

    `route(..., who="ship")` is how a voyage starts. On a sea arrival the hull
    is already on the water where the beach left it, the ship runs the line,
    and the ENGINE ties her up at the berth nearest the line's end and pays the
    arrival card the moment he steps ashore. Nothing here says the island's
    name; the card does, where he lands.

    THE REFUSAL IS CAUGHT, AND THAT IS UNUSUAL. Almost every word in an island
    should be allowed to raise: a refusal on your own line is how you find out a
    name is wrong. This one is caught because the crossing has a fallback the
    engine already performs: with no line the student sails her in himself, by
    the keys or by clicking the water, and the tie-up is one press. Losing the
    handler here would lose nothing else, but the refusal is still LOGGED with
    the engine's own sentence, because a silent one is a name nobody fixes.
    """
    flags = yield get("flags")
    if CROSSED in flags:
        return

    try:
        yield route(SAIL_LINE, who="ship")
        yield log("crossing_sailed", {"path": SAIL_LINE})
    except Exception as refused:
        yield log("route_refused", {"path": SAIL_LINE, "why": str(refused)})

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

    `guide_to` raises the arrow and the light on the door. The year's own
    objective is already pointing there from another map ("go into the mountain
    and find the principal"), so this is the same target said at the moment he
    is told about it, and the door itself takes the arrow down when he goes
    through: a door tears the scene down and nothing survives it.
    """
    yield say(WAITING, who=DOCK_THREE)
    yield guide_to(DOOR)
