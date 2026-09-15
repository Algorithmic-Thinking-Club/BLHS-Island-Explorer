"""Everything this island says and asks, and the names of the things you press.

Kept apart from island.py on purpose. What your island says and asks is CONTENT.
When it says it is CONTROL FLOW. You will want to change one without reading the
other.

Replace all of it. Keep the shape.
"""

# ---- the things a player can press -------------------------------------------
#
# Anchor NAMES from MAPVIS, not the labels a player reads. The box prints the
# label, so renaming the sign cannot break your code. If pressing E does nothing,
# the name here and the name in MAPVIS do not match.

GREETER = "greeter"


# ---- what she says -----------------------------------------------------------
#
# One idea per line, about twelve words. A wall of text is a student skipping it.

HELLO = "You're new. I'm the one they send to explain things."

# the fact the question below asks about
WHAT_WE_DO = "We meet Tuesdays in the library, and anybody can walk in."

WANT_A_GO = "Want a go?"
YES = "Go on then."
NO = "Not right now."

NOT_NOW = "Come back when you want that go."
WELL_DONE = "Nice. That is you finished here."
AGAIN = "Back again? Nothing left to do, but stay as long as you like."


# ---- what is actually scored -------------------------------------------------
#
# A `choice` and not a `quiz`, because a choice carries a reply on every option,
# and being told why you were wrong is worth more than being told that you were.
#
# Ask about YOUR thing. An island that only measures whether somebody can solve a
# puzzle has not measured whether they learned anything about it.

WHERE_WE_MEET = {
    "kind": "choice",
    "id": "skeleton-where",
    "prompt": "Where does this thing meet?",
    "options": [
        {"text": "The library, on Tuesdays", "correct": True,
         "reply": "That is it. Walk in, nobody signs you up."},
        {"text": "The gym, before school",
         "reply": "No. It is the library, and it is after school."},
        {"text": "Nowhere, it is online",
         "reply": "No. There is a room, and you turn up to it."},
    ],
}
