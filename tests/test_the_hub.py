"""The hub does what it says: the arrival as one piece, and three people on the way up.

BRIEF-ARRIVAL items 1 to 5, tested the way test_the_maw.py tests the room.
Nothing here performs anything; the island yields dicts and this file answers
them. What it can prove is the shape: the crossing is asked for exactly once
per run and its refusal is caught and logged rather than taking the island
down, and each of the three posts says one line in school words.
"""
import os
import re
import unittest

from tests import pump

ISLAND = "the-hub"

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _engine_words():
    with open(os.path.join(HERE, "vine.py"), encoding="utf-8") as f:
        return set(re.findall(r'"kind": "([a-z_]+)"', f.read()))


# ONE RUN STATE FOR EVERY TEST FILE, in pump. This one held only `flags`, so the
# day the island asked `year` all sixteen tests in here died with a KeyError at
# the fixture. Keeping a local copy is what let that happen.
answering = pump.answering


class TheIslandLoads(unittest.TestCase):
    def setUp(self):
        self.manifest = pump.load(ISLAND)

    def test_it_claims_the_three_dock_people_and_the_opening(self):
        # THE LIST IS EXACT. The three posts are the ones Ash is placing
        # (docs/ops/ARC-MANIFEST.md). Until the hub is republished with them the
        # engine says so by name at load and these simply never fire.
        self.assertEqual(pump.handlers(), [
            "start", "talk:dock_one", "talk:dock_three", "talk:dock_two",
        ])

    def test_it_does_not_claim_the_door(self):
        # a door is taken by the engine before it asks who owns the anchor
        self.assertNotIn("talk:panthers_maw", pump.handlers())

    def test_the_map_is_the_hub(self):
        self.assertEqual(self.manifest["map"], "hub")

    def test_the_programme_is_not_the_map(self):
        self.assertNotEqual(self.manifest["programme"], self.manifest["map"])


class TheCrossing(unittest.TestCase):
    def setUp(self):
        pump.load(ISLAND)

    def test_the_arrival_is_written_down_when_the_whole_piece_is_over(self):
        """AT THE TUNNEL AND NOWHERE EARLIER, which reverses what this file used
        to assert. Ash, 2026-09-07: the flag sat one line after the crossing on
        the argument that a crossing happens once, and the cost was a student who
        reloaded halfway up the quay getting the flag, no handler, no bars and the
        tiller in his hands on a boat already tied up. The arrival is the whole
        piece from the water to the door, so the piece being OVER is the thing
        written down, and a reload in the middle is a safe replay.
        """
        kinds = pump.kinds(pump.run("start", answering()))
        self.assertGreater(kinds.index("set_flag"), kinds.index("ashore"))
        self.assertGreater(kinds.index("set_flag"), kinds.index("walk_to"))
        # once, and only once, or a replay would write a second row
        self.assertEqual(kinds.count("set_flag"), 1)

    def test_the_ship_is_sent_along_the_sail_line_once(self):
        first = pump.run("start", answering())
        routes = pump.only(first, "route")
        self.assertEqual(len(routes), 1)
        self.assertEqual(routes[0]["path"], "the_hub_approach")
        self.assertEqual(routes[0]["who"], "ship")
        self.assertEqual([i["flag"] for i in pump.only(first, "set_flag")], ["hub:crossed"])

    def test_and_never_again(self):
        # walking back out of the mountain is not a sea arrival
        later = pump.run("start", answering(flags=["hub:crossed"]))
        self.assertEqual(pump.only(later, "route"), [])
        self.assertEqual(pump.only(later, "set_flag"), [])

    def test_a_hub_with_no_sail_line_yet_is_logged_and_not_a_crash(self):
        # the published hub carries no `the_hub_approach` today. The refusal is
        # raised on the island's own line; caught, it is written down with the
        # engine's sentence, and the flag is still set so the next load does not
        # put a student who just walked out of the mountain back on the water.
        seen = pump.run("start", answering(refuse=("route",)))
        logged = [i for i in pump.only(seen, "log") if i["event"] == "route_refused"]
        self.assertEqual(len(logged), 1)
        self.assertEqual(logged[0]["data"]["path"], "the_hub_approach")
        self.assertIn("route", logged[0]["data"]["why"])
        self.assertEqual([i["flag"] for i in pump.only(seen, "set_flag")], ["hub:crossed"])

    def test_it_says_nothing_until_she_is_tied_up(self):
        # the arrival card is the engine's and it is paid where he lands; the one
        # line this island says comes after the crossing, at the wide shot
        kinds = pump.kinds(pump.run("start", answering()))
        self.assertLess(kinds.index("route"), kinds.index("say"))


