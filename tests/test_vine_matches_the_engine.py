"""The vendored vine.py has not drifted from the engine's.

`vine.py` at the root of this repo is a copy. The real one lives in the game and
gets written into the runtime over the top of it, so at runtime the engine always
wins. That sounds safe and it is not: a member writing `say(text, portrait=...)`
against a copy the engine does not have gets a green test here and a TypeError in
the game, on a line that looks correct.

That already happened once, on `say`, in the first commit of this repo.

So this reads the engine's file when it is on the same machine and compares the
signature of every word we ship. On a member's laptop the game repo is not there,
and the test says so out loud rather than passing quietly, because a skip nobody
sees is the same as no test.

Point it somewhere else with BLHS_GAME if your checkout is not next door.
"""
import os
import re
import unittest

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GAME = os.environ.get("BLHS_GAME") or os.path.join(os.path.dirname(HERE), "AdventureGame")
ENGINE_VINE = os.path.join(GAME, "src", "vine", "py", "vine.py")

# every word this repo hands members. The engine has more; those are not ours to
# have an opinion about, and a member's first copy does not use one.
OURS = ("say", "choose", "open", "play", "get", "set_flag", "award", "log", "guide_to")


def signatures(source):
    """{name: the whole def line} for every top-level def."""
    return {m.group(1): m.group(0).strip()
            for m in re.finditer(r"^def (\w+)\(.*?\):", source, re.M | re.S)}


class TheCopyAgrees(unittest.TestCase):
    def setUp(self):
        if not os.path.isfile(ENGINE_VINE):
            self.skipTest(
                "no game checkout at %s, so drift cannot be checked here. This is "
                "expected on a member's machine and is not expected on Ash's. Set "
                "BLHS_GAME if yours is somewhere else." % ENGINE_VINE)
        with open(ENGINE_VINE, encoding="utf-8") as f:
            self.engine = signatures(f.read())
        with open(os.path.join(HERE, "vine.py"), encoding="utf-8") as f:
            self.ours = signatures(f.read())

    def test_we_ship_the_nine_and_nothing_else(self):
        self.assertEqual(sorted(self.ours), sorted(OURS))

    def test_the_engine_still_has_all_nine(self):
        # a word disappearing from the engine is the other direction of the same
        # bug, and it turns a member's island into a NameError on import
        missing = [w for w in OURS if w not in self.engine]
        self.assertEqual(missing, [])

    def test_every_signature_is_the_engine_s_signature(self):
        for word in OURS:
            if word in self.engine:
                with self.subTest(word=word):
                    self.assertEqual(self.ours[word], self.engine[word])


if __name__ == "__main__":
    unittest.main()
