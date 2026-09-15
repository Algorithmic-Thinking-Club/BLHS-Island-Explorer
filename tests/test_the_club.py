"""Tests for the ATC island, the template a member copies."""
import unittest

try:
    from tests import pump
except ImportError:
    import pump

ISLAND = "atc"


def answering(refuse=(), **state):
    """Build the run state a test hands to the island.

    Flags are spelled the way your island receives them, with no `atc:` in front,
    because the engine scopes a member island's flags for you.
    """
    return pump.answering(refuse=refuse, **state)


class TheIslandLoads(unittest.TestCase):
    def setUp(self):
        pump.load(ISLAND)

    def test_it_claims_the_three_things_a_student_can_press(self):
        got = set(pump.handlers())
        self.assertIn("start", got)
        for who in ("talk:host", "talk:the_desk", "talk:trophies"):
            self.assertIn(who, got)


class TheTaskList(unittest.TestCase):
    """The tasks the island declares, and when each row ticks."""

    def setUp(self):
        pump.load(ISLAND)

    def test_the_list_goes_up_on_every_load_so_a_re_entry_is_harmless(self):
        seen = pump.run("start", answering())
        decls = pump.only(seen, "island_tasks")
        self.assertEqual(len(decls), 1)
        self.assertEqual([t["id"] for t in decls[0]["tasks"]], ["meet", "program"])
        # and again, with the island already met, because `island_tasks` replaces
        again = pump.run("start", answering(flags=["met"]))
        self.assertEqual(len(pump.only(again, "island_tasks")), 1)

    def test_every_row_it_declares_can_actually_be_ticked(self):
        """Every task the island declares can be ticked on some path through it."""
        declared = {t["id"] for t in pump.only(pump.run("start", answering()), "island_tasks")[0]["tasks"]}
        ticked = set()
        for road, state in (
            ("talk:host", {}),
            ("talk:host", {"flags": ["met"]}),
            # the student who pressed the machine first and comes back to him after
            ("talk:host", {"flags": ["met", "built:y1"]}),
            ("talk:the_desk", {}),
        ):
            for i in pump.only(pump.run(road, answering(**state)), "task_done"):
                ticked.add(i["id"])
        self.assertEqual(declared, ticked,
                         "a row nobody can tick is an island nobody can finish")

    def test_a_row_is_ticked_when_it_is_true_and_not_on_the_way_in(self):
        seen = pump.run("talk:host", answering())
        kinds = pump.kinds(seen)
        # he has spoken before meeting him counts
        self.assertLess(kinds.index("say"), kinds.index("task_done"))


class TheScreen(unittest.TestCase):
    """The camera goes into the monitor and has to come back out of it."""

    def setUp(self):
        pump.load(ISLAND)

    def test_the_camera_comes_back_when_the_screen_is_played(self):
        seen = pump.run("talk:the_desk", answering())
        shots = [i.get("shot") for i in pump.only(seen, "framing")]
        self.assertEqual(shots, ["the_screen", None])

    def test_the_camera_comes_back_even_when_the_screen_refuses(self):
        """The shot and the objective come back even when `play` refuses.

        Wrap the framing in try/finally so a bad question cannot strand the camera.
        """
        trail = []
        run = dict(pump.FRESH_RUN)
        run["year"] = 1

        def answer(intent):
            trail.append(intent)
            if intent["kind"] == "play":
                raise pump.Refused("that step names an instruction the list does not have")
            if intent["kind"] == "get":
                return run[intent["path"]]
            if intent["kind"] == "choose":
                return 0
            return None

        with self.assertRaises(Exception):
            pump.run("talk:the_desk", answer)
        shots = [i.get("shot") for i in trail if i["kind"] == "framing"]
        lines = [i.get("text") for i in trail if i["kind"] == "objective"]
        self.assertIn(None, shots, "the shot was left up when play refused")
        self.assertIn(None, lines, "the panel was left saying fix the program")

    def test_declining_hands_the_panel_back(self):
        """Declining the machine clears the objective and plays nothing."""
        seen = pump.run("talk:the_desk", answering(choices=[1]))
        lines = [i.get("text") for i in pump.only(seen, "objective")]
        self.assertIn(None, lines)
        self.assertEqual(pump.only(seen, "play"), [])


class TheYear(unittest.TestCase):
    """A club is taken again in a later year, so the island has to be finishable twice."""

    def setUp(self):
        pump.load(ISLAND)

    def test_the_done_flag_carries_the_year(self):
        seen = pump.run("talk:the_desk", answering(year=2))
        flags = [i["flag"] for i in pump.only(seen, "set_flag")]
        self.assertTrue(any(f.endswith(":y2") or f == "built:y2" for f in flags),
                        "the flag has to carry the year or the club can only ever be done once")

    def test_a_year_with_the_club_done_asks_for_nothing(self):
        seen = pump.run("start", answering(year=1, flags=["built:y1"]))
        self.assertEqual(pump.only(seen, "guide_to"), [])
        # and the list still goes up, so the sheet can say it is finished
        self.assertEqual(len(pump.only(seen, "island_tasks")), 1)


if __name__ == "__main__":
    unittest.main()
