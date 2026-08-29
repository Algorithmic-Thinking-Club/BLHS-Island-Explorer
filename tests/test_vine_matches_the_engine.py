"""The vendored vine.py and grape.py have not drifted from the engine's.

Both files at the root of this repo are copies. The real ones live in the game
and get written into the runtime over the top of them, so at runtime the engine
always wins. That sounds safe and it is not: a member writing
`say(text, portrait=...)` against a copy the engine does not have gets a green
test here and a TypeError in the game, on a line that looks correct.

That already happened once, on `say`, in the first commit of this repo.

So this reads the engine's files when they are on the same machine. `grape.py`
has to be byte for byte the same file, because there is one of it and no reason
for two. `vine.py` is a subset by design, nine of the engine's fifteen words, so
what is compared there is every signature we ship.

On a member's laptop the game repo is not there, and the test says so out loud
rather than passing quietly, because a skip nobody sees is the same as no test.

Point it somewhere else with BLHS_GAME if your checkout is not next door.
"""
import os
import re
import unittest

from tools import manifest

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GAME = os.environ.get("BLHS_GAME") or os.path.join(os.path.dirname(HERE), "AdventureGame")
ENGINE_PY = os.path.join(GAME, "src", "vine", "py")
ENGINE_VINE = os.path.join(ENGINE_PY, "vine.py")
ENGINE_GRAPE = os.path.join(ENGINE_PY, "grape.py")

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


class TheFormatRulesAgree(unittest.TestCase):
    """The two checkers hold the same lists, or a member gets caught by one only.

    `tools/manifest.py` and the engine's `grape-source.ts` implement one package
    format twice, on purpose: a member gets the answer on their own laptop in a
    second instead of in a browser a minute later. That trade is only worth
    anything while the two agree, and within a day of being written the reserved
    name lists had drifted by four names. `test.py` failed here and loaded there;
    `inspect.py` and `driver.py` passed here and were refused there.

    So the constants are compared rather than trusted.
    """

    SOURCE = os.path.join(ENGINE_PY, "grape-source.ts")

    def setUp(self):
        if not os.path.isfile(self.SOURCE):
            self.skipTest("no game checkout at %s" % self.SOURCE)
        with open(self.SOURCE, encoding="utf-8") as f:
            self.ts = f.read()

    def strings(self, block):
        """every 'quoted' name inside a named const's braces or brackets"""
        m = re.search(r"(?:const|export const)\s+%s\s*=\s*(?:new Set\()?\[(.*?)\]" % block,
                      self.ts, re.S)
        self.assertIsNotNone(m, "no %s in grape-source.ts" % block)
        return sorted(re.findall(r"'([^']+)'", m.group(1)))

    def number(self, name):
        m = re.search(r"(?:const|export const)\s+%s\s*=\s*([\d_ *]+)" % name, self.ts)
        self.assertIsNotNone(m, "no %s in grape-source.ts" % name)
        return eval(m.group(1).replace("_", ""))       # noqa: S307 - our own source

    def test_the_reserved_names_are_the_same_list(self):
        self.assertEqual(self.strings("TAKEN"), sorted(manifest.TAKEN))

    def test_the_engine_owned_names_are_the_same_list(self):
        self.assertEqual(self.strings("ENGINE_OWNED"), sorted(manifest.ENGINE_OWNED))

    def test_the_seasons_are_the_same_list(self):
        self.assertEqual(self.strings("SEASONS"), sorted(manifest.SEASONS))

    def test_the_numbers_are_the_same_numbers(self):
        self.assertEqual(self.number("FORMAT"), manifest.FORMAT)
        self.assertEqual(self.number("TEXT_MAX"), manifest.TEXT_MAX)
        self.assertEqual(self.number("MAX_MODULES"), manifest.MAX_MODULES)


class GrapeIsTheSameFile(unittest.TestCase):
    """Not a subset and not a signature match. The same bytes.

    vine.py is deliberately nine of fifteen words. grape.py has no reason to
    differ at all, so the cheapest correct check is the strictest one, and it
    fails on a comment as readily as on a rule.
    """

    def test_byte_for_byte(self):
        if not os.path.isfile(ENGINE_GRAPE):
            self.skipTest(
                "no game checkout at %s. Expected on a member's machine, not on "
                "Ash's. Set BLHS_GAME if yours is somewhere else." % ENGINE_GRAPE)
        with open(ENGINE_GRAPE, encoding="utf-8") as f:
            theirs = f.read()
        with open(os.path.join(HERE, "grape.py"), encoding="utf-8") as f:
            ours = f.read()
        self.assertEqual(ours, theirs, "grape.py has drifted from the engine's copy")


if __name__ == "__main__":
    unittest.main()
