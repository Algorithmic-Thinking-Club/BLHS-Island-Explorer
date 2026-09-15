"""Tests for the Panther Maw: both films, all seven handlers, every branch.

Nothing here performs anything. The island yields intents and this file answers
them, so it checks what the island asks for and in what order.
"""
import os
import re
import unittest

from tests import pump

ISLAND = "panther-maw"

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# the words the engine understands, read out of vine.py rather than typed here
def _engine_words():
    with open(os.path.join(HERE, "vine.py"), encoding="utf-8") as f:
        return set(re.findall(r'"kind": "([a-z_]+)"', f.read()))


def answering(flags=(), board=(), trophies=None, advisory=None, mode="game", picks=(), score=3.4,
              refuse=(), year=1, planned=False, **rest):
    """A run for this island to answer against.

    `board` is the cord board and `picks` is the buttons the player presses.
    """
    return pump.answering(
        refuse=refuse, choices=picks, score=score,
        flags=flags, cord_board=board, trophies=trophies or {"stickers": [], "badges": []},
        advisory=advisory, mode=mode, year=year, planned=planned, **rest)


# `maw:railed` says he has been here before; `maw:founding` gates the tunnel beat.
RAILED = "maw:railed"
FOUNDING = "maw:founding"

# `maw:handed_over` says the opening is finished, and fences the road to the ending.
HANDED_OVER = "maw:handed_over"


def midyear(**kw):
    """A run with Advisory still owed, which is the ordinary half of the year."""
    kw.setdefault("advisory", "core:y1")
    return answering(**kw)


# "yearbook" is the phase for a year with the sheet stamped and the beat sat
def finished(year=1, flags=(), **kw):
    """An engine whose year is done, so the principal can close it."""
    return answering(phase="yearbook", year=year,
                     flags=[RAILED, HANDED_OVER] + list(flags), **kw)


def last(kinds, word):
    """The index of the last time `word` happens, for the words the room says twice."""
    return max(n for n, k in enumerate(kinds) if k == word)


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
        # the list is exact, not a subset: six of the room's eleven anchors can be pressed
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
            # nobody bound means `place` refusing, which is the word this road takes away
            ("first arrival, the founding", pump.run("start", answering())),
            ("first arrival, nobody bound",
             pump.run("start", answering(refuse=("place",)))),
            ("later arrival", pump.run("start", answering(flags=[RAILED]))),
            ("home, after the page turned", pump.run("start", answering(
                flags=[RAILED, "yearbook:y1"]))),
            # the closing film, the only place `enter` and the last `choose` are said.
            # It is pressed, not loaded into: an earlier `start` has already set the
            # latch that fences the load road.
            ("the ending, the page still to turn",
             pump.run("talk:principal_desk", finished(handle="Ash"))),
            ("the ending, the page already turned",
             pump.run("talk:principal_desk", finished(
                 handle="Ash", flags=["yearbook:y1", "maw:wall_shown:y1"]))),
            ("the founding, from the desk", pump.run("talk:principal_desk", answering())),
            ("the desk again", pump.run("talk:principal_desk",
                                        answering(flags=[RAILED]))),
            ("the counselor, home", pump.run("talk:counselor", answering(advisory=None))),
            ("the fire, owed", pump.run("talk:hearth", answering(advisory="core:y1"))),
            ("the fire, banked", pump.run("talk:hearth", answering(advisory=None))),
            ("the fire, walked out of", pump.run("talk:hearth",
                                                 answering(advisory="core:y1", score=None))),
            ("the counselor, empty", pump.run("talk:counselor", midyear(picks=[1]))),
            ("the counselor, full", pump.run("talk:counselor", midyear(board=board, picks=[0]))),
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
        # `pump.askable` reads the paths out of vine.py, so nothing here is typed twice
        askable = pump.askable()
        for label, seen in self.paths():
            with self.subTest(path=label):
                for g in pump.only(seen, "get"):
                    self.assertIn(g["path"], askable)

    def test_every_place_it_names_is_an_anchor_on_the_published_room(self):
        # eleven names and no others. A name the room lacks is refused in the game.
        room = {"arrive_maw", "maw_entrance", "chart_table", "hearth", "counselor",
                "principal_desk", "outfitter", "trophy_wall", "the_hall",
                "east_tunnel", "west_tunnel"}
        # and `thor`, which is a place and not an anchor: it means beside the player,
        # and it is the heading `actor_face` derives.
        named = room | {"thor"}
        # `at` is a place too, because `place` is what puts a body at one
        for label, seen in self.paths():
            with self.subTest(path=label):
                for intent in seen:
                    for key in ("anchor", "actor", "to", "at"):
                        if isinstance(intent.get(key), str):
                            self.assertIn(intent[key], named)


