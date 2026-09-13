"""THE ALGORITHMIC THINKING CLUB, which is the island a member copies.

The Maw is the complicated example and the hub is the opening. This one is the
TEMPLATE, so a mistake in here is a mistake every member inherits, and the things
worth testing are the ones a beginner will actually get wrong: a task that can never
be ticked, a camera left pointing at a desk, a sentence left on the glass.
"""
import unittest

try:
    from tests import pump
except ImportError:
    import pump

ISLAND = "atc"


def answering(refuse=(), **state):
    """The shared run state, and one thing about flags worth knowing.

    A MEMBER'S ISLAND LIVES IN ITS OWN CORNER OF THE FLAGS. The engine puts your
    programme id in front of everything you write, and takes it back off everything you
    read, so an island that says `set_flag("met")` finds `"met"` in `get("flags")` while
    the save holds `"atc:met"`. That is why this island's own done-flag is spelled
    `built:y1` with no `atc:` on it.

    The vine's own two islands, the hub and the Maw, run UNSCOPED, which is why their
    code spells `maw:railed` in full. Yours does not work that way.

    So the flags handed to a test here are the ones your island RECEIVES, without the
    prefix, because that is what the engine would have given it.
    """
    return pump.answering(refuse=refuse, **state)


class TheIslandLoads(unittest.TestCase):
    def setUp(self):
        self.manifest = pump.load(ISLAND)

    def test_it_claims_the_three_things_a_student_can_press(self):
        got = set(pump.handlers())
        self.assertIn("start", got)
        for who in ("talk:host", "talk:the_desk", "talk:trophies"):
            self.assertIn(who, got)


class TheTaskList(unittest.TestCase):
    """What the island says it is asking for, and when the rows tick.

    Ash asked for islands to always have tasks to do and for finishing them to be
    what finishing the island means, so a row that cannot be reached is the island
    being unfinishable, not a cosmetic slip.
    """

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
        """THE ONE THAT MADE THE ISLAND UNFINISHABLE.

        The machine can be pressed without ever speaking to the president, so a
        student who walks up to the lit computer first finishes the program and then
        finds him afterwards. "meet" used to be ticked in only one branch, and that
        branch is unreachable once the club is done, so the island sat at one of two
        for the rest of the year and the way home never appeared.
        """
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
        """THE TYPO A MEMBER WILL MAKE.

        `play` refuses rather than returning when a question will not validate: a step
        naming an instruction that is not in the list, two questions sharing an id, a
        misspelt kind. Without a try/finally round the shot, that typo left a student at
        eight times zoom staring at a desk with the controls back in his hands and "Fix
        the program." across the top, which reads as the game breaking rather than as
        somebody's mistake.
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
        """A student who is walked to the machine and says not right now is standing in
        front of it, so "Follow him to the machine." is a sentence about a thing he has
        just declined to do. It used to stay on the glass for the rest of the year."""
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
