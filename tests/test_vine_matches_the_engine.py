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
# and the one that goes the other way: the roster rows a member's PR adds here,
# which tools/sync.py carries into the engine when Ash merges
CROSSES = (("islands.json", os.path.join("src", "game", "roster", "member-islands.json")),)

# THE ISLANDS THE VINE WROTE, whole folders, and the engine's copy is the master.
#
# The Panther's Maw is the game's own home base written in the same python a
# member writes. It ships out of the engine's `public/grapes/`, because that is
# where a bound island is fetched from, and it is HERE because it is the advanced
# example somebody reads to understand the machine. Two copies of a four file
# island drift faster than two copies of one file, and a drifted copy here is a
# member learning from a version of the room that is not the one they play.
VENDORED_ISLANDS = (("panther-maw", os.path.join("public", "grapes", "panther-maw")),)


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


class TheVinesOwnIslandsAreTheSameFolders(unittest.TestCase):
    """Every file, both ways, so neither a stale edit nor a stray module hides.

    Comparing the files the engine has is only half of it. A module left behind
    HERE after the engine deleted it is a `.py` on disk that no manifest lists,
    which `tools/manifest.py` refuses, and the member reading the error wrote
    none of it.
    """

    def test_every_file_is_the_same_file(self):
        for folder, theirs_rel in VENDORED_ISLANDS:
            theirs = os.path.join(GAME, theirs_rel)
            if not os.path.isdir(theirs):
                self.skipTest("no game checkout at %s" % theirs)
            ours = os.path.join(HERE, "islands", folder)
            engine_files = sorted(n for n in os.listdir(theirs)
                                  if os.path.isfile(os.path.join(theirs, n)))
            our_files = sorted(n for n in os.listdir(ours)
                               if os.path.isfile(os.path.join(ours, n)))
            self.assertEqual(
                our_files, engine_files,
                "islands/%s does not hold the same files as the engine's. "
                "Run: python tools/sync.py" % folder)
            for name in engine_files:
                with self.subTest(island=folder, file=name):
                    with open(os.path.join(theirs, name), encoding="utf-8") as f:
                        engine = f.read()
                    with open(os.path.join(ours, name), encoding="utf-8") as f:
                        mine = f.read()
                    self.assertEqual(
                        mine, engine,
                        "islands/%s/%s has drifted from the engine's copy. "
                        "Run: python tools/sync.py" % (folder, name))


class TheRosterRowsCrossed(unittest.TestCase):
    """islands.json here and member-islands.json in the engine are one file.

    A member's pull request adds a row HERE, because this is the repository a
    member opens. The engine reads its own copy at boot rather than asking GitHub
    for a roster on a school network with a bad afternoon, so the row has to
    cross, and `python tools/sync.py` is the crossing. An unsynced merge is an
    island the member can see and the game cannot.
    """

    def test_the_engine_has_the_same_rows(self):
        for ours_name, theirs_rel in CROSSES:
            theirs = os.path.join(GAME, theirs_rel)
            if not os.path.isfile(theirs):
                self.skipTest("no game checkout at %s" % GAME)
            with self.subTest(file=ours_name):
                with open(theirs, encoding="utf-8") as f:
                    engine = f.read()
                with open(os.path.join(HERE, ours_name), encoding="utf-8") as f:
                    ours = f.read()
                self.assertEqual(
                    ours, engine,
                    "%s has not been carried into the engine. Run: python tools/sync.py"
                    % ours_name)


class TheRegistryMatchesTheFolders(unittest.TestCase):
    def test_every_row_names_a_folder_that_exists(self):
        self.assertEqual(manifest.registry_faults(), [])


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