class WalkingIn(unittest.TestCase):
    def setUp(self):
        pump.load(ISLAND)

    def test_the_first_time_in_is_the_film_and_his_line_is_the_first_word(self):
        """The room opens with the film, and nothing speaks before the bars go up."""
        first = pump.run("start", answering())
        kinds = pump.kinds(first)
        said = pump.only(first, "say")
        self.assertLess(kinds.index("movie"), kinds.index("say"))
        self.assertEqual(said[0]["text"], "Welcome to Bonney Lake High. Come with me.")
        self.assertEqual(said[0]["who"], "principal_desk")
        self.assertIn(FOUNDING, [i["flag"] for i in pump.only(first, "set_flag")])

    def test_and_never_again(self):
        later = pump.run("start", answering(flags=[RAILED]))
        self.assertEqual(pump.only(later, "say"), [])

    def test_the_case_is_on_the_wall_from_the_first_frame(self):
        """Arrival puts the drawn case up on every load, whatever is in it."""
        for flags in ((), (RAILED,)):
            for trophies in ({"stickers": [], "badges": []},
                             {"stickers": ["a"], "badges": []}):
                with self.subTest(flags=flags, trophies=trophies):
                    seen = pump.run("start", answering(flags=flags, trophies=trophies))
                    shown = pump.only(seen, "show")
                    self.assertTrue(shown)
                    self.assertEqual({(i["anchor"], i["visible"]) for i in shown},
                                     {("trophy_wall", True)})

    def test_a_room_with_no_shelf_still_gets_its_founding(self):
        # `show` is a hard refusal on the offline copy, and beat 1 still has to run
        seen = pump.run("start", answering(refuse=("show",)))
        said = [i["text"] for i in pump.only(seen, "say")]
        self.assertEqual(said[0], "Welcome to Bonney Lake High. Come with me.")
        self.assertIn("show_refused", [i["event"] for i in pump.only(seen, "log")])
        self.assertIn(FOUNDING, [i["flag"] for i in pump.only(seen, "set_flag")])

    def test_walking_in_with_the_year_done_plays_the_ending(self):
        """Coming back in with the year finished plays the closing film, not a line."""
        # the quiet road runs first, because the room will not start the ending on a
        # load that just played a film and remembers that for the life of the import.
        after = pump.run("start", answering(
            flags=[RAILED, HANDED_OVER, "yearbook:y1"], phase="done"))
        self.assertEqual(pump.only(after, "movie"), [])
        self.assertEqual(pump.only(after, "say"), [])

        seen = pump.run("start", finished(handle="Ash"))
        self.assertEqual([i["on"] for i in pump.only(seen, "movie")], [True, False])
        said = [i["text"] for i in pump.only(seen, "say")]
        self.assertTrue(said)
        for text in said:
            self.assertNotIn("next time", text.lower())
        self.assertNotIn("maw:next_time", [i["flag"] for i in pump.only(seen, "set_flag")])


