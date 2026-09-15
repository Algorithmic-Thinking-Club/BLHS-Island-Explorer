"""The beach opening: he wakes on the sand, finds a bottle, and sails to the hub."""

from grape import on_start, on_talk
from vine import (
    award, enter, framing, fx, guide_to, log, pose, route, say, set_flag, show,
    sound, wait, wait_for,
)

from lines import CAST_OFF, DECIDED, LOOKING, MESSAGE, NUDGED, SPOTTED, THOR, WAKING


@on_start
def opening():
    """Everything from opening your eyes to the boat leaving."""

    # ---- he is asleep before he is awake ---------------------------------
    # the bottle is already on the map, so hide it now and show it when it lands
    yield show("the_wrack_line", False)
    # take the close shot on him before anything else
    yield framing("the_waking")
    yield pose("sleep", facing="south")
    yield sound("surf_in")
    yield wait(900)

    # ---- and then he is ---------------------------------------------------
    yield pose("sit")
    yield wait(600)
    for line in WAKING:
        yield say(line, who=THOR)
    yield pose("stand")
    yield wait(400)
    # framing(None) goes back to the map's own view
    yield framing(None)
    yield say(LOOKING, who=THOR)

    # ---- the sea puts something on the sand -------------------------------
    # play the sound and show the thing on the same beat
    yield pose(facing="west")
    yield sound("bottle")
    yield show("the_wrack_line", True)

    # framing takes a shot set up on the map, so no camera numbers live here
    yield framing("the_find")
    # let the camera arrive before he speaks
    yield wait(900)
    yield fx("spark", anchor="the_wrack_line")
    yield say(SPOTTED, who=THOR)
    yield wait(500)
    yield framing(None)

    # ---- the arrow, and then the walk is taken ----------------------------
    # wait_for answers True if he walked there himself, False if the time ran out
    yield guide_to("the_wrack_line")
    arrived = yield wait_for("the_wrack_line", ms=9000)
    if not arrived:
        yield say(NUDGED, who=THOR)
        # route walks him along a path drawn on the map
        yield route("the_wrack_walk")

    # ---- what is in it ----------------------------------------------------
    yield sound("cork_pop")
    yield wait(400)
    for line in MESSAGE:
        yield say(line, who=THOR)
    yield set_flag("read_the_bottle")
    yield log("bottle_opened", {"walked": arrived})

    # ---- down to the water ------------------------------------------------
    yield say(DECIDED, who=THOR)
    yield guide_to("the_jetty")
    yield route("the_long_way")

    # ---- and off ----------------------------------------------------------
    # route(..., who="ship") puts him aboard and sails the line, and returns when it is done
    yield sound("board")
    yield say(CAST_OFF, who=THOR)
    yield route("the_crossing", who="ship")

    # watch her get her head round before the cut. A crossing that cuts away the
    # instant the sail fills reads as a loading screen, not as leaving.
    yield wait(1800)

    # enter is a door, and this one goes to the hub under a cover
    yield enter("hub", at="panthers_maw")

    # award(fact=...) adds a Handbook fact and no grade
    yield award(fact="the_bottle")


@on_talk("the_wrack_line")
def the_bottle_again():
    """If he comes back to it afterwards."""
    yield say(MESSAGE[-1], who=THOR)
