"""Every line anybody says on the ATC island.

One idea per line, about twelve words, written as somebody talking. `who=` takes
an anchor name and the box prints the label that anchor carries on the map.
"""

# ---- who is speaking ---------------------------------------------------------
#
# These are anchor names from the map, not people's names. HOST is the post at the
# top of the stair, TROPHIES is the plinth, DESK is the machine that is switched on.

HOST = "host"
TROPHIES = "trophies"
DESK = "the_desk"


# ---- stop 1, at the top of the stair ----------------------------------------
# the greeting, then the line that says when the club meets and how to join

HELLO = "Hi, I'm Ashwath. Welcome to the computer science club."
WHEN_AND_HOW = "We're in 303 after school until three. There's a form if you want to join."

# and what he says on every visit after the first
AGAIN = "Back again. Grab a machine whenever you want."

# ---- what he says on a second year of the club -------------------------------
# said instead of the first-year lines when get("rank") shows a second year
SECOND_YEAR = (
    "You came back. Most people don't. That makes you one of about five "
    "who've done two years of this."
)
# said instead of the beginner's explanation, because he already knows where 303 is
SECOND_YEAR_HOW = (
    "You know where we are and you know how it works. So this year you're not "
    "just fixing my program, you're the one people ask."
)
# the machine, on a second year: the same puzzle, a different reason to be at it
SECOND_YEAR_DESK = "Same broken program. See if it's still hard."


# ---- stop 2, the medal plinth ------------------------------------------------
# the plinth says this, not a person, so it stays one line

MEDALS = "First year we existed, and we made it to Nationals."


# ---- stop 3, at the machine that is on ---------------------------------------

THE_GAME = "This is the game we're building. You're playing it right now."
WANT_A_GO = "Somebody left this part half finished. Want to try it?"

YES = "Sure"
NO = "Not right now"

# said when he says no, so the offer stays open rather than closing
COME_BACK = "It'll still be here. Have a look around."


# ---- stop 4, when the result card closes -------------------------------------
# praises the work, not the score

WELL_DONE = "Nice. That's what we do in here every week."


# ---- stop 5, the last thing said on the island -------------------------------
# the join moment, and there is nothing to press: it names the step outside the game

FORM = "Form's on the desk by the door. Come by whenever."
