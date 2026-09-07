"""Everything anybody says in the Maw, in one place.

An island is a folder and this is the first reason why. What the room SAYS is
content, and WHEN it says it is control flow, and the day somebody wants to
change one without reading the other they will be glad these were apart.

The names below are also the answer to a question you will hit in your own
island: who is talking. A speaker is an ANCHOR NAME, and the box prints the
label whoever placed that anchor typed in MAPVIS, never this string. So the
counselor's plate reads "The Counselor" because that is the label on her post,
and renaming that label cannot break a line of this file.

Two names are not anchors. THOR is the reserved word for the player, and the box
puts the name the student chose at setup on the plate. TABLE is THOR on purpose:
the chart table is furniture, furniture does not talk, and the anchor carries no
label anyway, so naming it as the speaker would print the raw identifier
`chart_table` at the exact spot a person's name goes.

HOW LONG A LINE MAY BE, AND HOW MANY. One idea, about twelve words, and ONE LINE
PER BEAT. That second half is BRIEF-MAW-RAIL and it is stricter than what was
here: year one walks a student between five places, and at each one exactly one
person says exactly one thing before the thing happens. Ash played the version
with three lines a beat: "a bunch of words, a bunch of instructions that open to
read more words. A student doesn't know what the hell is going on."

That rule is not a style preference, it is the literal-words law: a student who
skips every line in this room must still end up understanding where the table
is, because the light on the floor taught them and the text only confirmed it.
And every line says the school thing first. Advisory is Advisory, the yearbook is
the yearbook, the cords are your cords.
"""

# ---- who is speaking ---------------------------------------------------------

THOR = "thor"
HEARTH = "hearth"
COUNSELOR = "counselor"
PRINCIPAL = "principal_desk"
WALL = "trophy_wall"
OUTFITTER = "outfitter"
TABLE = THOR

# the one drawn face in the game so far. It is the `principal-pro` character
# MAPVIS drew for this very room, cropped, and Ash locked it: do not draw
# another one. A line with no portrait shows a plate with no face, which is what
# nearly every line in this game is.
FACE = "principal"


# ---- the principal, and the lines of the rail --------------------------------
#
# BEAT 1. He walks over and says this and nothing else. The pick screen opens
# right after it, and the pick screen is the thing that explains the year, by
# being a screen of cards a student can press. There is no tour and no speech.
# He does not describe the room; the table lights and the student is walked to it.

WELCOME = "Welcome to Bonney Lake. Let's plan your year."

# BEAT 2, after the cards have been stamped. It is the handover of the corner's
# middle button as well as the answer to the stamp: BRIEF-MAW-RAIL gives each of
# the three corner buttons one line at the moment it first matters, and this is
# My Year's.
YEAR_SET = "That is your year. It is in My Year, in the corner."
# said only when he closed the cards without stamping, so the rail can offer them
# again rather than walking him on with an empty sheet
STAMP_IT = "Pick one club or sport and two classes, then stamp it."

# BEAT 3, after Advisory. The Guide's handover, and the only thing said about a
# score, because the pop over the map is the result.
GUIDE_IS_YOURS = "Everything you just learned is in your Guide, in the corner."
# and when he left the questions unfinished
COME_BACK = "Come back to the fire when you have a minute."

# every visit after the rail, at the desk
BACK_AGAIN = "Everything you need is on the walls. Take a look around."


# ---- the fire ----------------------------------------------------------------
#
# NOTHING IS SAID AFTER THE QUESTIONS ANY MORE. The reward pop names what was
# finished and what it was worth, over the map, and that is the result. A line
# here as well was the same fact said twice.

CIRCLE = "Advisory is starting. Answer the questions."
BANKED = "Advisory is done for this year. Come back next year."
# `play` comes back None when they closed the panel, and None is not a score
LEFT = "You did not finish Advisory. Come back when you have a minute."


# ---- the counselor -----------------------------------------------------------

NOTHING_YET = "No cord started yet. That is what four years are for."
ASK = "Ask about the cords?"
SHOW_ME = "Open the Guide"
NOT_NOW = "Not now"

# BEAT 5. She has the cord, the yearbook turns the page, and then the last line
# of the thirty minutes, which carries the Map's handover with it.
CORD = "Year one is done. Here is your first cord."
NEXT_TIME = "Year two, next time. The Map in the corner is yours."
# the counselor pressed on the way out with the year still open
YEAR_DONE = "Year one is done. Let's turn the page and see what you earned."


# ---- the chart table ---------------------------------------------------------

SHEET = "This is My Year. Plan all four years here."


# ---- the outfitter -----------------------------------------------------------

NOOK = "Pick a new coat color. Nothing here costs anything."


# ---- the trophy wall ---------------------------------------------------------

#
# NO NUMBER IN EITHER LINE, ON PURPOSE. The wall panel counts frames (Advisory
# and the classes and the picks), the drape counts things on the wall, and the
# stickers and badges the run holds are a third count. Thor used to say "no
# badges on the wall yet" over a panel reading "3 of 6 frames filled"
# (STATE-OF-THE-GAME confusing 9). The panel is the readout; he introduces it.
EMPTY_WALL = "This is my trophy wall. What I earn this year goes up here."
FULL_WALL = "This is my trophy wall. Let's see what is on it."
