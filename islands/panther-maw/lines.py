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


# ---- the principal, and the five lines of the rail ---------------------------
#
# ONE LINE PER STOP AND THE LINE IS THE WHY. BRIEF-MAW-RAIL-2, Ash after playing
# rail-1: *"Everything in the cutscene should be clear and easy to follow and
# make sense WHY it is happening. I have no idea what is going on: a fire, click
# two classes, it makes no sense. And if you think more text is the answer, we
# are doomed."*
#
# So the answer is not more words, it is the RIGHT words and fewer of them. The
# principal walks ahead and the student follows him, which is what an orientation
# is, and at each stop he turns round and says the one sentence that says why
# this thing is happening to you. Never an instruction: the light on the floor
# and the screen that opens are the instruction.
#
# These five are word for word from the brief and nothing may be added beside
# them. The two lines about the corner buttons that used to ride along on beats 2
# and 3 are CUT: the corner is hidden for the whole cutscene now and appears when
# the bars come down, so a sentence handing it over was a sentence about a button
# that was not on the screen.

# BEAT 1, at the tunnel mouth, after he has walked over to you.
WELCOME = "Welcome to Bonney Lake High. Come with me."

# BEAT 2, at the table, before the schedule opens.
SCHEDULE_IS_YOURS = "Your schedule. Every Panther fills one in."
# said ONLY when he closed the schedule without stamping it, so the rail can
# offer it again rather than walking him on with an empty sheet. It is not a
# sixth line: nobody on the road ever hears it.
STAMP_IT = "Fill both Elective periods, pick one club or sport, then stamp it."

# BEAT 3, at the fire, before Advisory.
ADVISORY_IS_MONDAY = "This is Advisory. Every Monday starts here."
# and when he left the questions unfinished. Recovery, like STAMP_IT.
COME_BACK = "Come back to the fire when you have a minute."

# BEAT 4, at the wall, before it opens.
WALL_IS_YOURS = "What you earn goes up here."

# every visit after the rail is over, at the desk
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
# of the thirty minutes.
CORD = "Year one is done. Here is your first cord."
# THE LAST LINE OF THE THIRTY MINUTES, and it carries nothing else. It used to
# hand over the Map as well; the corner arrives on its own the moment the bars
# come down, one second after this is read.
NEXT_TIME = "Year two, next time."
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
