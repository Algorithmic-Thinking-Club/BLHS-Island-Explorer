"""The skeleton island does what it says.

This is also the example of how to test your own island, so it is written to be
copied. Everything here runs in plain Python with no game and no browser: an
island is a set of generators that yield dicts, and a test answers those dicts.

It proves your logic and nothing else. Nothing in here performs anything, so a
green test and a broken island are perfectly compatible. The game is the only
place your island really runs.
"""
import unittest

from tests import pump

ISLAND = "skeleton"

# the words the template may use. A word aimed at a name the map does not carry
# is refused on the line that asked for it, so the island somebody copies first
# should not contain one. Widen this when your map really has the anchors.
PROVEN = {"say", "choose", "get", "set_flag", "award", "log", "guide_to",
          "objective", "island_tasks", "task_done", "play"}

# every road through the island, each with the buttons a player presses and what
# the activity comes back as. Add a row when you add a branch.
ROADS = [
    ("all the way through", {"choices": [0]}),
    ("says not right now", {"choices": [1]}),
    ("closes the activity", {"choices": [0], "score": None}),
    ("comes back to a finished island", {"flags": ["finished:y1"]}),
]


class TheIslandLoads(unittest.TestCase):
    def setUp(self):
        self.manifest = pump.load(ISLAND)

    def test_it_registers_what_the_game_will_call(self):
        self.assertEqual(pump.handlers(), ["start", "talk:greeter"])

    def test_it_reads_its_own_manifest(self):
        import grape
        self.assertEqual(grape.manifest()["programme"], self.manifest["programme"])
        # a copy, so editing what you got back cannot change what the game thinks
        grape.manifest()["programme"] = "not-yours"
        self.assertEqual(grape.manifest()["programme"], self.manifest["programme"])

    def test_every_road_uses_only_words_that_have_been_watched_working(self):
        said = set(pump.kinds(pump.run("start", pump.answering())))
        for name, state in ROADS:
            with self.subTest(road=name):
                said |= set(pump.kinds(pump.run("talk:greeter", pump.answering(**state))))
        self.assertEqual(said - PROVEN, set())


class TheTaskList(unittest.TestCase):
    """What the island is asking for, and whether the rows can be ticked."""

    def setUp(self):
        pump.load(ISLAND)

    def test_the_list_goes_up_on_every_load(self):
        for state in ({}, {"flags": ["finished:y1"]}):
            with self.subTest(**state):
                seen = pump.run("start", pump.answering(**state))
                rows = pump.only(seen, "island_tasks")
                self.assertEqual(len(rows), 1)
                self.assertEqual([t["id"] for t in rows[0]["tasks"]], ["meet", "answer"])

    def test_every_row_it_declares_can_actually_be_ticked(self):
        # a row nobody can tick is an island nobody can finish, and the way back
        # to the dock never appears
        declared = {t["id"] for t in
                    pump.only(pump.run("start", pump.answering()), "island_tasks")[0]["tasks"]}
        ticked = set()
        for name, state in ROADS:
            for i in pump.only(pump.run("talk:greeter", pump.answering(**state)), "task_done"):
                ticked.add(i["id"])
        self.assertEqual(declared, ticked)

    def test_a_row_ticks_when_it_is_true_and_not_on_the_way_in(self):
        kinds = pump.kinds(pump.run("talk:greeter", pump.answering(choices=[0])))
        self.assertLess(kinds.index("say"), kinds.index("task_done"))


class TheActivity(unittest.TestCase):
    def setUp(self):
        self.manifest = pump.load(ISLAND)

    def road(self, **state):
        return pump.run("talk:greeter", pump.answering(**state))

    def test_finishing_writes_one_row_with_the_grade_that_was_earned(self):
        rows = pump.only(self.road(choices=[0], score=2.5), "award")
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["programme"], self.manifest["programme"])
        self.assertEqual(rows[0]["grade"], 2.5)

    def test_a_grade_of_zero_is_still_a_row(self):
        # a student who got everything wrong has to have a row, or the transcript
        # loses exactly the people it most needs to show
        row = pump.only(self.road(choices=[0], score=0), "award")[0]
        self.assertIn("grade", row)
        self.assertEqual(row["grade"], 0)

    def test_saying_not_right_now_never_reaches_the_activity(self):
        seen = self.road(choices=[1])
        self.assertEqual(pump.only(seen, "play"), [])
        self.assertEqual(pump.only(seen, "award"), [])
        # and the line at the top is handed back rather than left on the glass
        self.assertIn(None, [i.get("text") for i in pump.only(seen, "objective")])

    def test_closing_the_activity_is_not_a_zero(self):
        seen = self.road(choices=[0], score=None)
        self.assertEqual(pump.only(seen, "award"), [])
        self.assertIn(None, [i.get("text") for i in pump.only(seen, "objective")])

    def test_the_line_at_the_top_comes_back_even_when_the_activity_refuses(self):
        # `play` refuses rather than returning when a question will not validate,
        # which is the mistake a member is most likely to make in lines.py
        trail = []
        engine = pump.answering(choices=[0])

        def answer(intent):
            trail.append(intent)
            if intent["kind"] == "play":
                raise pump.Refused("that question has two options with the same id")
            return engine(intent)

        with self.assertRaises(Exception):
            pump.run("talk:greeter", answer)
        self.assertIn(None, [i.get("text") for i in trail if i["kind"] == "objective"])


class TheYear(unittest.TestCase):
    """An island can be taken again in a later year, so it has to close twice."""

    def setUp(self):
        pump.load(ISLAND)

    def test_the_done_flag_carries_the_year(self):
        seen = pump.run("talk:greeter", pump.answering(year=2, choices=[0]))
        self.assertEqual([i["flag"] for i in pump.only(seen, "set_flag")], ["finished:y2"])

    def test_a_finished_year_asks_for_nothing(self):
        seen = pump.run("start", pump.answering(flags=["finished:y1"]))
        self.assertEqual(pump.only(seen, "guide_to"), [])
        self.assertEqual(pump.only(seen, "objective"), [])


class TheShapeOfAnIsland(unittest.TestCase):
    """The rules grape.py holds you to, checked where a member can read them."""

    def tearDown(self):
        # these fill the registry with fakes; leave it as the next file expects
        pump.load(ISLAND)

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

    def test_a_forgotten_yield_is_caught_and_named(self):
        import grape
        grape._forget()

        @grape.on_start
        def forgot():
            return 5

        with self.assertRaises(TypeError) as caught:
            pump.run("start")
        self.assertIn("yield", str(caught.exception))
        self.assertIn("forgot", str(caught.exception))

    def test_a_handler_behind_your_own_decorator_is_not_accused(self):
        # a wrapper returns a generator without being one, so the check has to be
        # on what the call gives back rather than on the function
        import grape
        grape._forget()

        def logged(fn):
            def wrapper():
                return fn()
            return wrapper

        @grape.on_start
        @logged
        def go():
            yield {"kind": "log", "event": "ran"}

        self.assertEqual(pump.kinds(pump.run("start")), ["log"])


if __name__ == "__main__":
    unittest.main()
