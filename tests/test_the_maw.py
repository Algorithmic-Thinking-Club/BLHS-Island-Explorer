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
what the machine can do, so it reaches twenty of the engine's thirty-three
words, `place`, `lead_to`, `actor_face`, `show` and `enter` among them, and
every one of them is checked below to be a word the engine really has rather
than one somebody wished for.

TWO WORDS THIS FILE USED TO NAME HERE ARE NOW ASSERTED ABSENT, which is the
opposite claim and is worth the line. `look_at` is gone because the film rides
the student's own shoulder and a second of the camera somewhere he is not is a
cut in the middle of a cutscene. `cutscene` is gone because the engine's
registry plays a scene an island cannot read; both films here are composed word
by word so a member can see what happens.
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
              refuse=(), year=1, planned=False, **rest):
    """The shared run state, with this file's own spellings kept.

    ONE RUN STATE LIVES IN pump NOW. This used to hold seven paths of its own and
    raise KeyError on anything else, so the day `founding.py` asked `phase` the
    file lost 21 tests to the fixture rather than to the island: `handle` and
    `picks` followed it. The names here stay because sixty-two call sites use
    them, and `picks` means the buttons a player presses, which the engine calls
    a choose queue and not the year's picks.
    """
    return pump.answering(
        refuse=refuse, choices=picks, score=score,
        flags=flags, cord_board=board, trophies=trophies or {"stickers": [], "badges": []},
        advisory=advisory, mode=mode, year=year, planned=planned, **rest)


# WHAT "HE HAS BEEN HERE BEFORE" IS SPELLED AS. The latch the arrival reads is
# `maw:railed` (founding.py:113, gated at island.py:148 and :215), and
# `maw:founding` only controls the tunnel beat INSIDE the opening. Six tests here
# passed the wrong one, so the island replayed its whole introduction and then
# they asserted it had not happened. Assertions that the founding flag gets
# WRITTEN are untouched, because that is a different question.
RAILED = "maw:railed"
FOUNDING = "maw:founding"

# and what says the opening is OVER, written one line after the bars come down.
# It is a third name and not a spare: `maw:railed` is written just before them,
# so a student who reloads in that gap hears the handover instead of being left
# with three corner buttons nobody introduced. It is also the fence the press
# road into the ending uses (island.py:239).
HANDED_OVER = "maw:handed_over"


def midyear(**kw):
    """An engine with Advisory still owed, which is when the counselor counsels.

    She says the same thing with Advisory done, so this is no longer the fence it
    was: she used to open the yearbook on that run and Ash ruled that out on
    2026-09-08. It stays because a test about the cords should still say which
    half of the year it means, and because Advisory owed is the ordinary one.
    """
    kw.setdefault("advisory", "core:y1")
    return answering(**kw)


# the shape of a run that has finished a year, which is the only thing the
# closing film will play on. `phase` is the sequencer's own answer and
# "yearbook" is its word for a year with the sheet stamped, the beat sat and no
# voyage left; `maw:handed_over` is what says the opening is over, which is the
# fence on the PRESS road (founding.py:125, island.py:239).
def finished(year=1, flags=(), **kw):
    """An engine whose year is done, so the principal can close it."""
    return answering(phase="yearbook", year=year,
                     flags=[RAILED, HANDED_OVER] + list(flags), **kw)


