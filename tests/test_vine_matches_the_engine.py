"""The vendored vine.py and grape.py have not drifted from the engine's.

Both files at the root of this repo are copies of the engine's. The game writes
its own into the runtime over the top of them, so at runtime the engine always
wins and a stale copy here cannot reach a player. What it CAN do is waste an
afternoon: a member writes `say(text, portrait=...)` against a copy that has an
argument the engine does not, the test here goes green, and the game raises a
TypeError on a line that looks correct. That happened, on `say`, in this repo's
first commit.

So both are compared BYTE FOR BYTE. Not a subset and not a signature match: there
is one of each file and no reason for two, `python tools/sync.py` makes them the
same, and this fails on a comment as readily as on a rule.

THE NINE-WORD FENCE IS NOT HERE. vine.py carries all fifteen of the engine's
words, because a member's editor should see what the engine actually has. What is
fenced to nine is the STARTER SKELETON, so a member's first copy never contains a
word that comes back as a refusal on their own line, and that fence lives in
test_skeleton.py where the skeleton is.

On a member's laptop the game repo is not there, and these say so out loud rather
than passing quietly, because a skip nobody sees is the same as no test.

Point it somewhere else with BLHS_GAME if your checkout is not next door.
"""
import os
import re
import unittest

from tools import manifest

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GAME = os.environ.get("BLHS_GAME") or os.path.join(os.path.dirname(HERE), "AdventureGame")
ENGINE_PY = os.path.join(GAME, "src", "vine", "py")

# every file this repo vendors out of the engine
VENDORED = ("vine.py", "grape.py")


class TheCopiesAreTheSameFiles(unittest.TestCase):
    def test_byte_for_byte(self):
        for name in VENDORED:
            theirs = os.path.join(ENGINE_PY, name)
            if not os.path.isfile(theirs):
                self.skipTest(
                    "no game checkout at %s. Expected on a member's machine, not on "
                    "Ash's. Set BLHS_GAME if yours is somewhere else." % ENGINE_PY)
            with self.subTest(file=name):
                with open(theirs, encoding="utf-8") as f:
                    engine = f.read()
                with open(os.path.join(HERE, name), encoding="utf-8") as f:
                    ours = f.read()
                self.assertEqual(
                    ours, engine,
                    "%s has drifted from the engine's copy. Run: python tools/sync.py" % name)


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


if __name__ == "__main__":
    unittest.main()
