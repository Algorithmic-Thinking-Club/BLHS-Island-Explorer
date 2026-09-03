"""The Panther's Maw does what it says, in both arms, down every branch.

This is the ADVANCED example's test, and it is written to be read next to
`test_skeleton.py` rather than instead of it. The skeleton's test shows the
smallest honest set: one handler, both arms, one award. This one shows what the
same idea looks like when the island is a room with seven handlers and most of
them branch on what the run holds.

WHAT A TEST LIKE THIS CAN AND CANNOT SAY. Nothing here performs anything. The
island yields dicts and this file answers them, so it proves the island asks for
the right things in the right order and takes the right branch. It cannot prove
the engine will do any of it: that only happens in the game, and for this island
it is `scripts/maw1-proof.mjs` in the engine repo, in a real browser, on the
published room. A green file here and a dead room are perfectly compatible.

THE NINE-WORD FENCE DOES NOT APPLY HERE, and that is on purpose. It fences the
STARTER SKELETON so a beginner's first copy cannot contain a word that comes
back as a refusal on their own line. This island is the other document: it is
what the machine can do, so it reaches for `look_at`, `actor_face`, `cutscene`
and `show`, and every one of those is checked below to be a word the engine
really has rather than one somebody wished for.
"""
import os
import re
import unittest

from tests import pump

ISLAND = "panther-maw"

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# the words the engine understands, read out of the vendored vine.py rather than
# typed here. A list typed twice is a list that drifts, and the whole point of
# this check is catching a word this island invented.
def _engine_words():
    with open(os.path.join(HERE, "vine.py"), encoding="utf-8") as f:
        return set(re.findall(r'"kind": "([a-z_]+)"', f.read()))


def answering(flags=(), board=(), trophies=None, advisory=None, mode="game", picks=(), score=3.4,
              refuse=()):
    """An engine that answers the questions this island actually asks.

    `refuse` names words this pretend engine cannot perform. A real refusal is
    RAISED at the yield that asked for it, which is what `pump.run` does with a
    thrown value, so this is the shape a member's island really meets.
    """
    queue = list(picks)
    state = {
        "flags": list(flags),
        "cord_board": list(board),
        "trophies": trophies or {"stickers": [], "badges": []},
        "advisory": advisory,
        "mode": mode,
    }

    def answer(intent):
        if intent["kind"] in refuse:
            raise pump.Refused('%s: this map cannot do that' % intent["kind"])
        if intent["kind"] == "get":
            return state[intent["path"]]
        if intent["kind"] == "choose":
            return queue.pop(0) if queue else 0
        if intent["kind"] == "play":
            return score
        return None
    return answer


def cord(name, earned=False, progress=0.0, detail="0 of 5", at_graduation=False):
    """One row shaped the way `get("cord_board")` really hands them over."""
    row = {
        "id": name.lower().replace(" ", "-"), "name": name, "colors": "gold",
        "rule": "the school's own words", "source": "docs/blhs/awards.md",
        "published": True, "earned": earned, "progress": progress, "detail": detail,
    }
    if at_graduation:
        row["settlesAtGraduation"] = True
    return row


class TheIslandLoads(unittest.TestCase):
    def setUp(self):
        self.manifest = pump.load(ISLAND)

    def test_it_claims_the_six_pressable_anchors_and_nothing_else(self):
        # THE LIST IS EXACT, not a subset. A handler claiming an anchor the room
        # does not carry is silent from the player's side, and the room carries
        # eleven anchors of which only six can be pressed: the other five are a
        # spawn, a region and three doors, and the file says why for each.
        self.assertEqual(pump.handlers(), [
            "start",
            "talk:chart_table", "talk:counselor", "talk:hearth",
            "talk:outfitter", "talk:principal_desk", "talk:trophy_wall",
        ])

    def test_it_does_not_claim_a_door(self):
        # `fire()` takes a door before it ever asks who owns the anchor, so a
        # handler on one would never run and would look exactly like a typo.
        for door in ("maw_entrance", "east_tunnel", "west_tunnel"):
            self.assertNotIn("talk:" + door, pump.handlers())

    def test_it_does_not_claim_the_region_or_the_spawn(self):
        # a region is logged and never fired, and a spawn is not something you
        # walk up to. Both would register cleanly here and do nothing in the game.
        for name in ("the_hall", "arrive_maw"):
            self.assertNotIn("talk:" + name, pump.handlers())

    def test_the_map_is_the_published_room(self):
        self.assertEqual(self.manifest["map"], "panther-maw")

    def test_the_programme_is_not_the_map(self):
        # one key space to the roster, so an id that is both cannot be resolved
        self.assertNotEqual(self.manifest["programme"], self.manifest["map"])