def last(kinds, word):
    """Where a word happens for the LAST time, because the room says several twice.

    Arrival stands the principal in front of whoever walked in and hands him
    straight back before the film has started, so `actor_release` is already in
    the list by the time the film's own one matters. `index` would find the
    wrong one and the assertion would read as though it had passed.
    """
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
            # NOBODY BOUND MEANS `place` REFUSING, not `actor_move`. This road
            # asked for `actor_move` back, which the films moved off years ago,
            # so it drove the ordinary arrival a second time under a label saying
            # it was driving the hard one.
            ("first arrival, the founding", pump.run("start", answering())),
            ("first arrival, nobody bound",
             pump.run("start", answering(refuse=("place",)))),
            ("later arrival", pump.run("start", answering(flags=[RAILED]))),
            ("home, after the page turned", pump.run("start", answering(
                flags=[RAILED, "yearbook:y1"]))),
            # THE CLOSING FILM, WHICH NO ROAD HERE USED TO REACH. It is the only
            # place `actor_move`, `enter` and the last `choose` are said, so
            # three checks in this class were passing over words nobody drove.
            # Pressed rather than walked into, because the load road is fenced by
            # a module latch and an earlier `start` above has already set it.
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
        # READ OUT OF vine.py, not copied from it. The list that stood here had
        # drifted four paths behind the docstring its own comment cited, and six
        # subtests were failing on `phase` and `planned`, which the engine has
        # always answered. See pump.askable.
        askable = pump.askable()
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
        # AND `thor`, WHICH IS THE ONE PLACE IN THE FILMS THAT IS NOT AN ANCHOR.
        # `place(PRINCIPAL, THOR)` and `actor_move(PRINCIPAL, THOR)` mean "beside
        # whoever is standing there", which is how the principal stopped being
        # bound to the tunnel mouth, and no map can carry that name.
        named = room | {"thor"}
        # `at` IS A PLACE TOO. It was left out, so `place`, the one word the
        # opening uses to put a body anywhere, was the word this check could not
        # see. A typo in it is refused on the island's own line in the game.
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
        """The room opens by playing the introduction. Nothing greets anybody.

        BRIEF-YEAR-ONE beat 4 is no longer one line and a panel: it is the second
        half of a film that went up on the beach, and the bars are already up
        when this handler runs. So what holds is the ORDER. The room dresses
        itself, the frame goes up, and the first thing said inside the Maw is
        beat 1's one line from the principal. A room that spoke before the bars
        would be a room talking over whatever the last map was still showing.
        """
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
        """Arrival puts the drawn case up, on every load, whatever is in it.

        THE COUNT USED TO DECIDE THIS AND IT NO LONGER DOES. The room hid the
        shelf whenever the run held nothing, and nothing in year one awards a
        sticker or a badge, so the case was hidden from the title screen to the
        handover and was never once drawn. Ash, 2026-09-07: *"the 'what you earn
        goes up here' asset is still nonexistent."*

        What the old rule was answering is real: the painting has things on its
        shelves, so a first year walked in to a case that LOOKED full. Hiding it
        traded a case that overstates for a wall with a hole in it. A trophy case
        in a school is empty in September and is still a trophy case; the honest
        count is the panel's, and the line at the wall carries no number.

        So what arrival owes the player is the case being there before he walks
        over, and that the room can never take it down.
        """
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
        # `show` is a hard refusal on the offline copy of this room, and before
        # the guard it would have taken the founding with it. The founding is a
        # film with four lines in it now, so the check is that BEAT 1 happened
        # rather than that the room said one thing: counting lines here would be
        # counting the rail and not the guard.
        seen = pump.run("start", answering(refuse=("show",)))
        said = [i["text"] for i in pump.only(seen, "say")]
        self.assertEqual(said[0], "Welcome to Bonney Lake High. Come with me.")
        self.assertIn("show_refused", [i["event"] for i in pump.only(seen, "log")])
        self.assertIn(FOUNDING, [i["flag"] for i in pump.only(seen, "set_flag")])

    def test_walking_in_with_the_year_done_plays_the_ending(self):
        """Coming back in with the year finished is a film, not a line.

        THE LINE THAT WAS HERE IS CUT. The room used to say "Year one is done.
        Year two, next time." on the way in and write `maw:next_time` so it only
        said it once. BRIEF-INTRO-FILM section 4: *"No 'Year two' wording
        anywhere; the intro does not end with a promise about next time."* The
        flag went with it, replaced by `maw:handed_over`, which records something
        that happened rather than something that was said.

        What a student gets instead is Ash's own road, 2026-09-08: *"walking into
        the Maw with the year done starts the ending film."*
        """
        # THE QUIET ROAD FIRST, AND THE ORDER IS NOT A STYLE CHOICE. The room
        # will not start the ending on a load that just played a film, and it
        # remembers that in a module variable which lives as long as the import,
        # so any earlier `start` in this method that played one would make the
        # run below prove nothing.
        #
        # "Once" is the sequencer's job now and not a flag's: the phase leaves
        # "yearbook" the moment the page turns, so the load after the ending gets
        # the quiet room.
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
    """THE OPENING FILM: the tunnel, the sheet, the fire, the wall, the handover.

    Beat 4 used to be the whole of this class, and it was one line and a screen.
    It is five beats inside one set of bars now, and every one of them is the
    principal walking ahead with the student following him, which is what a
    freshman orientation is. `founding.py`'s own header lists them in order.

    TWO ROADS ARE DRIVEN AND THEY ARE BOTH REAL. `self.whole` is the student who
    does everything he is asked, which is the only road that reaches the
    handover. `self.stepped_off` is the one who closes the schedule and keeps
    closing it, which the film has to survive because closing a screen is not a
    decision and a rail that walked him on with an empty sheet would have lost
    the one thing it walked him there for.
    """

    def setUp(self):
        self.manifest = pump.load(ISLAND)
        self.whole = pump.run("start", answering(planned=True, advisory="core:y1"))
        self.stepped_off = pump.run("start", answering())

    def test_the_principal_appears_in_front_of_whoever_walked_in(self):
        """He is PLACED at the student, and no anchor is named at all.

        ASH, 2026-09-08: *"he pops up in front of thor at any time. he isnt bound
        to the entrance of the maw."* It took three tries to get here and both
        dead ends are worth keeping written down. The first WALKED him over, and
        the walk crossed the gap between the bridge and the floor, so Ash saw a
        man flying across the edge. The second placed him at the tunnel, which is
        right for a student who has just come in and wrong for every other
        moment: a student who finished his year at the fire and pressed him got a
        man who materialised across the room and had to walk back.

        `place(PRINCIPAL, THOR)` names the player as a PLACE, so the scene
        happens wherever the student is standing and no beat in the film has to
        know where that is.
        """
        placed = [(i["actor"], i["at"]) for i in pump.only(self.whole, "place")]
        self.assertEqual(placed[0], ("principal_desk", "thor"))
        # and nothing in the opening carries a body straight at a target. That
        # word belongs to the closing film, where he really does cross the room.
        self.assertEqual(pump.only(self.whole, "actor_move"), [])

    def test_he_is_standing_there_before_the_camera_moves_or_he_speaks(self):
        # the order `opening()` was written for: placed, then the shot comes in
        # on the two of them, then he talks. Placed after the camera there would
        # be a frame of him still at his desk while the shot travels in, and
        # talking before either is a voice over an empty room.
        kinds = pump.kinds(self.whole)
        self.assertLess(kinds.index("place"), kinds.index("view"))
        self.assertLess(kinds.index("view"), kinds.index("say"))

    def test_one_line_per_beat_and_never_two(self):
        """lines.py's rule: one person says one thing before the thing happens.

        Ash after playing the version with three lines a beat: *"a bunch of
        words, a bunch of instructions that open to read more words. A student
        doesn't know what the hell is going on."* So the number to count is not
        one, it is the number of beats that SPEAK on a road nobody steps off: the
        tunnel, the fire, the wall and the handover. The sheet is silent here
        because it was already stamped when he walked in.

        The recovery lines are the exception the rule names. STAMP_IT and
        COME_BACK are only ever said to somebody who closed a screen, and nobody
        who finishes a beat hears one.
        """
        said = [i["text"] for i in pump.only(self.whole, "say")]
        self.assertEqual(len(said), 4)
        self.assertEqual(len(set(said)), 4)
        # AND IT IS NOT THE ENGINE'S CANNED CUTSCENE. `cutscene` plays a scene
        # out of the registry, which no island can see inside; this film is
        # composed word by word here, so a member can read what happens.
        self.assertEqual(pump.only(self.whole, "cutscene"), [])
        # AND THE CAMERA NEVER CUTS AWAY. The first rail sent it to each station
        # for a second before setting off, which is a cut in the middle of a
        # cutscene; the whole film rides the student's own shoulder now.
        self.assertEqual(pump.only(self.whole, "look_at"), [])

    def test_the_principal_has_a_face_on_the_line(self):
        for line in pump.only(self.whole, "say"):
            self.assertEqual(line.get("portrait"), "principal")

    def test_it_writes_the_bare_flags_the_engine_sequences_off(self):
        """Year one's flags, in the order the film writes them, every one unscoped.

        `src/game/run/objective.ts` sequences the whole of year one off these
        exact strings, and the light that tells a student what to do next sits on
        the desk until `maw:founding` is written. This island is the vine's own
        content and the engine runs it unscoped, so a flag written the way a
        MEMBER's island writes one would land as `the-maw:founding` and the light
        would stay on that desk for four years with nothing saying why.
        """
        flags = [i["flag"] for i in pump.only(self.whole, "set_flag")]
        self.assertEqual(flags, [
            "maw:founding", "vignette:y1", "maw:wall_shown:y1", "maw:railed",
            "handbook:granted", "chart:granted", "maw:handed_over",
        ])
        for flag in flags:
            self.assertFalse(flag.startswith(self.manifest["programme"] + ":"), flag)

    def test_the_corner_arrives_after_the_bars_and_one_plaque_at_a_time(self):
        """The two grants used to be in beat 1, which is inside the movie now.

        The frame HIDES the corner rather than dimming it, so written at the
        start they were written on the one stretch of the game where nobody could
        see them arrive, and `inventory.ts` fires its arrival flourish once per
        flag. Written at the end, on the frame the student gets the room.

        AND THE WAIT BETWEEN THEM IS THE BEAT. Both flags on one frame is a
        single flicker rather than a corner filling up.
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
        """Beat 1's two flags are the year's own light; the arrow goes on top.

        `src/game/run/objective.ts` reads those two and puts its light on the
        chart table, and `take_him` raises the rail's own arrow over the same
        table a moment later, so the thing a student is walked to is lit before
        he is walked to it. The wait that used to be the middle of this
        assertion has moved to the handover, where it separates the two corner
        grants; a light being SEEN is not what a wait is for here, because the
        student is watching a man set off towards it.
        """
        kinds = pump.kinds(self.stepped_off)
        self.assertLess(kinds.index("set_flag"), kinds.index("guide_to"))
        self.assertLess(kinds.index("guide_to"), kinds.index("open"))
        self.assertEqual(pump.only(self.stepped_off, "guide_to")[0]["anchor"], "chart_table")
        self.assertEqual({i["ui"] for i in pump.only(self.stepped_off, "open")}, {"planner"})

    def test_every_arrow_it_raises_is_taken_down_before_it_lets_go(self):
        """An arrow left up sits over the last station for the rest of the run.

        This used to say the founding raised none at all, which was true when the
        beat was one line and a screen. The rail points at every station it takes
        him to and that is the teaching: a student who reads nothing still sees
        the light on the floor. So the rule holds at the other end instead. The
        last thing every road out of the film says about the arrow is
        `guide_to(None)`, which hands the pointing back to the year, and the year
        has something to say the moment the bars come down.
        """
        for label, seen in (("the whole film", self.whole),
                            ("stepped off at the schedule", self.stepped_off)):
            with self.subTest(road=label):
                arrows = pump.only(seen, "guide_to")
                self.assertTrue(arrows)
                self.assertIsNone(arrows[-1]["anchor"])

    def test_he_is_let_go_after_the_last_panel_and_never_walked_home(self):
        # measured in a browser, twice. Walked back UNDER a panel, the walk
        # waited (nothing moves under a panel) and then ran for five seconds
        # with this handler still open, and an open handler drops every press
        # in the room. Walked back BEFORE the panel to his own anchor, he moved
        # twelve pixels: a bound anchor's stand point travels with the body, so
        # no name on this room means "home". Released after the panel, the
        # handler is over the moment it is up. founding.py has the whole of it.
        #
        # AND THE CAMERA COMES BACK AFTER HIM, in that order, because `view` is
        # what ends the shot the release happened inside.
        for label, seen in (("the whole film", self.whole),
                            ("stepped off at the schedule", self.stepped_off)):
            with self.subTest(road=label):
                kinds = pump.kinds(seen)
                released = last(kinds, "actor_release")
                self.assertLess(last(kinds, "open"), released)
                self.assertLess(released, last(kinds, "view"))
                self.assertEqual(pump.only(seen, "actor_move"), [])

    def test_a_room_with_nobody_bound_still_gets_its_founding(self):
        """THE OFFLINE COPY OF THIS ROOM BINDS NO PLACEMENTS.

        Every word that touches a body is a hard refusal there, and a refusal is
        raised at the line that asked, so one uncaught one would take the lines,
        the flags and the screens with it and year one would replay on every
        visit forever. The game falls back to that copy whenever it cannot reach
        the platform, so this is not a hypothetical room.

        THE WORD THIS USED TO REFUSE WAS `actor_move`, which the film stopped
        saying when the principal stopped being walked over. So the guard was
        being proved by refusing a word nobody yields, which proves nothing at
        all. Refusing all six is what the offline bundle really does.
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
        """A student who pressed E on him is standing in front of him already.

        `rail(walk=False)` is the whole of it. Beat 1 skips the placing, because
        putting a body where the student is standing shoves a man who is already
        there a body length sideways, and it logs which road it came in by so
        the two arrivals are told apart on the record.
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
        """He reads the run and says one thing. Nothing is performed.

        THE QUESTIONS ARE NOT COUNTED HERE any more, which is the change. He
        asks three now (the latch, the year, and whether the year is done) and a
        fourth would be no worse, because a `get` costs a student nothing. What
        must never come back is the film: a press once the introduction has
        played cannot put the bars up on a room he has been walking around in.
        """
        again = pump.run("talk:principal_desk", answering(flags=[RAILED]))
        self.assertEqual([k for k in pump.kinds(again) if k != "get"], ["say"])


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
        # THE ONE THAT BROKE HER. Both GPA bands move on the very first grade and
        # keep moving for four years, so sorted by progress alone they are the
        # only two cords she would ever name, in any year, on any run.
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
        # THE CORDS PAGE, NOT THE ISLANDS ONE (Ash, 2026-09-09). `open("handbook")`
        # always lands on Islands, so the one beat in this game whose whole
        # subject is the cords opened the page about islands. The panel name is
        # half of what this test holds: asking her and getting the wrong page is
        # no better than asking her and getting nothing.
        yes = pump.run("talk:counselor", midyear(picks=[0]))
        no = pump.run("talk:counselor", midyear(picks=[1]))
        self.assertEqual([i["ui"] for i in pump.only(yes, "open")], ["cords"])
        self.assertEqual(pump.only(no, "open"), [])

    def test_nobody_answering_is_not_the_first_button(self):
        # -1 is the player walking off while the buttons are up
        gone = pump.run("talk:counselor", midyear(picks=[-1]))
        self.assertEqual(pump.only(gone, "open"), [])

    def test_she_never_starts_the_ending_however_finished_the_year_is(self):
        """ASH, 2026-09-08: *"the counselor never starts it."*

        SHE USED TO OPEN THE YEARBOOK HERSELF and that deleted the ending
        outright: the page turning is the flag the closing film's own trigger
        goes false on, and hers was the most likely press in the room. Then she
        started the film instead, which was better and still wrong, because the
        closing is the principal coming to FIND you and a student who wanders
        over to her first should not trigger a man walking up behind him. Two
        doors into one film is one door too many, and she is in the film anyway.

        So she says the same thing whatever the run holds, and the year being
        over is the objective bar's to announce and the principal's to act on.
        """
        for label, ans in (("advisory done, page not turned",
                            answering(advisory=None)),
                           ("the whole year done",
                            answering(advisory=None, phase="yearbook"))):
            with self.subTest(run=label):
                seen = pump.run("talk:counselor", ans)
                self.assertEqual(pump.only(seen, "movie"), [])
                self.assertEqual([i["ui"] for i in pump.only(seen, "open")], ["cords"])
                # and she turns no page, which is the thing that used to cost the
                # whole ending
                self.assertEqual(pump.only(seen, "set_flag"), [])
                self.assertIn("No cord started yet", pump.only(seen, "say")[0]["text"])

    def test_after_the_page_has_turned_she_counsels_again(self):
        seen = pump.run("talk:counselor", answering(
            advisory=None, flags=["yearbook:y1"], picks=[1]))
        self.assertEqual(pump.only(seen, "open"), [])
        self.assertIn("No cord started yet", pump.only(seen, "say")[0]["text"])


# REAL BUG: `well_done` spells the year out, and no test below fails on it.
#
# The closing film's FIRST line is `well_done(handle, picks)` in founding.py, and
# its bare shape is lines.py's WELL_DONE_BARE, "%s, that is your first year at
# Bonney Lake." Said in any year. That is the same defect Ash reported on
# 2026-09-09 (*"I finished year 2, and it says 'year one is done' everywhere"*)
# and `well_done_now`, two functions below it, was fixed for it while this one was
# not: it asks for the year and this one does not.
#
# WHY IT IS A LINE HERE AND NOT AN ASSERTION. The bare shape only fires when the
# student picked no classes and no seasons, and a year cannot reach phase
# "yearbook" on an unstamped sheet, so nobody can hear it today. A red test over a
# sentence nobody reaches would be noise. The fix is one argument, in a file no
# test in this folder may edit.
#
# AND WHILE READING IT: the film says two congratulations, `well_done` at the top
# and `well_done_now` after the page turns. lines.py's comment at WELL_DONE_BARE
# reads as though the first had been replaced by the second. Ash's own words from
# 2026-09-07 and 2026-09-09 support either, so it is his call and not a defect.
class TheClosingFilm(unittest.TestCase):
    """The other film: he comes to find you, the cord, the page, and the boat.

    IT HAD NO TESTS IN HERE AT ALL, which is how the counselor's own tests came
    to be the only place the yearbook was checked. She stopped opening it on
    2026-09-08 and the rules about the page had nowhere to live, so they were
    asserted of a handler that no longer reads them.

    Both roads in are `island.py`'s: the room loading with the year done, and the
    principal being pressed by a student standing in it. This class presses him,
    because the load road is fenced by a module latch that any earlier run in the
    same test would have set.
    """

    def setUp(self):
        pump.load(ISLAND)

    def test_the_turned_flag_is_the_current_years(self):
        """Year two's page is `yearbook:y2`, and year one's does not close it.

        ASH, 2026-09-09: *"I finished year 2, and it says 'year one is done'
        everywhere."* A bare `yearbook` would mean year one's page closed all
        four years: the film would skip the counselor, skip the cord, and walk a
        student to the boat having shown him nothing.

        This was asked of the counselor while she was the one who read the flag
        to decide whether to open the book. She does not open it at all now, so
        the rule is asked where the flag is really read.
        """
        # year two with year ONE's page turned: she is still owed, and both the
        # year and the cord in her line are the ones he just finished
        seen = pump.run("talk:principal_desk", finished(year=2, flags=["yearbook:y1"]))
        said = [i["text"] for i in pump.only(seen, "say")]
        self.assertIn("Year two is done. Here is your second cord.", said)
        self.assertEqual([i["ui"] for i in pump.only(seen, "open")], ["wall", "yearbook"])
        self.assertIn("maw:wall_shown:y2", [i["flag"] for i in pump.only(seen, "set_flag")])

        # and with year TWO's page turned she is done: nothing opens, and the
        # last thing in the room is the boat
        over = pump.run("talk:principal_desk", finished(
            year=2, handle="Ash", flags=["yearbook:y2", "maw:wall_shown:y2"]))
        self.assertEqual(pump.only(over, "open"), [])
        self.assertEqual([i["map"] for i in pump.only(over, "enter")], ["hub"])

    def test_the_last_press_of_the_year_is_his_and_the_film_waits_on_it(self):
        # ASH, 2026-09-09: *"a big button should pop on the screen, 'Sail Home'."*
        # `choose` draws its options as buttons over the box, so one option is
        # one big button and the film stops until it is pressed. The ending stops
        # being a thing that happens TO a student and becomes the last thing he
        # does, and the door out comes after the press and not before it.
        seen = pump.run("talk:principal_desk", finished(
            handle="Ash", flags=["yearbook:y1", "maw:wall_shown:y1"]))
        kinds = pump.kinds(seen)
        self.assertEqual([i["options"] for i in pump.only(seen, "choose")], [["Sail Home"]])
        self.assertLess(kinds.index("choose"), kinds.index("enter"))
        # and he is let go of before the door, because `enter` tears this island
        # down and a driven body left standing is left standing on the next map
        self.assertLess(last(kinds, "actor_release"), kinds.index("enter"))

    def test_a_page_left_unturned_steps_off_instead_of_sailing(self):
        # closing the yearbook is not finishing the year, so the film hands the
        # room back with the desk still lit rather than putting him on a boat
        # home from a year it cannot close.
        seen = pump.run("talk:principal_desk", finished(handle="Ash"))
        self.assertEqual(pump.only(seen, "enter"), [])
        self.assertEqual(pump.only(seen, "choose"), [])
        self.assertEqual([i["view"] for i in pump.only(seen, "view")], ["close", "walk"])
        self.assertEqual([i["text"] for i in pump.only(seen, "objective")][-1], None)


class TheWall(unittest.TestCase):
    def setUp(self):
        pump.load(ISLAND)

    def test_an_empty_wall_keeps_its_case_and_the_line_says_it_is_empty(self):
        """The case is furniture. The sentence is what carries the emptiness.

        IT USED TO HIDE THE SHELF and that was the wrong answer to a real
        complaint. The painting has things on its shelves, so a first year with
        nothing earned walked in to a case that LOOKED full; hiding it traded a
        case that overstates for a wall with a hole in it, and a hole is worse. A
        trophy case in a school is empty in September and is still a trophy case.
        A student is supposed to see it, want it filled, and read what is in it
        off the panel, which is the whole of "what you earn goes up here" and
        needs the case ON THE WALL to say it.
        """
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
        # THE PICTURE NO LONGER ANSWERS THIS and the line does. The case stays on
        # the wall either way, so `visible` is the same on an empty run and a full
        # one, and asserting it here would have read as a proof of the count
        # while proving nothing. Either list on its own flips the sentence, which
        # is what "together" means: the wall is a shelf and what a shelf says is
        # how full it is, not which kind of thing filled it.
        for trophies in ({"stickers": ["a"], "badges": []},
                         {"stickers": [], "badges": ["c"]}):
            with self.subTest(trophies=trophies):
                seen = pump.run("talk:trophy_wall", answering(trophies=trophies))
                self.assertIn("see what is on it", pump.only(seen, "say")[0]["text"])

    def test_no_number_is_ever_said_at_the_wall(self):
        # the panel counts frames and the line used to count badges, so the
        # two disagreed on one screen; the line carries no number at all now
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
