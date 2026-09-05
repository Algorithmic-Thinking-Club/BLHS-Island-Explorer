"""The hub does what it says: the crossing once, and three people on the way up.

BRIEF-YEAR-ONE beats 2 and 3, tested the way test_the_maw.py tests the room.
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

    def test_it_says_nothing_on_the_water(self):
        # the arrival card is the engine's and it is paid where he lands
        self.assertEqual(pump.only(pump.run("start", answering()), "say"), [])


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
