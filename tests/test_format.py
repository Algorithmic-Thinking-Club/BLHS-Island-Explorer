"""Every island in this repo is loadable, and the rules that decide that hold.

Three parts. The first walks the repo and refuses to let a broken island sit in
it. The second actually imports every island, because a manifest can be perfect
about a file that does not parse. The third builds deliberately broken manifests
in a scratch folder and checks each one is caught, since a validator nobody has
ever seen say no is a validator that might only ever say yes.
"""
import json
import os
import shutil
import tempfile
import unittest

from tests import pump
from tools import manifest


class EveryIslandInTheRepo(unittest.TestCase):
    def test_there_is_at_least_one(self):
        self.assertTrue(manifest.islands(), "islands/ is empty")

    def test_each_one_is_loadable(self):
        for folder in manifest.islands():
            with self.subTest(island=os.path.basename(folder)):
                self.assertEqual(manifest.faults(folder), [])

    def test_no_two_claim_the_same_id(self):
        self.assertEqual(manifest.collisions(), [])

    def test_each_one_actually_imports(self):
        # A CORRECT MANIFEST ABOUT A FILE THAT DOES NOT PARSE passes everything
        # above. So does one whose island.py imports a module it does not ship.
        # Both of those are green manifests and dead islands, and importing is
        # the only thing that tells them apart.
        for folder in manifest.islands():
            island = os.path.basename(folder)
            with self.subTest(island=island):
                pump.load(island)
                self.assertTrue(pump.handlers(),
                                "%s registered no handlers, so the game can never "
                                "call into it" % island)

    def test_every_handler_in_every_island_is_a_generator(self):
        # THE FORGOTTEN YIELD, CAUGHT FOR EVERYBODY. A member who never copies
        # the skeleton's own tests still gets this one, because it walks the
        # repo. A handler with no yield in it does nothing and says nothing.
        import inspect
        import grape
        for folder in manifest.islands():
            island = os.path.basename(folder)
            pump.load(island)
            for key, fn in sorted(grape._handlers.items()):
                with self.subTest(island=island, handler=key):
                    self.assertTrue(
                        inspect.isgeneratorfunction(fn),
                        "%s in %s has no yield in it, so nothing it does would ever "
                        "reach the engine" % (getattr(fn, "__name__", key), island))