class TheFoundingEvent(unittest.TestCase):
    """The opening film: the tunnel, the sheet, the fire, the wall, the handover.

    `self.whole` is the student who does everything he is asked, and
    `self.stepped_off` is the one who keeps closing the schedule.
    """

    def setUp(self):
        self.manifest = pump.load(ISLAND)
        self.whole = pump.run("start", answering(planned=True, advisory="core:y1"))
        self.stepped_off = pump.run("start", answering())

    def test_the_principal_appears_in_front_of_whoever_walked_in(self):
        """He is placed at the student, so the film names no anchor at all."""
        placed = [(i["actor"], i["at"]) for i in pump.only(self.whole, "place")]
        self.assertEqual(placed[0], ("principal_desk", "thor"))
        # and nothing in the opening carries a body straight at a target. That
        # word belongs to the closing film, where he really does cross the room.
        self.assertEqual(pump.only(self.whole, "actor_move"), [])

    def test_he_is_standing_there_before_the_camera_moves_or_he_speaks(self):
        # the order `opening()` needs: placed, then the shot, then he speaks
        kinds = pump.kinds(self.whole)
        self.assertLess(kinds.index("place"), kinds.index("view"))
        self.assertLess(kinds.index("view"), kinds.index("say"))

    def test_one_line_per_beat_and_never_two(self):
        """One person says one thing a beat, so four beats speak on this road.

        The recovery lines are the exception, and only a student who closes a screen
        hears one.
        """
        said = [i["text"] for i in pump.only(self.whole, "say")]
        self.assertEqual(len(said), 4)
        self.assertEqual(len(set(said)), 4)
        # and not the engine's canned `cutscene`, which plays a scene an island cannot
        # read. This film is composed word by word so a member can follow it.
        self.assertEqual(pump.only(self.whole, "cutscene"), [])
        # and the camera never cuts away: the film rides the student's own shoulder
        self.assertEqual(pump.only(self.whole, "look_at"), [])

    def test_the_principal_has_a_face_on_the_line(self):
        for line in pump.only(self.whole, "say"):
            self.assertEqual(line.get("portrait"), "principal")

    def test_it_writes_the_bare_flags_the_engine_sequences_off(self):
        """Year one's flags, in the order the film writes them, every one unscoped.

        The engine sequences year one off these exact strings, so a scoped flag like
        `the-maw:founding` would never be read.
        """
        flags = [i["flag"] for i in pump.only(self.whole, "set_flag")]
        self.assertEqual(flags, [
            "maw:founding", "vignette:y1", "maw:wall_shown:y1", "maw:railed",
            "handbook:granted", "chart:granted", "maw:handed_over",
        ])
        for flag in flags:
            self.assertFalse(flag.startswith(self.manifest["programme"] + ":"), flag)

    def test_the_corner_arrives_after_the_bars_and_one_plaque_at_a_time(self):
        """The corner grants land after the bars come down, one at a time.

        A wait between the two flags keeps each arrival its own moment.
        """
        def where(pred):
            return next(n for n, i in enumerate(self.whole) if pred(i))

        bars_down = where(lambda i: i["kind"] == "movie" and i["on"] is False)
        handbook = where(lambda i: i.get("flag") == "handbook:granted")
        chart = where(lambda i: i.get("flag") == "chart:granted")
        self.assertLess(bars_down, handbook)
        self.assertLess(handbook, chart)
        self.assertTrue(any(i["kind"] == "wait" for i in self.whole[handbook:chart]))

    def test_the_year_lights_the_table_before_the_rail_points_at_it(self):
        """The year lights the chart table first, and the rail's arrow goes on top."""
        kinds = pump.kinds(self.stepped_off)
        self.assertLess(kinds.index("set_flag"), kinds.index("guide_to"))
        self.assertLess(kinds.index("guide_to"), kinds.index("open"))
        self.assertEqual(pump.only(self.stepped_off, "guide_to")[0]["anchor"], "chart_table")
        self.assertEqual({i["ui"] for i in pump.only(self.stepped_off, "open")}, {"planner"})

    def test_every_arrow_it_raises_is_taken_down_before_it_lets_go(self):
        """No arrow is left up: every road out of the film ends with `guide_to(None)`."""
        for label, seen in (("the whole film", self.whole),
                            ("stepped off at the schedule", self.stepped_off)):
            with self.subTest(road=label):
                arrows = pump.only(seen, "guide_to")
                self.assertTrue(arrows)
                self.assertIsNone(arrows[-1]["anchor"])

    def test_he_is_let_go_after_the_last_panel_and_never_walked_home(self):
        # he is released after the last panel, and the camera comes back after him,
        # because `view` ends the shot the release happened inside.
        for label, seen in (("the whole film", self.whole),
                            ("stepped off at the schedule", self.stepped_off)):
            with self.subTest(road=label):
                kinds = pump.kinds(seen)
                released = last(kinds, "actor_release")
                self.assertLess(last(kinds, "open"), released)
                self.assertLess(released, last(kinds, "view"))
                self.assertEqual(pump.only(seen, "actor_move"), [])

    def test_a_room_with_nobody_bound_still_gets_its_founding(self):
        """The offline copy of this room binds no placements.

        Every word that touches a body is a hard refusal there, so the film has to run
        to the end with all six of them refused.
        """
        seen = pump.run("start", answering(
            refuse=("place", "lead_to", "walk_to", "actor_face", "actor_release", "show"),
            planned=True, advisory="core:y1"))
        said = [i["text"] for i in pump.only(seen, "say")]
        self.assertEqual(said[0], "Welcome to Bonney Lake High. Come with me.")
        flags = [i["flag"] for i in pump.only(seen, "set_flag")]
        self.assertIn(FOUNDING, flags)
        # and it runs all the way to the end rather than stopping quietly
        # somewhere in the middle with the room still held
        self.assertIn(HANDED_OVER, flags)
        self.assertEqual([i["ui"] for i in pump.only(seen, "open")], ["wall", "tour"])
        # and every one of them says which word could not perform, on the
        # island's own line, rather than being swallowed
        logged = {i["event"] for i in pump.only(seen, "log")}
        for event in ("place_refused", "lead_to_refused", "walk_to_refused",
                      "actor_face_refused", "actor_release_refused", "show_refused"):
            self.assertIn(event, logged)

    def test_from_the_desk_nobody_is_placed_and_nobody_is_moved(self):
        """A press starts in front of him, so `rail(walk=False)` skips the placing.

        It logs which road the arrival came in by, so the two are told apart.
        """
        seen = pump.run("talk:principal_desk", answering(planned=True, advisory="core:y1"))
        self.assertEqual(pump.only(seen, "place"), [])
        self.assertEqual(pump.only(seen, "actor_move"), [])
        self.assertIn(FOUNDING, [i["flag"] for i in pump.only(seen, "set_flag")])
        pressed = [i["data"]["where"] for i in pump.only(seen, "log")
                   if i["event"] == "founding_seen"]
        walked = [i["data"]["where"] for i in pump.only(self.whole, "log")
                  if i["event"] == "founding_seen"]
        self.assertEqual(pressed, ["principal_desk"])
        self.assertEqual(walked, ["arrive_maw"])

    def test_a_second_visit_is_one_line_and_no_scene(self):
        """He reads the run and says one thing. The film never comes back."""
        again = pump.run("talk:principal_desk", answering(flags=[RAILED]))
        self.assertEqual([k for k in pump.kinds(again) if k != "get"], ["say"])