class TheArrivalIsOnePiece(unittest.TestCase):
    """BRIEF-ARRIVAL items 1 to 5, in Ash's order, as the shape of the yields.

    None of this proves it LOOKS right; nothing here draws anything. It proves
    the order, which is the half a test can hold: the bars go up before the ship
    moves, the island is framed before they come down, and nobody is asked to do
    anything until the card has had the screen.
    """

    def setUp(self):
        pump.load(ISLAND)

    def test_the_crossing_is_inside_the_bars(self):
        kinds = pump.kinds(pump.run("start", answering()))
        self.assertLess(kinds.index("movie"), kinds.index("route"))
        # up for the crossing, down at the dock, up again for the walk he is
        # being shown, and down when he is standing at the tunnel
        # raised once, at the first frame, and never lowered by this island at
        # all: the frame lasts the whole arrival and the door takes it with it
        movies = [i["on"] for i in pump.only(pump.run("start", answering()), "movie")]
        self.assertEqual(movies, [True])

    def test_the_crossing_is_close_and_the_pull_out_comes_after_it(self):
        """Ash's second order: close on the ship, then the dock, then wide."""
        seen = pump.run("start", answering())
        kinds = pump.kinds(seen)
        views = pump.only(seen, "view")
        self.assertEqual([v["view"] for v in views], ["ship", "island", "close"])
        # the ship shot is asked for before she moves, and the wide one after
        self.assertLess(kinds.index("view"), kinds.index("route"))
        self.assertLess(kinds.index("route"), kinds.index("view", kinds.index("route")))

    def test_he_steps_off_and_then_the_island_is_framed_over_the_card(self):
        """HE IS ASHORE FIRST AND THE WIDE SHOT COMES AFTER, which is also the
        reverse of what stood here. The card is not skipped: the engine's own
        ashore path suppresses it at the moment of stepping off and pays it on the
        island shot once the camera has settled, so the card still plays over the
        wide frame. What the old order would have meant is a wide shot of an
        island with nobody on it yet.
        """
        kinds = pump.kinds(pump.run("start", answering()))
        wide = kinds.index("view", kinds.index("route"))
        self.assertLess(kinds.index("ashore"), wide)
        # and the bars are still up over it: the only `movie` in the whole
        # handler is the one that raised them, before anything moved
        self.assertEqual(kinds.count("movie"), 1)
        self.assertLess(kinds.index("movie"), wide)

    def test_the_camera_moves_once_from_the_island_to_him(self):
        """Ash watched a two step shift: full island, half island, then Thor.

        MEASURED FROM THE WIDE SHOT AND NOT FROM STEPPING OFF. The window used to
        start at `ashore`, which now sits BEFORE the island shot, so it spanned
        two views by construction and could never hold. The thing it was written
        to catch is a second pull-in between seeing the island and following him,
        and that is exactly one shot, still.
        """
        kinds = pump.kinds(pump.run("start", answering()))
        wide = kinds.index("view", kinds.index("route"))
        views = [i for i, k in enumerate(kinds) if k == "view" and wide < i < kinds.index("walk_to")]
        self.assertEqual(len(views), 1)

    def test_the_line_nobody_could_say_is_said(self):
        seen = pump.run("start", answering())
        said = [i["text"] for i in pump.only(seen, "say")]
        self.assertIn("The principal is waiting for you up there.", said)

    def test_he_is_not_put_ashore_before_the_island_has_been_seen(self):
        seen = pump.run("start", answering())
        kinds = pump.kinds(seen)
        self.assertEqual(len(pump.only(seen, "ashore")), 1)
        self.assertLess(kinds.index("ashore"), kinds.index("walk_to"))

    def test_he_walks_to_the_door_and_the_way_is_drawn_first(self):
        seen = pump.run("start", answering())
        kinds = pump.kinds(seen)
        self.assertEqual([i["anchor"] for i in pump.only(seen, "guide_to")], ["panthers_maw"])
        self.assertEqual([i["anchor"] for i in pump.only(seen, "walk_to")], ["panthers_maw"])
        self.assertLess(kinds.index("guide_to"), kinds.index("walk_to"))

    def test_the_frame_is_raised_once_and_never_lowered_here(self):
        seen = pump.run("start", answering())
        kinds = pump.kinds(seen)
        movies = [i for i, k in enumerate(kinds) if k == "movie"]
        # one word, before anything moves, and nothing takes it down: the engine
        # hands the controls back when this handler ends and the door takes the
        # frame when he walks through it
        self.assertEqual(len(movies), 1)
        self.assertLess(movies[0], kinds.index("route"))
        self.assertLess(movies[0], kinds.index("walk_to"))

    def test_a_refused_crossing_still_takes_the_bars_down_and_still_walks(self):
        # the one that matters: bars raised, the boat refused, and a student left
        # behind two black bars with no controls would be a dead-looking laptop
        seen = pump.run("start", answering(refuse=("route",)))
        self.assertEqual([i["on"] for i in pump.only(seen, "movie")], [True])
        self.assertEqual([i["anchor"] for i in pump.only(seen, "walk_to")], ["panthers_maw"])

    def test_walking_back_out_of_the_mountain_raises_no_bars(self):
        later = pump.run("start", answering(flags=["hub:crossed"]))
        self.assertEqual(pump.only(later, "movie"), [])
        self.assertEqual(pump.only(later, "walk_to"), [])