class EveryWordItUsesIsARealWord(unittest.TestCase):
    """An island cannot invent a word, and this is what says so out loud."""

    def setUp(self):
        pump.load(ISLAND)
        self.words = _engine_words()

    def paths(self):
        """Every branch this island has, driven, as (label, intents)."""
        board = [cord("High Honors", earned=True), cord("AP Honors", progress=0.6, detail="3 of 5")]
        return [
            ("first arrival", pump.run("start", answering())),
            ("later arrival", pump.run("start", answering(flags=["maw:seen"]))),
            ("the founding", pump.run("talk:principal_desk", answering(flags=["maw:seen"]))),
            ("the desk again", pump.run("talk:principal_desk",
                                        answering(flags=["maw:seen", "maw:founding"]))),
            ("the fire, owed", pump.run("talk:hearth", answering(advisory="core:y1"))),
            ("the fire, banked", pump.run("talk:hearth", answering(advisory=None))),
            ("the fire, walked out of", pump.run("talk:hearth",
                                                 answering(advisory="core:y1", score=None))),
            ("the counselor, empty", pump.run("talk:counselor", answering(picks=[1]))),
            ("the counselor, full", pump.run("talk:counselor", answering(board=board, picks=[0]))),
            ("the chart table", pump.run("talk:chart_table", answering())),
            ("the outfitter", pump.run("talk:outfitter", answering())),
            ("the empty wall", pump.run("talk:trophy_wall", answering())),
            ("the full wall", pump.run("talk:trophy_wall", answering(
                trophies={"stickers": ["a", "b"], "badges": ["c"]}))),
        ]

    def test_no_branch_asks_for_a_word_the_engine_does_not_have(self):
        for label, seen in self.paths():
            with self.subTest(path=label):
                self.assertEqual(set(pump.kinds(seen)) - self.words, set())

    def test_no_branch_asks_a_question_get_cannot_answer(self):
        # the closed list, out of vine.py's own docstring for `get`
        askable = {"year", "gpa", "tokens", "cords", "cord_board", "trophies",
                   "flags", "islands", "handle", "mode", "graduated", "advisory"}
        for label, seen in self.paths():
            with self.subTest(path=label):
                for g in pump.only(seen, "get"):
                    self.assertIn(g["path"], askable)

    def test_every_place_it_names_is_an_anchor_on_the_published_room(self):
        # ELEVEN NAMES AND NO OTHERS. A name the room does not carry is refused
        # at the member's own line in the game, which is right and late; here it
        # is caught before anybody opens a browser.
        room = {"arrive_maw", "maw_entrance", "chart_table", "hearth", "counselor",
                "principal_desk", "outfitter", "trophy_wall", "the_hall",
                "east_tunnel", "west_tunnel"}
        for label, seen in self.paths():
            with self.subTest(path=label):
                for intent in seen:
                    for key in ("anchor", "actor", "to"):
                        if isinstance(intent.get(key), str):
                            self.assertIn(intent[key], room)


class WalkingIn(unittest.TestCase):
    def setUp(self):
        pump.load(ISLAND)

    def test_the_room_introduces_itself_once(self):
        first = pump.run("start", answering())
        self.assertEqual(pump.kinds(first).count("say"), 2)
        self.assertIn("set_flag", pump.kinds(first))

    def test_and_never_again(self):
        later = pump.run("start", answering(flags=["maw:seen"]))
        self.assertEqual(pump.only(later, "say"), [])

    def test_the_wall_tells_the_truth_before_anybody_presses_it(self):
        # THE ONE THE GATE COULD NOT SEE. A placement is drawn from the first
        # frame, and the drawn shelf is a case with things on it, so a first year
        # with nothing earned used to walk in to a full trophy case and watch it
        # vanish when they pressed E. Arrival syncs it, on every load.
        for flags in ((), ("maw:seen",)):
            with self.subTest(flags=flags):
                empty = pump.run("start", answering(flags=flags))
                self.assertEqual([i["visible"] for i in pump.only(empty, "show")], [False])
                full = pump.run("start", answering(
                    flags=flags, trophies={"stickers": ["a"], "badges": []}))
                self.assertEqual([i["visible"] for i in pump.only(full, "show")], [True])

    def test_a_room_with_no_shelf_still_gets_its_arrival_lines(self):
        # `show` is a hard refusal on the offline copy of this room, and before
        # the guard it would have taken the two arrival lines with it.
        seen = pump.run("start", answering(refuse=("show",)))
        self.assertEqual(pump.kinds(seen).count("say"), 2)
        self.assertIn("show_refused", [i["event"] for i in pump.only(seen, "log")])