class TheFire(unittest.TestCase):
    def setUp(self):
        pump.load(ISLAND)

    def test_it_plays_the_beat_the_engine_named(self):
        seen = pump.run("talk:hearth", answering(advisory="core:y1"))
        self.assertEqual([i["beat"] for i in pump.only(seen, "play")], ["core:y1"])

    def test_it_never_forces_an_arm(self):
        # leave the arm off and the engine renders the one this student was assigned
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
        seen = pump.run("talk:counselor", midyear(picks=[1]))
        said = [i["text"] for i in pump.only(seen, "say")]
        self.assertEqual(len(said), 1)
        self.assertIn("No cord started yet", said[0])

    def test_she_says_the_engines_own_detail_string_and_not_her_own_arithmetic(self):
        board = [cord("AP Honors", progress=0.6, detail="3 of 5 AP classes passed")]
        seen = pump.run("talk:counselor", midyear(board=board, picks=[1]))
        said = [i["text"] for i in pump.only(seen, "say")]
        self.assertIn("3 of 5 AP classes passed", said[0])

    def test_she_says_at_most_two_of_each(self):
        board = [cord("A", earned=True), cord("B", earned=True), cord("C", earned=True),
                 cord("D", progress=0.9), cord("E", progress=0.5), cord("F", progress=0.1)]
        seen = pump.run("talk:counselor", midyear(board=board, picks=[1]))
        self.assertEqual(len(pump.only(seen, "say")), 4)

    def test_the_two_graduation_cords_do_not_take_both_slots(self):
        # both GPA bands move on the first grade, so progress alone would name only them
        board = [
            cord("Highest Honors", progress=0.93, detail="GPA 3.50 of 3.76", at_graduation=True),
            cord("High Honors", progress=1.0, detail="GPA 3.50 of 3.5", at_graduation=True),
            cord("AP Honors", progress=0.6, detail="3 of 5 AP classes passed"),
        ]
        said = [i["text"] for i in
                pump.only(pump.run("talk:counselor", midyear(board=board, picks=[1])), "say")]
        self.assertEqual(len(said), 2)
        self.assertEqual(len([t for t in said if t.startswith("G") or "GPA" in t]), 1)
        self.assertTrue(any("AP Honors" in t for t in said), said)

    def test_the_nearest_cord_is_named_first(self):
        board = [cord("Far", progress=0.1, detail="1 of 5"),
                 cord("Near", progress=0.9, detail="4 of 5")]
        seen = pump.run("talk:counselor", midyear(board=board, picks=[1]))
        self.assertIn("Near", pump.only(seen, "say")[0]["text"])

    def test_a_cord_at_exactly_zero_is_not_close_to_anything(self):
        seen = pump.run("talk:counselor", midyear(board=[cord("Untouched")], picks=[1]))
        self.assertIn("No cord started yet", pump.only(seen, "say")[0]["text"])

    def test_the_cords_page_opens_only_when_it_is_asked_for(self):
        # the cords page, not the islands one: `open("handbook")` lands on Islands
        yes = pump.run("talk:counselor", midyear(picks=[0]))
        no = pump.run("talk:counselor", midyear(picks=[1]))
        self.assertEqual([i["ui"] for i in pump.only(yes, "open")], ["cords"])
        self.assertEqual(pump.only(no, "open"), [])

    def test_nobody_answering_is_not_the_first_button(self):
        # -1 is the player walking off while the buttons are up
        gone = pump.run("talk:counselor", midyear(picks=[-1]))
        self.assertEqual(pump.only(gone, "open"), [])

    def test_she_never_starts_the_ending_however_finished_the_year_is(self):
        """She says the same thing whatever the run holds. The ending is not hers."""
        for label, ans in (("advisory done, page not turned",
                            answering(advisory=None)),
                           ("the whole year done",
                            answering(advisory=None, phase="yearbook"))):
            with self.subTest(run=label):
                seen = pump.run("talk:counselor", ans)
                self.assertEqual(pump.only(seen, "movie"), [])
                self.assertEqual([i["ui"] for i in pump.only(seen, "open")], ["cords"])
                # and she turns no page
                self.assertEqual(pump.only(seen, "set_flag"), [])
                self.assertIn("No cord started yet", pump.only(seen, "say")[0]["text"])

    def test_after_the_page_has_turned_she_counsels_again(self):
        seen = pump.run("talk:counselor", answering(
            advisory=None, flags=["yearbook:y1"], picks=[1]))
        self.assertEqual(pump.only(seen, "open"), [])
        self.assertIn("No cord started yet", pump.only(seen, "say")[0]["text"])