class TheRulesActuallyRefuse(unittest.TestCase):
    """Each test breaks one thing and checks the complaint names that field."""

    GOOD = {
        "format": 1,
        "programme": "test-club",
        "map": "test-shore",
        "title": "A Test",
        "season": "Winter",
        "owner": "atc",
        "entry": "island.py",
        "modules": ["island.py"],
        "content": {
            "what": {"text": "A thing that does not exist.", "source": "unknown"},
            "when": {"text": "Never.", "source": "unknown"},
            "how_to_join": {"text": "You cannot.", "source": "unknown"},
            "blurb": "a fixture for tests",
        },
    }
    GONE = object()          # sentinel: leave this field out entirely

    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.folder = os.path.join(self.dir, "test-island")
        os.makedirs(self.folder)
        self.addCleanup(shutil.rmtree, self.dir)

    def write(self, folder=None, **changes):
        m = dict(self.GOOD)
        for key, value in changes.items():
            if value is self.GONE:
                m.pop(key, None)
            else:
                m[key] = value
        where = folder or self.folder
        with open(os.path.join(where, "island.json"), "w", encoding="utf-8") as f:
            json.dump(m, f)
        return manifest.faults(where)

    def touch(self, *names, **kw):
        where = kw.get("folder") or self.folder
        for n in names:
            with open(os.path.join(where, n), "w", encoding="utf-8") as f:
                f.write("# a module\n")

    def only(self, problems):
        self.assertEqual(len(problems), 1, problems)
        return problems[0]

    # ---- the shape of the file ----------------------------------------------

    def test_a_correct_one_passes(self):
        self.touch("island.py")
        self.assertEqual(self.write(), [])

    def test_no_island_json_at_all(self):
        self.assertIn("island.json", self.only(manifest.faults(self.folder)))

    def test_unreadable_json(self):
        with open(os.path.join(self.folder, "island.json"), "w", encoding="utf-8") as f:
            f.write("{ not json")
        self.assertIn("not valid JSON", self.only(manifest.faults(self.folder)))

    def test_json_that_is_not_an_object(self):
        with open(os.path.join(self.folder, "island.json"), "w", encoding="utf-8") as f:
            f.write("[1, 2, 3]")
        self.assertIn("has to be an object", self.only(manifest.faults(self.folder)))

    def test_a_byte_order_mark_is_read_rather_than_refused(self):
        # every Windows editor will put one there, and it is not the member's bug
        self.touch("island.py")
        with open(os.path.join(self.folder, "island.json"), "w", encoding="utf-8-sig") as f:
            json.dump(self.GOOD, f)
        self.assertEqual(manifest.faults(self.folder), [])

    def test_a_folder_name_that_is_not_a_slug(self):
        shouted = os.path.join(self.dir, "Test_Island")
        os.makedirs(shouted)
        self.touch("island.py", folder=shouted)
        problems = self.write(folder=shouted)
        self.assertTrue(any("folder name" in p for p in problems), problems)

    def test_the_content_section_is_required(self):
        # P18. The half a builder skips, so it gets skipped out loud.
        self.touch("island.py")
        self.assertIn("`content`", self.only(self.write(content=self.GONE)))

    def test_a_fact_with_no_source_is_refused_and_unknown_is_not(self):
        self.touch("island.py")
        bare = dict(self.GOOD["content"])
        bare["what"] = {"text": "BLHS opened in 2005."}
        self.assertIn("content.what.source", self.only(self.write(content=bare)))
        # "unknown" is a decision a member made, and it passes
        said = dict(self.GOOD["content"])
        said["what"] = {"text": "Nobody has published this.", "source": "unknown"}
        self.assertEqual(self.write(content=said), [])

    def test_a_blurb_that_is_a_paragraph(self):
        self.touch("island.py")
        long = dict(self.GOOD["content"])
        long["blurb"] = "one two three four five six seven eight"
        self.assertIn("content.blurb", self.only(self.write(content=long)))

    def test_a_meeting_time_nobody_sourced(self):
        self.touch("island.py")
        meets = dict(self.GOOD["content"])
        meets["meets"] = [{"day": "Tuesday", "time": "2:10", "room": "200 Flex"}]
        self.assertIn("meets[0].source", self.only(self.write(content=meets)))

    def test_a_missing_field_is_named(self):
        self.touch("island.py")
        self.assertIn("`owner`", self.only(self.write(owner=self.GONE)))

    def test_a_field_nobody_has_heard_of_is_named(self):
        # a typo in a key is otherwise completely silent: the value is simply
        # never read and the island behaves as though it was never written
        self.touch("island.py")
        self.assertIn("`sesaon`", self.only(self.write(sesaon="Fall")))

    # ---- the version --------------------------------------------------------

    def test_a_future_format_is_refused_by_number(self):
        self.touch("island.py")
        self.assertIn("format 1", self.only(self.write(format=2)))

    def test_a_format_that_is_not_a_number_at_all(self):
        # True == 1 in Python, so a boolean sails through a bare `!= 1` and then
        # fails on the engine's `=== 1`, which is the one place nobody is looking
        self.touch("island.py")
        for value in (True, 1.0, "1", None):
            with self.subTest(format=value):
                self.assertIn("`format`", self.only(self.write(format=value)))

    # ---- the ids ------------------------------------------------------------

    def test_programme_and_map_may_not_be_the_same_id(self):
        self.touch("island.py")
        self.assertIn("different key spaces", self.only(self.write(map="test-club")))

    def test_a_shouted_id_is_not_a_slug(self):
        self.touch("island.py")
        self.assertIn("`programme`", self.only(self.write(programme="TestClub")))

    def test_an_underscored_id_is_not_a_slug(self):
        self.touch("island.py")
        self.assertIn("`programme`", self.only(self.write(programme="test_club")))

    def test_a_double_hyphen_is_not_a_slug(self):
        self.touch("island.py")
        self.assertIn("`programme`", self.only(self.write(programme="test--club")))

    # ---- what a person reads ------------------------------------------------

    def test_a_blank_owner(self):
        self.touch("island.py")
        self.assertIn("`owner`", self.only(self.write(owner="   ")))

    def test_a_title_with_a_line_break_in_it(self):
        self.touch("island.py")
        self.assertIn("`title`", self.only(self.write(title="Line one\nLine two")))

    def test_a_title_nobody_can_fit_on_screen(self):
        self.touch("island.py")
        self.assertIn("`title`", self.only(self.write(title="T" * 200)))

    def test_a_season_outside_the_vocabulary(self):
        self.touch("island.py")
        self.assertIn("`season`", self.only(self.write(season="Summer")))

    def test_no_season_at_all_is_allowed(self):
        self.touch("island.py")
        self.assertEqual(self.write(season=self.GONE), [])

    # ---- the modules --------------------------------------------------------

    def test_a_module_that_is_not_there(self):
        self.touch("island.py")
        problems = self.write(modules=["island.py", "questions.py"])
        self.assertIn("questions.py", self.only(problems))

    def test_a_file_on_disk_that_nobody_listed(self):
        # the one that only breaks inside the game, which is the worst place
        self.touch("island.py", "questions.py")
        self.assertIn("never fetches it", self.only(self.write()))

    def test_a_subfolder_inside_an_island(self):
        # re-running the copy command nests a whole island inside another one,
        # and every file in it is unfetchable and invisible
        self.touch("island.py")
        os.makedirs(os.path.join(self.folder, "content"))
        self.assertIn("one flat folder", self.only(self.write()))

    def test_an_entry_outside_the_modules(self):
        self.touch("island.py")
        self.assertIn("`entry`", self.only(self.write(entry="main.py")))

    def test_a_module_with_a_path_in_it(self):
        self.touch("island.py")
        problems = self.write(modules=["island.py", "sub/thing.py"])
        self.assertIn("one flat folder", problems[0])

    def test_the_same_file_listed_twice(self):
        self.touch("island.py")
        problems = self.write(modules=["island.py", "island.py"])
        self.assertTrue(any("twice" in p for p in problems), problems)

    def test_a_filename_python_cannot_import(self):
        self.touch("island.py", "my.island.py")
        problems = self.write(modules=["island.py", "my.island.py"])
        self.assertTrue(any("after `import`" in p for p in problems), problems)

    def test_a_shouted_extension(self):
        # imports fine on Windows, 404s on GitHub, which is where it is fetched
        self.touch("island.py", "Questions.PY")
        problems = self.write(modules=["island.py", "Questions.PY"])
        self.assertTrue(any("case-sensitive" in p or "after `import`" in p
                            for p in problems), problems)

    def test_a_module_named_after_one_python_already_has(self):
        self.touch("island.py", "random.py")
        problems = self.write(modules=["island.py", "random.py"])
        self.assertTrue(any("already uses" in p for p in problems), problems)

    def test_shipping_the_engines_own_module(self):
        self.touch("island.py", "vine.py")
        problems = self.write(modules=["island.py", "vine.py"])
        self.assertTrue(any("the game provides" in p for p in problems), problems)


