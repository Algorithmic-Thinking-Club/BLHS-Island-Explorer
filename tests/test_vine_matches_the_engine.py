"""Checks this repo's copies of the engine's python have not drifted.

vine.py, grape.py, the vendored islands and islands.json are compared byte for
byte with the game checkout next door. Run `python tools/sync.py` to fix a
failure, and set BLHS_GAME if your game checkout is not in a sibling folder.
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
# the roster rows that cross the other way, from here into the engine
CROSSES = (("islands.json", os.path.join("src", "game", "roster", "member-islands.json")),)

# whole island folders vendored from the engine, which keeps the master copy
VENDORED_ISLANDS = (
    ("panther-maw", os.path.join("public", "grapes", "panther-maw")),
    ("castaway", os.path.join("public", "grapes", "castaway")),
    ("the-hub", os.path.join("public", "grapes", "the-hub")),
)


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
    """Compares every file both ways, so a module left behind here shows up too."""

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
    """islands.json here and member-islands.json in the engine hold the same rows."""

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
    """tools/manifest.py and the engine's grape-source.ts hold the same format rules."""

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


class TheAskablePathsAreTheSameList(unittest.TestCase):
    """The paths get() documents, the engine answers and the pump serves are one list."""

    def setUp(self):
        try:
            from tests import pump
        except ImportError:
            import pump
        self.pump = pump
        engine = os.path.join(GAME, "src", "game", "intent-engine.ts")
        if not os.path.exists(engine):
            self.skipTest("the engine repo is not next door, so there is nothing to cross")
        with open(engine, encoding="utf-8") as f:
            self.ts = f.read()

    def test_the_engine_answers_exactly_what_get_documents(self):
        m = re.search(r"const READABLE_PATHS: Record<RunPath, true> = \{(.*?)\}", self.ts, re.S)
        self.assertIsNotNone(m, "intent-engine.ts has no READABLE_PATHS table to cross")
        theirs = set(re.findall(r"([a-z_]{2,20}): true", m.group(1)))
        self.assertEqual(theirs, self.pump.askable())

    def test_the_pump_holds_a_value_for_every_path(self):
        self.assertEqual(set(self.pump.FRESH_RUN), self.pump.askable())


if __name__ == "__main__":
    unittest.main()