# known bug: `well_done` names year one in every year, and no test below fails on it.
class TheClosingFilm(unittest.TestCase):
    """The other film: he comes to find you, the cord, the page, and the boat.

    These tests press the principal rather than loading the room, because the load
    road is fenced by a module latch an earlier run would have set.
    """

    def setUp(self):
        pump.load(ISLAND)

    def test_the_turned_flag_is_the_current_years(self):
        """Year two's page is `yearbook:y2`, and year one's does not close it."""
        # year two with year one's page turned: her line names the year just finished
        seen = pump.run("talk:principal_desk", finished(year=2, flags=["yearbook:y1"]))
        said = [i["text"] for i in pump.only(seen, "say")]
        self.assertIn("Year two is done. Here is your second cord.", said)
        self.assertEqual([i["ui"] for i in pump.only(seen, "open")], ["wall", "yearbook"])
        self.assertIn("maw:wall_shown:y2", [i["flag"] for i in pump.only(seen, "set_flag")])

        # and with year two's page turned nothing opens, and the room ends at the boat
        over = pump.run("talk:principal_desk", finished(
            year=2, handle="Ash", flags=["yearbook:y2", "maw:wall_shown:y2"]))
        self.assertEqual(pump.only(over, "open"), [])
        self.assertEqual([i["map"] for i in pump.only(over, "enter")], ["hub"])

    def test_the_last_press_of_the_year_is_his_and_the_film_waits_on_it(self):
        # `choose` draws one option as one big button, and the film waits on the press
        seen = pump.run("talk:principal_desk", finished(
            handle="Ash", flags=["yearbook:y1", "maw:wall_shown:y1"]))
        kinds = pump.kinds(seen)
        self.assertEqual([i["options"] for i in pump.only(seen, "choose")], [["Sail Home"]])
        self.assertLess(kinds.index("choose"), kinds.index("enter"))
        # and he is let go of before the door, because `enter` tears this island
        # down and a driven body left standing is left standing on the next map
        self.assertLess(last(kinds, "actor_release"), kinds.index("enter"))

    def test_a_page_left_unturned_steps_off_instead_of_sailing(self):
        # closing the yearbook is not finishing the year, so the film hands the room back
        seen = pump.run("talk:principal_desk", finished(handle="Ash"))
        self.assertEqual(pump.only(seen, "enter"), [])
        self.assertEqual(pump.only(seen, "choose"), [])
        self.assertEqual([i["view"] for i in pump.only(seen, "view")], ["close", "walk"])
        self.assertEqual([i["text"] for i in pump.only(seen, "objective")][-1], None)


