"""Every island in this repo is loadable, and the rules that decide that hold.

Two halves. The first walks the repo and refuses to let a broken island sit in
it. The second builds deliberately broken manifests in a scratch folder and
checks that each one is caught, because a validator nobody has ever seen say no
is a validator that might only ever say yes.
"""
import json
import os
import shutil
import tempfile
import unittest

from tools import manifest


class EveryIslandInTheRepo(unittest.TestCase):
    def test_there_is_at_least_one(self):
        self.assertTrue(manifest.islands(), "islands/ is empty")

    def test_each_one_is_loadable(self):
        for folder in manifest.islands():
            with self.subTest(island=os.path.basename(folder)):
                self.assertEqual(manifest.faults(folder), [])

    def test_no_two_claim_the_same_key(self):
        self.assertEqual(manifest.collisions(), [])


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
    }

    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.folder = os.path.join(self.dir, "test-island")
        os.makedirs(self.folder)
        self.addCleanup(shutil.rmtree, self.dir)

    def write(self, **changes):
        m = dict(self.GOOD)
        for key, value in changes.items():
            if value is manifest:      # sentinel: delete the field
                m.pop(key, None)
            else:
                m[key] = value
        with open(os.path.join(self.folder, "island.json"), "w", encoding="utf-8") as f:
            json.dump(m, f)
        return manifest.faults(self.folder)

    def touch(self, *names):
        for n in names:
            with open(os.path.join(self.folder, n), "w", encoding="utf-8") as f:
                f.write("# a module\n")

    def only(self, problems):
        self.assertEqual(len(problems), 1, problems)
        return problems[0]

    def test_a_correct_one_passes(self):
        self.touch("island.py")
        self.assertEqual(self.write(), [])

    def test_no_island_json_at_all(self):
        self.assertIn("island.json", self.only(manifest.faults(self.folder)))

    def test_unreadable_json(self):
        with open(os.path.join(self.folder, "island.json"), "w", encoding="utf-8") as f:
            f.write("{ not json")
        self.assertIn("not valid JSON", self.only(manifest.faults(self.folder)))

    def test_a_missing_field_is_named(self):
        self.touch("island.py")
        self.assertIn("`owner`", self.only(self.write(owner=manifest)))

    def test_a_field_nobody_has_heard_of_is_named(self):
        # a typo in a key is otherwise completely silent: the value is simply
        # never read and the island behaves as though it was never written
        self.touch("island.py")
        self.assertIn("`sesaon`", self.only(self.write(sesaon="Fall")))

    def test_a_future_format_is_refused_by_number(self):
        self.touch("island.py")
        self.assertIn("format 1", self.only(self.write(format=2)))

    def test_programme_and_map_may_not_be_the_same_id(self):
        self.touch("island.py")
        self.assertIn("different key spaces", self.only(self.write(map="test-club")))

    def test_a_shouted_id_is_not_a_slug(self):
        self.touch("island.py")
        self.assertIn("`programme`", self.only(self.write(programme="Test_Club")))

    def test_a_season_outside_the_vocabulary(self):
        self.touch("island.py")
        self.assertIn("`season`", self.only(self.write(season="Summer")))

    def test_no_season_at_all_is_allowed(self):
        self.touch("island.py")
        self.assertEqual(self.write(season=manifest), [])

    def test_a_module_that_is_not_there(self):
        self.touch("island.py")
        problems = self.write(modules=["island.py", "questions.py"])
        self.assertIn("questions.py", self.only(problems))

    def test_a_file_on_disk_that_nobody_listed(self):
        # the one that only breaks inside the game, which is the worst place
        self.touch("island.py", "questions.py")
        self.assertIn("never fetches it", self.only(self.write()))

    def test_an_entry_outside_the_modules(self):
        self.touch("island.py")
        self.assertIn("`entry`", self.only(self.write(entry="main.py")))

    def test_a_module_with_a_path_in_it(self):
        self.touch("island.py")
        problems = self.write(modules=["island.py", "sub/thing.py"])
        self.assertIn("one flat folder", problems[0])

    def test_shipping_the_engines_own_module(self):
        self.touch("island.py", "vine.py")
        problems = self.write(modules=["island.py", "vine.py"])
        self.assertTrue(any("the game provides" in p for p in problems), problems)


if __name__ == "__main__":
    unittest.main()