class TheFoundingEvent(unittest.TestCase):
    def setUp(self):
        pump.load(ISLAND)
        self.seen = pump.run("talk:principal_desk", answering(flags=["maw:seen"]))

    def test_it_writes_the_bare_flag_the_engine_sequences_off(self):
        flags = [i["flag"] for i in pump.only(self.seen, "set_flag")]
        self.assertEqual(flags, ["maw:founding"])

    def test_it_plays_the_authored_cutscene(self):
        self.assertEqual([i["script"] for i in pump.only(self.seen, "cutscene")],
                         ["maw-founding"])

    def test_it_points_the_room_out_and_then_gives_the_camera_back(self):
        looks = [i["anchor"] for i in pump.only(self.seen, "look_at")]
        self.assertEqual(looks, ["hearth", "counselor", "trophy_wall", None])

    def test_it_turns_the_principal_and_turns_him_back(self):
        turns = [i["facing"] for i in pump.only(self.seen, "actor_face")]
        self.assertEqual(turns, ["west", "south-west"])

    def test_the_principal_has_a_face_on_every_line_he_speaks(self):
        for line in pump.only(self.seen, "say"):
            self.assertEqual(line.get("portrait"), "principal")

    def test_a_room_with_nobody_at_the_desk_still_gets_its_founding(self):
        # THE OFFLINE COPY OF THIS ROOM BINDS NO PLACEMENTS. `actor_face` is a hard
        # refusal there, and a refusal is raised at the line that asked, so before
        # the guard it took the cutscene and the flag with it and the founding
        # replayed on every visit forever.
        seen = pump.run("talk:principal_desk",
                        answering(flags=["maw:seen"], refuse=("actor_face",)))
        self.assertEqual([i["script"] for i in pump.only(seen, "cutscene")], ["maw-founding"])
        self.assertEqual([i["flag"] for i in pump.only(seen, "set_flag")], ["maw:founding"])
        # and it says which word could not perform, rather than swallowing it
        self.assertIn("actor_face_refused", [i["event"] for i in pump.only(seen, "log")])

    def test_a_second_visit_is_one_line_and_no_scene(self):
        again = pump.run("talk:principal_desk", answering(flags=["maw:seen", "maw:founding"]))
        self.assertEqual(pump.kinds(again), ["get", "say"])


class TheFire(unittest.TestCase):
    def setUp(self):
        pump.load(ISLAND)

    def test_it_plays_the_beat_the_engine_named(self):
        seen = pump.run("talk:hearth", answering(advisory="core:y1"))
        self.assertEqual([i["beat"] for i in pump.only(seen, "play")], ["core:y1"])

    def test_it_never_forces_an_arm(self):
        # THE ONE THING AN ISLAND MUST NOT DO. Left off, the engine renders the
        # arm this student was assigned at join and both halves of the class read
        # the same content. Setting it here would opt somebody out of the study.
        for mode in ("game", "plain"):
            seen = pump.run("talk:hearth", answering(advisory="core:y1", mode=mode))
            for p in pump.only(seen, "play"):
                self.assertNotIn("as_plain", p)

    def test_a_banked_fire_does_not_run_the_beat_again(self):
        seen = pump.run("talk:hearth", answering(advisory=None))
        self.assertEqual(pump.only(seen, "play"), [])

    def test_it_never_awards_the_engines_own_beat(self):
        # the runner already wrote the grade, the credit and the tags. A second
        # row here would weigh the same year's GPA twice.
        for score in (4.0, 0.0, None):
            seen = pump.run("talk:hearth", answering(advisory="core:y1", score=score))
            self.assertEqual(pump.only(seen, "award"), [], "score=%r" % (score,))

    def test_walking_out_of_the_beat_is_not_a_zero(self):
        left = pump.run("talk:hearth", answering(advisory="core:y1", score=None))
        got = pump.run("talk:hearth", answering(advisory="core:y1", score=0.0))
        self.assertNotEqual(
            [i["text"] for i in pump.only(left, "say")],
            [i["text"] for i in pump.only(got, "say")])


