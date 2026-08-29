"""The words your island can say. THE GAME REPLACES THIS FILE.

Read that line again, because it is the only confusing thing in this repo. When
your island runs inside the game, the engine writes its own copy of vine.py into
the Python runtime and that copy is the one you get. This file exists for two
reasons and neither of them is the game:

  1. your editor can see the names, so `from vine import say` is not underlined
  2. `python -m unittest` can run your island's logic with no browser open

If this file and the engine's ever disagree, the engine is right. Nothing you
write here changes what the game does, and the loader refuses to load a file
called vine.py out of an island folder, so you cannot ship your own by accident.

WHAT IS HERE AND WHY IT IS ONLY NINE WORDS. The engine understands fifteen. Nine
of them have been watched working end to end, and those are the nine here. The
other six are real and the engine will answer them, but they are attached to
parts of the game that are still being built this week, so an island copied from
this repo does not use one yet. Ask before you reach for one (see NEEDS.md).

    say  choose  open  play  get  set_flag  award  log  guide_to

ONE RULE, AND IT IS THE WHOLE RULE: A WORD ONLY HAPPENS IF YOU YIELD IT. Every
function below builds a dict and does absolutely nothing else. The engine is on
the other side of a worker, and `yield` is how the dict gets to it.

    yield say("Hello.")        the line appears, and you wait for the click
    say("Hello.")              a dict is built, dropped, and nobody ever sees it

EVERY PLACE IS AN ANCHOR NAME, NEVER AN X AND A Y. Anchors are made in MAPVIS
and the name is kept separate from the label the player reads, so renaming a
sign cannot break your code. A coordinate would break the day the table moved.
"""


def say(text, who=None):
    """One line in the dialogue box. Comes back when the player clicks on."""
    intent = {"kind": "say", "text": text}
    # a key left out entirely rather than sent as None: the engine's `who` is
    # optional, and an explicit null is a different thing from an absent name
    if who is not None:
        intent["who"] = who
    return intent


def choose(options, prompt=None):
    """Buttons over the box. Comes back as the index the player picked.

    Comes back as -1, never as an index, when there was no answer at all: an
    empty options list, or the player leaving while the question was up. Check
    for -1 before you index into your own list, or you will read the last item.
    """
    intent = {"kind": "choose", "options": options}
    if prompt is not None:
        intent["prompt"] = prompt
    return intent


def open(ui):
    """Open one of the game's panels: planner, handbook, chart, wardrobe, settings.

    Yes, this shadows Python's built-in open() if you import it by name. Islands
    do not read files, so nothing here misses it, and the word is `open` because
    that is the word the engine already answers to. One spelling is worth more
    than one builtin you cannot use in here anyway.
    """
    return {"kind": "open", "ui": ui}


def play(beat, as_plain=None):
    """Run a scored activity the engine builds, and come back with the grade.

    Comes back as None, not as a zero, in three different situations: the player
    closed it without finishing, nothing was mounted to run it, or the name is
    not one the engine knows. None is not a score. Say something about it.

    LEAVE as_plain ALONE unless you mean it. Left out, the engine renders the arm
    this player was assigned when they joined, which is what keeps the two halves
    of the class looking at the same content.
    """
    intent = {"kind": "play", "beat": beat}
    if as_plain is not None:
        intent["as_plain"] = as_plain
    return intent


def get(path):
    """Ask the run about itself. A closed list, and this is all of it:

        year  gpa  tokens  cords  flags  islands  handle  mode  graduated

    `mode` is "game" or "plain" and is how your island knows which half of the
    class it is talking to.

    ANY OF THEM CAN COME BACK None when there is no saved run yet, which is what
    a bare test harness looks like. Do not do arithmetic on one without checking.
    """
    return {"kind": "get", "path": path}


def set_flag(flag):
    """Remember one thing about this player for the rest of the run.

    Your island's whole memory. Flags are shared with every other island today,
    so put your island's name in front of yours: "skeleton_met_greeter".
    """
    return {"kind": "set_flag", "flag": flag}


def award(programme=None, grade=None, tags=None, fact=None, sticker=None, badge=None):
    """Write the row your island earned onto the player's record.

    `programme` names the roster entry this finishes, and from that one word the
    engine already knows the title, the credit, the cord tags, the rank track and
    where the row goes on the transcript. An island says what it finished; it
    does not get to say what that is worth.

    `grade` is on the 0 to 4.0 scale, the same one the rest of the transcript is
    on. A grade with no programme still lands, as an anonymous row. A programme
    with no grade is how you say you finished something that is not graded.
    """
    intent = {"kind": "award"}
    # guarded on None and never on truthiness: `if value:` would read a grade of
    # zero as absent, and a student who scored nothing would get no row at all
    for key, value in (("programme", programme), ("grade", grade), ("tags", tags),
                       ("fact", fact), ("sticker", sticker), ("badge", badge)):
        if value is not None:
            intent[key] = value
    return intent


def log(event, data=None):
    """Add one typed event to the record. You add to it; you do not write it."""
    intent = {"kind": "log", "event": event}
    if data is not None:
        intent["data"] = data
    return intent


def guide_to(anchor):
    """Draw the arrow to a place, along ground that can actually be walked.

    Comes back at once. The arrow stays up and the player still has the controls,
    because being shown where to go is not the same as being taken there.
    """
    return {"kind": "guide_to", "anchor": anchor}
