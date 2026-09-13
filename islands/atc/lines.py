"""Everything anybody says on the ATC island, in one place.

An island is a folder and this is the first reason why. What the island SAYS is
content and WHEN it says it is control flow, and the day somebody wants to change
one without reading the other they will be glad these were apart.

WHO IS SPEAKING IS AN ANCHOR NAME. The box prints the LABEL whoever placed that
anchor typed in MAPVIS, never the string your code uses. So the plate over these
lines reads "the club president" because that is the label on his post, and
renaming that label cannot break a line of this file.

HOW LONG A LINE MAY BE, AND HOW MANY. One idea, about twelve words, and one line
per stop. Ash, after playing a version that broke it: "a bunch of words, a bunch
of instructions that open to read more words. A student doesn't know what the
hell is going on." The light on the floor and the screen that opens are the
instruction. The words only confirm them.

AND THEY ARE WRITTEN AS SOMEBODY TALKING. Not as a game. Nobody announces
themselves, nobody makes a speech, and nothing here is trying to sound clever.
"""

# ---- who is speaking ---------------------------------------------------------
#
# These are anchor names from the map, not people's names. HOST is the post at the
# top of the stair, TROPHIES is the plinth, DESK is the machine that is switched on.

HOST = "host"
TROPHIES = "trophies"
DESK = "the_desk"


# ---- stop 1, at the top of the stair ----------------------------------------
#
# TWO SHORT SENTENCES AND NOT ONE LONG ONE. A greeting really is two sentences,
# and the second one is doing the most important work on the island: it is the
# only place a student is told when ATC meets and how to get in. The scored
# question at the end asks about it, so it has to be said BEFORE the activity and
# not after, or the island is grading a fact it never gave.

HELLO = "Hi, I'm Ashwath. Welcome to the computer science club."
WHEN_AND_HOW = "We're in 303 after school until three. There's a form if you want to join."

# and what he says on every visit after the first
AGAIN = "Back again. Grab a machine whenever you want."


# ---- stop 2, the medal plinth ------------------------------------------------
#
# THE WALL SAYS THIS, NOT A PERSON, which is why it is one line and not a list. A
# place that shows you its medals is better than somebody reciting them. Every
# number in it is real: Regionals took first, second and third in Computer
# Programming, State took first and third, and one member competed at Nationals.
# Sourced to docs/ops/ATC-ISLAND-DESIGN.md section 1, which is Ash himself,
# because ATC is not on the official clubs list.

MEDALS = "First year we existed, and we made it to Nationals."


# ---- stop 3, at the machine that is on ---------------------------------------
#
# THE RECURSION, SAID AT THE ONE MOMENT IT IS LITERALLY TRUE. A freshman standing
# on a painted island, being told the island is the thing this club builds, is the
# whole argument for ATC in one sentence. It belongs here rather than at the door,
# where it would be a boast.

THE_GAME = "This is the game we're building. You're playing it right now."
WANT_A_GO = "Somebody left this part half finished. Want to try it?"

YES = "Sure"
NO = "Not right now"

# said when he says no, so the offer stays open rather than closing
COME_BACK = "It'll still be here. Have a look around."


# ---- stop 4, when the result card closes -------------------------------------
#
# NOT A CONGRATULATION ON A SCORE. He says what the student just did was the
# ordinary work of the club, which is a bigger thing to hear than "well done".

WELL_DONE = "Nice. That's what we do in here every week."


# ---- stop 5, the last thing said on the island -------------------------------
#
# THE JOIN MOMENT, AND THERE IS NOTHING TO PRESS. The student already committed a
# season to ATC on the year sheet before the ship ever sailed, so asking "do you
# want to join?" would be the game asking about a decision it watched them make.
#
# What it does instead is name the step the game cannot take for them. A game can
# teach a fourteen year old that room 303 exists, what happens in it and what to
# do about it. It cannot enrol them, and pretending otherwise is the one kind of
# lie this project has no room for.

FORM = "Form's on the desk by the door. Come by whenever."
