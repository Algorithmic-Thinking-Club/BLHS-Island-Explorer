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


def answering(flags=(), refuse=()):
    """An engine that answers the two questions this island asks."""
    state = {"flags": list(flags)}

    def answer(intent):
        if intent["kind"] in refuse:
            raise pump.Refused("%s: this map cannot do that" % intent["kind"])
        if intent["kind"] == "get":
            return state[intent["path"]]
        return None
    return answer


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
        # up once at the first frame and down once at the tunnel, and never in
        # between: the two seams in the middle were the glitches Ash watched
        movies = [i["on"] for i in pump.only(pump.run("start", answering()), "movie")]
        self.assertEqual(movies, [True, False])

    def test_the_crossing_is_close_and_the_pull_out_comes_after_it(self):
        """Ash's second order: close on the ship, then the dock, then wide."""
        seen = pump.run("start", answering())
        kinds = pump.kinds(seen)
        views = pump.only(seen, "view")
        self.assertEqual([v["view"] for v in views], ["ship", "island", "close"])
        # the ship shot is asked for before she moves, and the wide one after
        self.assertLess(kinds.index("view"), kinds.index("route"))
        self.assertLess(kinds.index("route"), kinds.index("view", kinds.index("route")))

    def test_the_card_plays_at_the_wide_shot_and_he_hops_out_after_it(self):
        kinds = pump.kinds(pump.run("start", answering()))
        wide = kinds.index("view", kinds.index("route"))
        self.assertLess(wide, kinds.index("ashore"))
        # and the bars are still up over it: there is only one `movie` before
        # the walk and it is the one that raised them
        self.assertEqual(kinds.index("movie"), kinds.index("movie"))
        self.assertLess(wide, kinds.index("movie", wide))

    def test_the_camera_moves_once_from_the_island_to_him(self):
        """Ash watched a two step shift: full island, half island, then Thor."""
        kinds = pump.kinds(pump.run("start", answering()))
        after = kinds.index("ashore")
        # exactly one shot is asked for between stepping off and walking
        views = [i for i, k in enumerate(kinds) if k == "view" and after < i < kinds.index("walk_to")]
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

    def test_the_walk_is_watched_and_the_frame_comes_off_at_the_door(self):
        seen = pump.run("start", answering())
        kinds = pump.kinds(seen)
        walk = kinds.index("walk_to")
        movies = [i for i, k in enumerate(kinds) if k == "movie"]
        # raised before anything moves, and lowered only after the walk: the bars
        # are up over every frame in between
        self.assertEqual(len(movies), 2)
        self.assertLess(movies[0], kinds.index("route"))
        self.assertLess(walk, movies[1])

    def test_a_refused_crossing_still_takes_the_bars_down_and_still_walks(self):
        # the one that matters: bars raised, the boat refused, and a student left
        # behind two black bars with no controls would be a dead-looking laptop
        seen = pump.run("start", answering(refuse=("route",)))
        self.assertEqual([i["on"] for i in pump.only(seen, "movie")], [True, False])
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
