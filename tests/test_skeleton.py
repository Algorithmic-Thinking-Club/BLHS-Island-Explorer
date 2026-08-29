"""The skeleton island does what it says, in both arms.

This is also the example of how to test your own island, so it is written to be
copied. Everything here runs in plain Python with no game and no browser: the
island is a generator that yields dicts, and a test answers those dicts.

Two of these are not really about the skeleton. TheStudyHolds is about the study,
it will be true of every island anybody writes, and it is the reason as_plain()
exists. TheWordsAreFenced walks every path through the file rather than one,
because a check that only drives the happy path fences nothing.
"""
import unittest

from tests import pump

# THE WORDS A MEMBER'S FIRST COPY MAY USE. The engine understands fifteen; these
# are the nine the vine's own content already asks for. An island copied from
# this repo must not contain a word that comes back as a refusal on a beginner's
# own line, so this is a fence around the template rather than around the API.
PROVEN = {"say", "choose", "open", "play", "get", "set_flag", "award", "log", "guide_to"}

# EVERY PATH THROUGH THE ISLAND, not one. A word smuggled into a branch nobody
# drives is a word nobody checks, and the plain arm is exactly the branch a
# member never exercises by hand, because they play the game arm.
# Add a row when you add a branch.
PATHS = [
    ("the game arm, all right", "game", [0, 1, 0]),
    ("the game arm, all wrong", "game", [0, 0, 1]),
    ("the game arm, walking away", "game", [1]),
    ("the plain arm, all right", "plain", [1, 0]),
    ("the plain arm, all wrong", "plain", [0, 1]),
    ("no saved run at all", None, [0, 1, 0]),
]


def answering(mode="game", picks=()):
    """An engine that says what arm this is and clicks the buttons you name."""
    queue = list(picks)

    def answer(intent):
        if intent["kind"] == "get" and intent["path"] == "mode":
            return mode
        if intent["kind"] == "choose":
            return queue.pop(0) if queue else 0
        return None
    return answer


def walk(mode, picks):
    """Everything the island asked for down one path."""
    return pump.run("talk:greeter", answering(mode=mode, picks=picks))


class TheIslandLoads(unittest.TestCase):
    def setUp(self):
        self.manifest = pump.load("skeleton")

    def test_registers_the_handlers_the_engine_will_call(self):
        self.assertEqual(pump.handlers(), ["start", "talk:greeter"])

    def test_says_who_it_finished_for(self):
        award = pump.only(walk("game", [0, 1, 0]), "award")[0]
        self.assertEqual(award["programme"], self.manifest["programme"])


class TheWordsAreFenced(unittest.TestCase):
    def setUp(self):
        pump.load("skeleton")

    def test_every_path_uses_only_words_that_have_been_seen_performing(self):
        seen = pump.run("start")
        for name, mode, picks in PATHS:
            with self.subTest(path=name):
                self.assertEqual(set(pump.kinds(walk(mode, picks))) - PROVEN, set())
        self.assertEqual(set(pump.kinds(seen)) - PROVEN, set())

    def test_every_path_ends_with_a_row_on_the_record(self):
        # an island that finishes without awarding is an island the planner never
        # sees close, and the study's own dependent variable reads zero
        for name, mode, picks in PATHS:
            with self.subTest(path=name):
                self.assertEqual(len(pump.only(walk(mode, picks), "award")), 1)


class TheGameArm(unittest.TestCase):
    def setUp(self):
        pump.load("skeleton")

    def test_all_right_is_full_marks(self):
        # stay, then the correct answer to each of the two questions
        self.assertEqual(pump.only(walk("game", [0, 1, 0]), "award")[0]["grade"], 4.0)

    def test_all_wrong_still_records_a_row(self):
        # A GRADE OF ZERO IS NOT AN ABSENT GRADE. A member's award has to survive
        # the student who got everything wrong, or that student has no row at all
        # and the study loses exactly the people it most needs to see. The key
        # check comes first: read the value first and a missing key raises a
        # KeyError before the assertion that was supposed to explain it.
        award = pump.only(walk("game", [0, 0, 1]), "award")[0]
        self.assertIn("grade", award)
        self.assertEqual(award["grade"], 0.0)

    def test_walking_away_is_a_branch_that_ends_early(self):
        seen = walk("game", [1])
        # the opening question and nothing after it: the quiz never happened
        self.assertEqual(len(pump.only(seen, "choose")), 1)
        self.assertEqual(pump.only(seen, "award")[0]["grade"], 0.0)

    def test_somebody_is_speaking(self):
        self.assertTrue(all("who" in s for s in pump.only(walk("game", [0, 1, 0]), "say")))

    def test_remembers_the_visit(self):
        manifest = pump.load("skeleton")
        flags = [i["flag"] for i in pump.only(walk("game", [0, 1, 0]), "set_flag")]
        self.assertEqual(len(flags), 1)
        # flags are one flat list shared with every other island, so a flag
        # without the island's own name on it is a flag two members can collide
        # on. Derived from the manifest, so renaming the island moves the test.
        self.assertTrue(flags[0].startswith(manifest["programme"].replace("-", "_")), flags)


