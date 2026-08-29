"""The skeleton island. Copy this folder, rename it, and start deleting.

THIS IS SCAFFOLDING AND IT IS NOT PRETENDING TO BE A GOOD ISLAND. It exists so
your first week is not spent staring at an empty folder. It has one of each
thing an island needs and no more: somebody to talk to, a choice that changes
what happens next, something scored, and a row on the player's record. When the
ATC island ships it will be the example worth copying. This is the shape.

Nothing in this file is a claim about Bonney Lake High School. That is on
purpose, and your version has to keep that promise a different way: every fact
about the school needs a source, and anything you invented is marked as
invented.

WHAT TO NOTICE WHILE YOU READ IT:

  - nothing calls the two functions below. They are handed to the engine by the
    decorators, and the engine calls them when the player does something.
  - every `yield` is a thing that takes time. Every line without one is just
    Python, running instantly, exactly as it looks.
  - the two arms of the study ask the same questions in the same order out of
    the same list. What differs is who is talking. Keep it that way.
"""
from grape import manifest, on_start, on_talk
from vine import award, choose, get, log, say, set_flag

from questions import WhatAGrapeIs

# TWO DIFFERENT STRINGS, AND THEY ARE NOT INTERCHANGEABLE. One is the anchor's
# name in MAPVIS, which is what your code addresses. The other is what the
# player reads. Renaming the sign must never break the code.
GREETER_ANCHOR = "greeter"
GREETER = "the greeter"


@on_start
def opened():
    """The engine calls this the moment the island loads, before anything else."""
    yield log("island_opened", {"island": manifest()["programme"]})


@on_talk(GREETER_ANCHOR)
def meet_the_greeter():
    """The engine calls this when the player presses E on the greeter."""
    quiz = WhatAGrapeIs()

    # WHICH HALF OF THE CLASS IS THIS. Comes back None when there is no saved
    # run at all, which is what a bare test harness looks like, and None is not
    # "plain", so an island that never joined a class gets the game arm.
    plain = (yield get("mode")) == "plain"

    if plain:
        right = yield from plain_check(quiz)
    else:
        right = yield from in_character(quiz)

    # ONE ROW ON THE RECORD. `programme` names the roster entry this finishes,
    # and from that one word the engine knows the title, the credit and the cord
    # tags. READ OUT OF YOUR OWN island.json rather than typed again here: two
    # copies of one id drift, and when they do a student's grade lands on
    # somebody else's row.
    yield award(programme=manifest()["programme"], grade=quiz.grade(right))
    # your island's own corner of the flag list. The engine puts your programme
    # id in front of it, so this really is "skeleton:met_greeter" in the save and
    # nobody else's island can collide with it or read it.
    yield set_flag("met_greeter")


def in_character(quiz):
    """The game arm: somebody asks, and reacts to what you said."""
    yield say("You are the first person up this path all week.", who=GREETER)

    stay = yield choose(["Ask me something, then.", "Just looking."],
                        prompt="Well?")
    # -1 is not an index. It means nobody answered, because the list was empty
    # or the player left while the question was up.
    if stay != 0:
        yield say("Fair enough. The path is still here when you change your mind.",
                  who=GREETER)
        return 0

    right = 0
    for item in quiz.ITEMS:
        pick = yield choose(item["options"], prompt=item["ask"])
        if pick == item["answer"]:
            right = right + 1
            yield say("That is it. %s" % item["because"], who=GREETER)
        else:
            yield say("Not quite. %s" % item["because"], who=GREETER)

    yield say("%d out of %d." % (right, len(quiz.ITEMS)), who=GREETER)
    return right


def plain_check(quiz):
    """The plain arm: the same questions, as text, with nobody saying them.

    No character, no reactions, no reveal. It is a check, and a control arm that
    hands over the answers measures nothing.
    """
    for line in quiz.as_plain():
        yield say(line)

    right = 0
    for item in quiz.ITEMS:
        pick = yield choose(item["options"], prompt=item["ask"])
        if pick == item["answer"]:
            right = right + 1

    yield say("%d out of %d correct." % (right, len(quiz.ITEMS)))
    return right