class TwoIslandsInOneRepo(unittest.TestCase):
    """collisions() had no test at all, so gutting it left the suite green."""

    def setUp(self):
        self.repo = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.repo)

    def island(self, name, programme, map_id):
        folder = os.path.join(self.repo, "islands", name)
        os.makedirs(folder)
        with open(os.path.join(folder, "island.json"), "w", encoding="utf-8") as f:
            json.dump({"format": 1, "programme": programme, "map": map_id,
                       "title": name, "owner": "atc", "entry": "island.py",
                       "modules": ["island.py"],
                       "content": {
                           "what": {"text": "x", "source": "unknown"},
                           "when": {"text": "x", "source": "unknown"},
                           "how_to_join": {"text": "x", "source": "unknown"},
                           "blurb": "a b c d",
                       }}, f)
        return folder

    def test_two_islands_that_do_not_clash(self):
        self.island("a", "chess", "chess-room")
        self.island("b", "pep", "gym")
        self.assertEqual(manifest.collisions(self.repo), [])

    def test_the_same_programme_twice(self):
        self.island("a", "chess", "chess-room")
        self.island("b", "chess", "gym")
        self.assertTrue(manifest.collisions(self.repo))

    def test_one_islands_programme_is_anothers_map(self):
        # ONE key space to the roster, so this is as broken as the case above and
        # a per-field check would have called it fine
        self.island("a", "chess", "chess-room")
        self.island("b", "pep", "chess")
        self.assertTrue(manifest.collisions(self.repo))

    def test_a_broken_manifest_does_not_take_the_sweep_down_with_it(self):
        self.island("a", "chess", "chess-room")
        bad = os.path.join(self.repo, "islands", "b")
        os.makedirs(bad)
        with open(os.path.join(bad, "island.json"), "w", encoding="utf-8") as f:
            f.write("[]")
        self.assertEqual(manifest.collisions(self.repo), [])


if __name__ == "__main__":
    unittest.main()