class ThePlainArm(unittest.TestCase):
    def setUp(self):
        pump.load("skeleton")

    def test_nobody_is_speaking(self):
        self.assertTrue(all("who" not in s for s in pump.only(walk("plain", []), "say")))

    def test_all_right_is_full_marks(self):
        self.assertEqual(pump.only(walk("plain", [1, 0]), "award")[0]["grade"], 4.0)

    def test_all_wrong_is_zero(self):
        # the control arm can award everybody full marks and nothing above would
        # notice, which would put the study's two halves on different scales
        self.assertEqual(pump.only(walk("plain", [0, 1]), "award")[0]["grade"], 0.0)

    def test_reads_out_everything_as_plain_promised(self):
        from questions import WhatAGrapeIs
        said = {s["text"] for s in pump.only(walk("plain", []), "say")}
        for line in WhatAGrapeIs().as_plain():
            self.assertIn(line, said)

    def test_does_not_hand_over_the_answers(self):
        from questions import WhatAGrapeIs
        quiz = WhatAGrapeIs()
        plain = "\n".join(quiz.as_plain())
        for item in quiz.ITEMS:
            # not the explanation, and not the right option singled out either:
            # a control arm that gives the answer away measures nothing
            self.assertNotIn(item["because"], plain)
            right = item["options"][item["answer"]]
            self.assertEqual(plain.count(right), 1, "the answer is called out twice")


class TheStudyHolds(unittest.TestCase):
    """The one test every island needs, and this is what it looks like."""

    def setUp(self):
        self.manifest = pump.load("skeleton")

    def scored(self, mode, picks):
        """The questions that count, in order, whoever is asking them.

        Read off the island's own items rather than off a position in the list,
        so a framing question the game arm asks and the plain arm does not is not
        mistaken for content, and so this keeps working when you add a question.
        """
        from questions import WhatAGrapeIs
        asks = {item["ask"] for item in WhatAGrapeIs.ITEMS}
        return [(c["prompt"], tuple(c["options"]))
                for c in pump.only(walk(mode, picks), "choose")
                if c.get("prompt") in asks]

    def test_asks_the_same_questions_in_both_arms(self):
        # CONTENT-CONSTANT, MEASURED. The whole study is a comparison between two
        # ways of teaching ONE thing. If the arms ask different questions, or the
        # same questions in a different order, the comparison is between two
        # different lessons and the result means nothing. Nobody eyeballs this
        # after a member edits one branch and forgets the other.
        from questions import WhatAGrapeIs
        game = self.scored("game", [0, 0, 0])
        plain = self.scored("plain", [0, 0])
        # asserted before the comparison: two empty lists are equal, and an
        # island that asks nothing would otherwise pass the study's own test
        self.assertEqual(len(game), len(WhatAGrapeIs.ITEMS))
        self.assertEqual(game, plain)

    def test_scores_the_same_way_in_both_arms(self):
        self.assertEqual(pump.only(walk("game", [0, 1, 0]), "award")[0]["grade"],
                         pump.only(walk("plain", [1, 0]), "award")[0]["grade"])

    def test_no_run_at_all_falls_back_to_the_game_arm(self):
        # get() comes back None when there is no saved run, which is what a bare
        # harness looks like. None is not "plain", and an island must not read it
        # as one, or every unjoined player silently becomes a control subject.
        seen = pump.run("talk:greeter", lambda i: 0 if i["kind"] == "choose" else None)
        self.assertTrue(all("who" in s for s in pump.only(seen, "say")))


class TheShapeOfAGrape(unittest.TestCase):
    """The rules grape.py enforces, checked where a member can read them."""

    def tearDown(self):
        # these tests fill the registry with fakes; leave it as the next test
        # file expects to find it
        pump.load("skeleton")

    def test_two_handlers_on_one_anchor_is_refused_at_import(self):
        import grape
        grape._forget()

        @grape.on_talk("post")
        def first():
            yield None

        with self.assertRaises(ValueError) as caught:
            @grape.on_talk("post")
            def second():
                yield None
        self.assertIn("post", str(caught.exception))
        self.assertIn("first", str(caught.exception))

    def test_an_anchor_that_is_not_a_name(self):
        import grape
        grape._forget()
        with self.assertRaises(ValueError):
            grape.on_talk("")

    def test_a_scored_thing_without_as_plain_says_so_by_name(self):
        import grape

        class Unwritten(grape.Scored):
            pass

        with self.assertRaises(NotImplementedError) as caught:
            Unwritten().as_plain()
        self.assertIn("Unwritten", str(caught.exception))

    def test_a_forgotten_yield_is_caught_before_the_body_runs(self):
        import grape
        ran = []

        grape._forget()

        @grape.on_start
        def forgot():
            ran.append(True)
            return 5

        with self.assertRaises(TypeError) as caught:
            pump.run("start")
        self.assertIn("yield", str(caught.exception))
        self.assertEqual(ran, [], "the body ran before anybody said it had no yield")


if __name__ == "__main__":
    unittest.main()