class TheCounselor(unittest.TestCase):
    def setUp(self):
        pump.load(ISLAND)

    def test_an_untouched_run_gets_one_honest_line(self):
        seen = pump.run("talk:counselor", answering(picks=[1]))
        said = [i["text"] for i in pump.only(seen, "say")]
        self.assertEqual(len(said), 1)
        self.assertIn("Nothing on your cape", said[0])

    def test_she_says_the_engines_own_detail_string_and_not_her_own_arithmetic(self):
        board = [cord("AP Honors", progress=0.6, detail="3 of 5 AP classes passed")]
        seen = pump.run("talk:counselor", answering(board=board, picks=[1]))
        said = [i["text"] for i in pump.only(seen, "say")]
        self.assertIn("3 of 5 AP classes passed", said[0])

    def test_she_says_at_most_two_of_each(self):
        board = [cord("A", earned=True), cord("B", earned=True), cord("C", earned=True),
                 cord("D", progress=0.9), cord("E", progress=0.5), cord("F", progress=0.1)]
        seen = pump.run("talk:counselor", answering(board=board, picks=[1]))
        self.assertEqual(len(pump.only(seen, "say")), 4)

    def test_the_two_graduation_cords_do_not_take_both_slots(self):
        # THE ONE THAT BROKE HER. Both GPA bands move on the very first grade and
        # keep moving for four years, so sorted by progress alone they are the
        # only two cords she would ever name, in any year, on any run.
        board = [
            cord("Highest Honors", progress=0.93, detail="GPA 3.50 of 3.76", at_graduation=True),
            cord("High Honors", progress=1.0, detail="GPA 3.50 of 3.5", at_graduation=True),
            cord("AP Honors", progress=0.6, detail="3 of 5 AP classes passed"),
        ]
        said = [i["text"] for i in
                pump.only(pump.run("talk:counselor", answering(board=board, picks=[1])), "say")]
        self.assertEqual(len(said), 2)
        self.assertEqual(len([t for t in said if t.startswith("G") or "GPA" in t]), 1)
        self.assertTrue(any("AP Honors" in t for t in said), said)

    def test_the_nearest_cord_is_named_first(self):
        board = [cord("Far", progress=0.1, detail="1 of 5"),
                 cord("Near", progress=0.9, detail="4 of 5")]
        seen = pump.run("talk:counselor", answering(board=board, picks=[1]))
        self.assertIn("Near", pump.only(seen, "say")[0]["text"])

    def test_a_cord_at_exactly_zero_is_not_close_to_anything(self):
        seen = pump.run("talk:counselor", answering(board=[cord("Untouched")], picks=[1]))
        self.assertIn("Nothing on your cape", pump.only(seen, "say")[0]["text"])

    def test_the_board_opens_only_when_it_is_asked_for(self):
        yes = pump.run("talk:counselor", answering(picks=[0]))
        no = pump.run("talk:counselor", answering(picks=[1]))
        self.assertEqual([i["ui"] for i in pump.only(yes, "open")], ["handbook"])
        self.assertEqual(pump.only(no, "open"), [])

    def test_nobody_answering_is_not_the_first_button(self):
        # -1 is the player walking off while the buttons are up
        gone = pump.run("talk:counselor", answering(picks=[-1]))
        self.assertEqual(pump.only(gone, "open"), [])