class TheWall(unittest.TestCase):
    def setUp(self):
        pump.load(ISLAND)

    def test_an_empty_wall_keeps_its_case_and_the_line_says_it_is_empty(self):
        """The case stays on the wall, and the line is what says it is empty."""
        seen = pump.run("talk:trophy_wall", answering())
        self.assertEqual([i["visible"] for i in pump.only(seen, "show")], [True])
        self.assertIn("What I earn this year goes up here", pump.only(seen, "say")[0]["text"])

    def test_it_speaks_before_it_touches_the_picture(self):
        # `show` refuses hard on a map whose trophy_wall is not bound to a
        # placement, and a refusal takes the rest of the handler with it. Said
        # first, a room drawn without a shelf still gets its sentence.
        for trophies in ({"stickers": [], "badges": []}, {"stickers": ["a"], "badges": []}):
            with self.subTest(trophies=trophies):
                kinds = pump.kinds(pump.run("talk:trophy_wall", answering(trophies=trophies)))
                self.assertLess(kinds.index("say"), kinds.index("show"))

    def test_it_counts_stickers_and_badges_together(self):
        # the case stays on the wall either way, so the line is what changes. Either
        # list on its own flips the sentence, which is what "together" means.
        for trophies in ({"stickers": ["a"], "badges": []},
                         {"stickers": [], "badges": ["c"]}):
            with self.subTest(trophies=trophies):
                seen = pump.run("talk:trophy_wall", answering(trophies=trophies))
                self.assertIn("see what is on it", pump.only(seen, "say")[0]["text"])

    def test_no_number_is_ever_said_at_the_wall(self):
        # the panel carries the count, and the line at the wall carries no number
        for trophies in ({"stickers": [], "badges": []}, {"stickers": ["a"], "badges": []},
                         {"stickers": ["a", "b"], "badges": ["c"]}):
            with self.subTest(trophies=trophies):
                said = pump.only(pump.run("talk:trophy_wall", answering(trophies=trophies)), "say")[0]
                self.assertFalse(any(ch.isdigit() for ch in said["text"]))
                self.assertEqual(said.get("who"), "thor")

    def test_it_opens_the_wall_panel_after_the_line(self):
        # the frames for everything picked this year are the engine's panel,
        # raised by name, after the line and the shelf
        seen = pump.run("talk:trophy_wall", answering())
        kinds = pump.kinds(seen)
        self.assertEqual(kinds[-1], "open")
        self.assertLess(kinds.index("say"), kinds.index("open"))
        self.assertEqual([i["ui"] for i in pump.only(seen, "open")], ["wall"])

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
        # `Planner.tsx` logs `planner_opened` itself, so a second one here doubles it
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
    """This island never chooses the arm, and asks for the same beat in either one."""

    def setUp(self):
        pump.load(ISLAND)

    def test_both_arms_are_sent_to_the_same_beat(self):
        game = pump.run("talk:hearth", answering(advisory="core:y1", mode="game"))
        plain = pump.run("talk:hearth", answering(advisory="core:y1", mode="plain"))
        self.assertEqual(pump.kinds(game), pump.kinds(plain))
        self.assertEqual([i["beat"] for i in pump.only(game, "play")],
                         [i["beat"] for i in pump.only(plain, "play")])

    def test_no_handler_anywhere_reads_the_arm_to_change_its_content(self):
        for handler in pump.handlers():
            with self.subTest(handler=handler):
                game = pump.run(handler, answering(mode="game", advisory="core:y1"))
                plain = pump.run(handler, answering(mode="plain", advisory="core:y1"))
                self.assertEqual([i.get("text") for i in pump.only(game, "say")],
                                 [i.get("text") for i in pump.only(plain, "say")])


