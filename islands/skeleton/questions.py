"""The scored half, kept in its own file on purpose.

An island is a folder, not a file, and this is the first reason why: what your
island ASKS is content, and when it asks it is control flow, and the day you
want to change one without reading the other you will be glad they were apart.

Everything the player is asked lives in ITEMS, once. Both halves of the class
read that same list: the game arm hears it from a character and the plain arm
reads it as text. That is the only difference between them, and it has to stay
the only difference, or the study is comparing two different lessons instead of
two ways of teaching one.

REPLACE ALL OF THIS. Write questions about your club, your sport, your class.
Two rules from the content policy and they are not negotiable: every fact about
BLHS needs a source, and anything you made up gets marked as made up.
"""
from grape import Scored


class WhatAGrapeIs(Scored):
    """Two questions about the thing you are reading, which is a stand-in.

    Your version asks about the real thing your island is about. This one asks
    about the API so that the template teaches something instead of shipping
    lorem ipsum, and so that nothing in it is a claim about the school.
    """

    title = "what a grape is"

    ITEMS = [
        {
            "ask": "What makes one of vine's words actually happen?",
            "options": ["Calling it", "Putting yield in front of it", "Importing it"],
            "answer": 1,
            "because": "A call with no yield builds a dict, drops it, and the engine never hears about it.",
        },
        {
            "ask": "Who decides when on_talk runs?",
            "options": ["The engine, when the player presses E", "Your island, at the top of the file"],
            "answer": 0,
            "because": "You register handlers. The game calls them. That is the whole shape of an island.",
        },
    ]

    def grade(self, right):
        """0 to 4.0, because that is the scale the rest of the transcript is on.

        Your curve is yours. Give partial credit, punish a second wrong answer,
        weight the hard question double: this is a method you override, not a
        number the engine hands you, and that is deliberate.
        """
        return round(4.0 * right / len(self.ITEMS), 2)

    def as_plain(self):
        """The same two questions, as flat text, with nobody saying them.

        No answers in here. The plain arm is a check, not a study guide, and a
        control arm that gives the answer away measures nothing.
        """
        lines = []
        for n, item in enumerate(self.ITEMS, 1):
            options = "   ".join(
                "%d) %s" % (i + 1, text) for i, text in enumerate(item["options"]))
            lines.append("%d. %s" % (n, item["ask"]))
            lines.append("   %s" % options)
        return lines