class TheWall(unittest.TestCase):
    def setUp(self):
        pump.load(ISLAND)

    def test_an_empty_wall_hides_the_shelf_and_says_so(self):
        seen = pump.run("talk:trophy_wall", answering())
        self.assertEqual([i["visible"] for i in pump.only(seen, "show")], [False])
        self.assertIn("Empty hooks", pump.only(seen, "say")[0]["text"])

    def test_it_speaks_before_it_touches_the_picture(self):
        # `show` refuses hard on a map whose trophy_wall is not bound to a
        # placement, and a refusal takes the rest of the handler with it. Said
        # first, a room drawn without a shelf still gets its sentence.
        for trophies in ({"stickers": [], "badges": []}, {"stickers": ["a"], "badges": []}):
            with self.subTest(trophies=trophies):
                kinds = pump.kinds(pump.run("talk:trophy_wall", answering(trophies=trophies)))
                self.assertLess(kinds.index("say"), kinds.index("show"))

    def test_it_counts_stickers_and_badges_together(self):
        seen = pump.run("talk:trophy_wall", answering(
            trophies={"stickers": ["a", "b"], "badges": ["c"]}))
        self.assertEqual([i["visible"] for i in pump.only(seen, "show")], [True])
        self.assertIn("3 up there", pump.only(seen, "say")[0]["text"])

    def test_one_thing_is_said_in_words_and_not_as_the_number_one(self):
        seen = pump.run("talk:trophy_wall", answering(trophies={"stickers": ["a"], "badges": []}))
        self.assertIn("One thing", pump.only(seen, "say")[0]["text"])

    def test_it_shows_the_anchor_and_never_the_placement(self):
        # the anchor is `trophy_wall` and the drawn shelf is `the_trophy_wall`.
        # Naming the placement here would refuse on the member's own line.
        seen = pump.run("talk:trophy_wall", answering())
        self.assertEqual([i["anchor"] for i in pump.only(seen, "show")], ["trophy_wall"])


class ThePanels(unittest.TestCase):
    def setUp(self):
        pump.load(ISLAND)

    def test_the_chart_table_opens_the_planner(self):
        seen = pump.run("talk:chart_table", answering())
        self.assertEqual([i["ui"] for i in pump.only(seen, "open")], ["planner"])

    def test_it_does_not_log_an_event_the_panel_already_logs(self):
        # `Planner.tsx` fires `planner_opened` when it mounts. A second one here
        # doubled every count of how often a student opened the year sheet.
        seen = pump.run("talk:chart_table", answering())
        self.assertEqual([i["event"] for i in pump.only(seen, "log")], [])

    def test_the_outfitter_opens_the_wardrobe(self):
        seen = pump.run("talk:outfitter", answering())
        self.assertEqual([i["ui"] for i in pump.only(seen, "open")], ["wardrobe"])

    def test_both_of_them_say_something_before_a_panel_covers_the_room(self):
        for handler in ("talk:chart_table", "talk:outfitter"):
            with self.subTest(handler=handler):
                kinds = pump.kinds(pump.run(handler, answering()))
                self.assertLess(kinds.index("say"), kinds.index("open"))


class TheStudyHolds(unittest.TestCase):
    """The one class every island needs, and this room's version of it.

    The skeleton's asks whether both arms read the same questions, because the
    skeleton owns its questions. This room does not: the only scored thing in it
    is the engine's own core beat, and the two arms of THAT are the engine's to
    render. So what has to hold here is one step back, and it is the rule that
    lets the engine keep its promise: this island must never choose the arm, and
    it must ask for the same beat whichever arm is playing.
    """

    def setUp(self):
        pump.load(ISLAND)

    def test_both_arms_are_sent_to_the_same_beat(self):
        game = pump.run("talk:hearth", answering(advisory="core:y1", mode="game"))
        plain = pump.run("talk:hearth", answering(advisory="core:y1", mode="plain"))
        self.assertEqual(pump.kinds(game), pump.kinds(plain))
        self.assertEqual([i["beat"] for i in pump.only(game, "play")],
                         [i["beat"] for i in pump.only(plain, "play")])

    def test_no_handler_anywhere_reads_the_arm_to_change_its_content(self):
        # a room that said different words to the two halves of the class would
        # be a second confound sitting inside the thing being measured
        for handler in pump.handlers():
            with self.subTest(handler=handler):
                game = pump.run(handler, answering(mode="game", advisory="core:y1"))
                plain = pump.run(handler, answering(mode="plain", advisory="core:y1"))
                self.assertEqual([i.get("text") for i in pump.only(game, "say")],
                                 [i.get("text") for i in pump.only(plain, "say")])


if __name__ == "__main__":
    unittest.main()