class TheStagingIsWatchable(unittest.TestCase):
    """Where the two of them stand, which way they look, and whether a walk shows.

    A walk aimed at the player stops beside him and covers almost no ground, so the
    words that cross a room are aimed at a place.
    """

    def setUp(self):
        pump.load(ISLAND)

    def films(self):
        """Both films, down the roads that reach every beat of them."""
        return [
            ("the opening, walked in",
             pump.run("start", answering(planned=True, advisory="core:y1"))),
            ("the opening, everything owed", pump.run("start", answering())),
            ("the opening, pressed at the desk",
             pump.run("talk:principal_desk", answering(planned=True, advisory="core:y1"))),
            ("the closing, the page still to turn",
             pump.run("talk:principal_desk", finished(handle="Ash"))),
            ("the closing, the page already turned",
             pump.run("talk:principal_desk", finished(
                 handle="Ash", flags=["yearbook:y1", "maw:wall_shown:y1"]))),
        ]

    def test_no_walk_in_either_film_is_aimed_at_the_player(self):
        """A walk aimed at the player stops beside him and covers almost no ground.

        `place` may still name the player, because it says where a body already is.
        """
        for label, seen in self.films():
            with self.subTest(film=label):
                for word in ("actor_move", "lead_to"):
                    aimed = [i for i in pump.only(seen, word) if i.get("to") == "thor"]
                    self.assertEqual(aimed, [], "%s is aimed at the player" % word)

    def test_the_closing_opens_by_crossing_the_hall(self):
        """The ending opens with `lead_to` across the hall, which is a walk you can see.

        `lead_to` ends by turning the two of them to face each other.
        """
        for road, flags in (("the page still to turn", []),
                            ("the page already turned",
                             ["yearbook:y1", "maw:wall_shown:y1"])):
            with self.subTest(road=road):
                seen = pump.run("talk:principal_desk", finished(handle="Ash", flags=flags))
                walks = [i for i in seen if i["kind"] in ("lead_to", "walk_to", "actor_move")]
                self.assertTrue(walks, "the ending moves nobody at all")
                self.assertEqual((walks[0]["kind"], walks[0].get("actor"), walks[0].get("to")),
                                 ("lead_to", "principal_desk", "the_hall"))
                # and the panel names the step he is being walked through
                said = [i["text"] for i in pump.only(seen, "objective")]
                self.assertEqual(said[0], "Follow the principal.")

    def test_the_congratulation_turns_him_instead_of_shuffling_him(self):
        """The congratulation turns him with `actor_face` instead of walking him."""
        seen = pump.run("talk:principal_desk", finished(
            handle="Ash", flags=["yearbook:y1", "maw:wall_shown:y1"]))
        congratulation = max(n for n, i in enumerate(seen)
                             if i["kind"] == "say" and "finished" in i["text"])
        turns = [n for n, i in enumerate(seen)
                 if i["kind"] == "actor_face" and i["facing"] == "thor"]
        self.assertTrue(turns, "nobody turns to the student before the last line")
        self.assertTrue([t for t in turns if t < congratulation],
                        "he is not turned to the boy he is congratulating")
        self.assertNotIn("actor_move", pump.kinds(seen))

    def test_every_heading_the_films_ask_for_is_derived_and_never_written(self):
        """Headings are derived, never written: `actor_face(x, "thor")` asks the scene.

        A compass point typed here is a bet on where a station sits, and it breaks when
        the station moves in MAPVIS.
        """
        THE_EIGHT = {
            "north", "north-east", "east", "south-east",
            "south", "south-west", "west", "north-west",
        }
        for label, seen in self.films():
            with self.subTest(film=label):
                for turn in pump.only(seen, "actor_face"):
                    # a name is a question the scene answers against the loaded map, so
                    # it moves when the table does. A compass point cannot.
                    self.assertNotIn(turn["facing"], THE_EIGHT,
                                     "a compass point written into a film")
                for word in ("place", "actor_move"):
                    for i in pump.only(seen, word):
                        self.assertIsNone(i.get("facing"))

    def test_no_arrow_is_ever_raised_over_a_region_or_a_door(self):
        """The arrow hangs on the anchor's own pixel, so only stations are pointed at.

        `the_hall`'s pixel sits inside the hearth's drawn fire, so an arrow there would
        point at Advisory instead.
        """
        stations = {"chart_table", "hearth", "trophy_wall", "counselor"}
        for label, seen in self.films():
            with self.subTest(film=label):
                for arrow in pump.only(seen, "guide_to"):
                    if arrow["anchor"] is None:
                        continue
                    self.assertIn(arrow["anchor"], stations)

    def test_the_arrow_and_the_panel_come_down_on_a_road_nobody_wrote(self):
        """`as_a_cutscene` promises the bars, and `as_a_film` the arrow and the panel.

        `open` is a hard refusal when nothing is mounted to hear it, so the film gives
        the room back on the way out.
        """
        for label, handler, ans in (
                ("the opening", "start", answering(refuse=("open",))),
                ("the closing", "talk:principal_desk",
                 finished(handle="Ash", refuse=("open",)))):
            with self.subTest(film=label):
                # watched through the answer, because `pump.run` raises the refusal
                # rather than handing back what it saw
                seen = []
                def watch(intent, ans=ans, seen=seen):
                    seen.append(intent)
                    return ans(intent)
                with self.assertRaises(RuntimeError):
                    pump.run(handler, watch)
                self.assertEqual([i["on"] for i in pump.only(seen, "movie")][-1], False)
                self.assertIsNone(pump.only(seen, "guide_to")[-1]["anchor"])
                self.assertIsNone(pump.only(seen, "objective")[-1]["text"])

    def test_the_panel_is_not_handed_back_under_the_last_button_of_the_year(self):
        """The island keeps its own step on the bar until the last button is pressed.

        Dropping it early with `objective(None)` lets the year's own sentence in over
        the top of the film.
        """
        seen = pump.run("talk:principal_desk", finished(
            handle="Ash", flags=["yearbook:y1", "maw:wall_shown:y1"]))
        at_button = next(n for n, i in enumerate(seen) if i["kind"] == "choose")
        before = [i["text"] for i in seen[:at_button] if i["kind"] == "objective"]
        self.assertEqual(before[-1], "Sail home.")
        self.assertNotIn(None, before)
        # and it is handed back once the press has happened, before the door out
        after = [i["text"] for i in seen[at_button:] if i["kind"] == "objective"]
        self.assertEqual(after[0], None)

if __name__ == "__main__":
    unittest.main()