class TheDock(unittest.TestCase):
    def setUp(self):
        pump.load(ISLAND)

    def test_each_person_says_one_line(self):
        for who in ("dock_one", "dock_two", "dock_three"):
            with self.subTest(who=who):
                seen = pump.run("talk:" + who, answering())
                said = pump.only(seen, "say")
                self.assertEqual(len(said), 1)
                self.assertEqual(said[0]["who"], who)

    def test_the_third_says_the_briefs_line_and_lights_the_door(self):
        seen = pump.run("talk:dock_three", answering())
        self.assertEqual(pump.only(seen, "say")[0]["text"],
                         "The principal is waiting for you up there.")
        self.assertEqual([i["anchor"] for i in pump.only(seen, "guide_to")], ["panthers_maw"])
        kinds = pump.kinds(seen)
        self.assertLess(kinds.index("say"), kinds.index("guide_to"))

    def test_every_line_is_short(self):
        # the literal-words law: one idea, about twelve words
        for who in ("dock_one", "dock_two", "dock_three"):
            for line in pump.only(pump.run("talk:" + who, answering()), "say"):
                self.assertLessEqual(len(line["text"].split()), 12, line["text"])


class EveryWordItUsesIsARealWord(unittest.TestCase):
    def setUp(self):
        pump.load(ISLAND)
        self.words = _engine_words()

    def test_no_branch_asks_for_a_word_the_engine_does_not_have(self):
        paths = [
            ("arrival", pump.run("start", answering())),
            ("arrival, refused", pump.run("start", answering(refuse=("route",)))),
            ("later", pump.run("start", answering(flags=["hub:crossed"]))),
        ] + [(who, pump.run("talk:" + who, answering()))
             for who in ("dock_one", "dock_two", "dock_three")]
        for label, seen in paths:
            with self.subTest(path=label):
                self.assertEqual(set(pump.kinds(seen)) - self.words, set())


if __name__ == "__main__":
    unittest.main()
