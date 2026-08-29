"""The skeleton island does what it says, in both arms.

This is also the example of how to test your own island, so it is written to be
copied. Everything here runs in plain Python with no game and no browser: the
island is a generator that yields dicts, and a test answers those dicts.

The one test in here that is not really about the skeleton is
test_asks_the_same_questions_in_both_arms. That one is about the study, it will
be true of every island anybody writes, and it is the reason as_plain() exists.
"""
import unittest

from tests import pump

# THE WORDS A MEMBER'S FIRST COPY MAY USE. The engine understands fifteen; these
# are the ones watched working end to end. An island copied from this repo must
# not contain a word that comes back as a refusal on a beginner's own line, so
# this list is a fence around the template rather than around the API.
PROVEN = {"say", "choose", "open", "play", "get", "set_flag", "award", "log", "guide_to"}


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


class TheIslandLoads(unittest.TestCase):
    def setUp(self):
        self.manifest = pump.load("skeleton")

    def test_registers_the_handlers_the_engine_will_call(self):
        self.assertEqual(pump.handlers(), ["start", "talk:greeter"])

    def test_uses_only_words_that_have_been_seen_performing(self):
        seen = pump.run("talk:greeter", answering()) + pump.run("start")
        self.assertEqual(set(pump.kinds(seen)) - PROVEN, set())

    def test_says_who_it_finished_for(self):
        seen = pump.run("talk:greeter", answering())
        award = pump.only(seen, "award")[0]
        self.assertEqual(award["programme"], self.manifest["programme"])


class TheGameArm(unittest.TestCase):
    def setUp(self):
        pump.load("skeleton")

    def test_all_right_is_full_marks(self):
        # stay, then the correct answer to each of the two questions
        seen = pump.run("talk:greeter", answering(picks=[0, 1, 0]))
        self.assertEqual(pump.only(seen, "award")[0]["grade"], 4.0)

    def test_all_wrong_still_records_a_row(self):
        # A GRADE OF ZERO IS NOT AN ABSENT GRADE. A member's award has to survive
        # the student who got everything wrong, or that student has no row at all
        # and the study loses exactly the people it most needs to see.
        seen = pump.run("talk:greeter", answering(picks=[0, 0, 1]))
        award = pump.only(seen, "award")[0]
        self.assertEqual(award["grade"], 0.0)
        self.assertIn("grade", award)

    def test_walking_away_is_a_branch_that_ends_early(self):
        seen = pump.run("talk:greeter", answering(picks=[1]))
        # the opening question and nothing after it: the quiz never happened
        self.assertEqual(len(pump.only(seen, "choose")), 1)
        self.assertEqual(pump.only(seen, "award")[0]["grade"], 0.0)

    def test_somebody_is_speaking(self):
        seen = pump.run("talk:greeter", answering(picks=[0, 1, 0]))
        self.assertTrue(all("who" in s for s in pump.only(seen, "say")))

    def test_remembers_the_visit(self):
        seen = pump.run("talk:greeter", answering())
        flags = [i["flag"] for i in pump.only(seen, "set_flag")]
        self.assertEqual(flags, ["skeleton_met_greeter"])
        # a flag shared with every other island needs the island's name on it
        self.assertTrue(flags[0].startswith("skeleton"), flags)


class ThePlainArm(unittest.TestCase):
    def setUp(self):
        pump.load("skeleton")

    def test_nobody_is_speaking(self):
        seen = pump.run("talk:greeter", answering(mode="plain"))
        self.assertTrue(all("who" not in s for s in pump.only(seen, "say")))

    def test_scores_the_same_way(self):
        seen = pump.run("talk:greeter", answering(mode="plain", picks=[1, 0]))
        self.assertEqual(pump.only(seen, "award")[0]["grade"], 4.0)

    def test_does_not_hand_over_the_answers(self):
        from questions import WhatAGrapeIs
        plain = " ".join(WhatAGrapeIs().as_plain())
        for item in WhatAGrapeIs.ITEMS:
            self.assertNotIn(item["because"], plain)


class TheStudyHolds(unittest.TestCase):
    """The one test every island needs and this is what it looks like."""

    def setUp(self):
        pump.load("skeleton")

    def test_asks_the_same_questions_in_both_arms(self):
        # CONTENT-CONSTANT, MEASURED. The whole study is a comparison between two
        # ways of teaching ONE thing. If the arms ask different questions, or the
        # same questions in a different order, the comparison is between two
        # different lessons and the result means nothing. Nobody can eyeball this
        # after a member edits one branch and forgets the other, so it is a test.
        def asked(mode):
            seen = pump.run("talk:greeter", answering(mode=mode, picks=[0, 0, 0]))
            return [(c.get("prompt"), tuple(c["options"])) for c in pump.only(seen, "choose")]

        game = asked("game")
        plain = asked("plain")
        # the game arm opens with a question of its own, which is presentation
        # rather than content; from there the two have to agree exactly
        self.assertEqual(game[1:], plain)

    def test_no_run_at_all_falls_back_to_the_game_arm(self):
        # get() comes back None when there is no saved run, which is what a bare
        # harness looks like. None is not "plain", and an island must not read it
        # as one, or every unjoined player silently becomes a control subject.
        seen = pump.run("talk:greeter", lambda intent: 0 if intent["kind"] == "choose" else None)
        self.assertTrue(all("who" in s for s in pump.only(seen, "say")))


class TheShapeOfAGrape(unittest.TestCase):
    """The rules grape.py enforces, checked where a member can read them."""

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

    def test_a_scored_thing_without_as_plain_says_so_by_name(self):
        import grape

        class Unwritten(grape.Scored):
            pass

        with self.assertRaises(NotImplementedError) as caught:
            Unwritten().as_plain()
        self.assertIn("Unwritten", str(caught.exception))

    def test_a_forgotten_yield_is_caught_at_dispatch(self):
        import grape
        grape._forget()

        @grape.on_start
        def forgot():
            return 5

        with self.assertRaises(TypeError) as caught:
            pump.run("start")
        self.assertIn("yield", str(caught.exception))


if __name__ == "__main__":
    unittest.main()
