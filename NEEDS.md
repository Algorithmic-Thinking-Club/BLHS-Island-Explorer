# What this repo needs from the engine

Written 2026-08-29 by the members-repo session. Everything here is an ask on
`AdventureGame`, not work that belongs in this repo. Each one says what is
missing, what it blocks, and where it lands.

The first four block the gate: **a member's island loading off a branch and
running a handler through the real dialogue box.** Nothing in this repo can
prove itself in the game until they exist.

---

## 1. `grape.py` has no home in the engine

The decorators (`on_start`, `on_talk`), the handler registry and `Scored` live
in this repo, at the root, because `src/vine/py/vine.py` belongs to the engine
session for its whole wave and its own test asserts that file holds exactly the
fifteen word builders and nothing else.

That is the right split. But the engine has to ship its own copy of `grape.py`
and write it into the MicroPython filesystem before importing an island, exactly
as it already does for `vine.py`, or the registry the island filled is not the
registry the engine reads. Until then no handler in this repo can ever be called.

**Lands in:** `src/vine/py/grape.py`, written to the runtime in
`grape.worker.ts` beside `vine.py`.

## 2. The protocol cannot call into a grape

`src/vine/py/protocol.ts` is `run | resume` outward and
`intent | print | done | crash` back. The engine can answer a grape and cannot
call one. Three messages are missing:

- `load`, carrying **a map of filenames to source** rather than one name and one
  string, so a multi-file island arrives whole. `runGrape.ts` currently strips
  directories off a single name.
- `ready`, coming back with the handler keys the import registered. The engine
  needs the list and not just the fact, because that list is what lets an anchor
  nobody claims say so by name instead of producing silence a member cannot tell
  from a typo in their own file.
- `call`, firing one handler by name.

Measured while writing this, against `@micropython/micropython-webassembly-pyscript`
1.29.0-6, so none of it is a guess:

- `FS.mkdirTree` exists and is idempotent; `FS.mkdir` throws on an existing
  directory and `FS.writeFile` never creates parents.
- Writing an island to `islands/<id>/` and putting that directory on `sys.path`
  makes `from questions import Quiz` work for a sibling file. A real package with
  `__init__.py` also works but then the sibling import has to be
  `from . import questions`, which is the one sharp edge a beginner would hit.
- The traceback names the member's own file across module boundaries:
  `File "islands/skeleton/questions.py", line 2, in q`.
- `yield from` works, carries a return value out, and a refusal thrown in with
  `generator.throw` lands at the yield inside the inner generator.
- `sys.modules` has to be purged for **every** module the island ships. Dropping
  only the entry means editing a sibling and re-running silently reuses the old
  one.
- `inspect` **does exist** in this build, including `isgenerator`. The comment at
  `driver.py:36` saying it does not is wrong. `type(x).__name__` still works and
  needs no import, so there is no reason to change the check, only the comment.
- `str.isalnum` and `str.isidentifier` do **not** exist. Anchor-name validation
  has to happen on the TypeScript side.

## 3. The loader fetches one file, from the app's own origin

`GrapeProof.tsx` fetches `/grapes/<file>.py`. A member's island is a manifest
plus its modules at a base URL, which is either a branch:

```
https://raw.githubusercontent.com/<owner>/blhs-islands/<branch>/islands/<id>/
```

or their own machine while they work, which is what `serve.py` in this repo
exists for. It sends `Access-Control-Allow-Origin: *` and `Cache-Control:
no-store`, walks up from port 5280 to find a free one, and hands out only `.py`
and `.json`. Verified serving this repo's skeleton.

`tools/manifest.py` is the validation, written as the thing that refuses and
names the field. The engine should run the same rules on what it fetched. The
two that matter most: a `format` number it does not know is refused by number,
and a module named `vine.py` or `grape.py` is refused, because a member's copy
would shadow the engine's on `sys.path`.

**A port note worth keeping.** Port 5275 was already taken by a node dev server
on this machine while I was testing, and a static server that fails to bind does
not fail loudly: the game fetches, gets somebody else's `index.html` back, and
tries to run a page of HTML as an island. That is why `serve.py` walks the port
range, and it is an argument for the loader refusing a response that is not
`.py` or JSON.

## 4. Nothing on the wire has a deadline or a version

Two different clocks, and they are not the same clock:

- **boot**, from `load` to `ready`. MicroPython not starting must not hang.
- **turnaround**, from `call` or `resume` to the worker's next message. This one
  covers the member's Python only. The player's thinking time sits on the engine
  side of a `say`, so the deadline has to be disarmed while an intent is being
  performed, or every slow reader kills their own island.

And a version in both directions. Both halves are built from the same repo, so a
mismatch is a stale cached worker chunk beside a fresh main chunk, which is an
ordinary thing on a school Chromebook that has had the tab open since Tuesday.
The manifest's `format` is the version that matters more, because these two
repositories ship on different days.

---

## Smaller, and each one is a real defect

## 5. A grape cannot tell which arm it is in

`engine.mode()` returns `'game'` with no save. `engine.read('mode')` returns
`null` with no save, because `if (!s) return null` at `intent-engine.ts:34` fires
before the switch reaches `case 'mode'`. So `get("mode")` is `null` in a bare
harness, and `get("year") + 1` throws inside the member's own island.

An island reading `null` as "not plain" accidentally does the right thing, which
is worse than doing the wrong thing, because it is not a rule anybody wrote down.
Either `read()` gets per-case defaults, or the harness gets an arm toggle, and
§80.8 asks for the toggle anyway: *a member harness that renders an island in
both arms on demand.* `tests/test_skeleton.py` has both of these pinned.

## 6. `play` reports success three different ways without performing

`requestBeat` resolves `null` when no HUD is mounted, when the beat id is
unknown, and when the player closed the panel. All three come back as
`{ok: true, value: null}` and a member cannot tell them apart. A typo'd beat id
reporting success is the exact thing `intents.ts:253` was written to outlaw. The
unknown-id branch should refuse so the traceback lands on the member's line; the
player-closed-it case is honestly null.

## 7. Flags are one flat list with no namespace

`intent-engine.ts` passes a grape's flag string straight through. Two members
both shipping `done` collide, silently, in a student's save. This repo's README
tells members to prefix by hand and the skeleton's test checks that it did, which
is a convention, not a fence. P4 is the fence.

## 8. `vine.py` is vendored here and will drift

There is a copy of `vine.py` at the root of this repo, cut down to the nine words
the skeleton is allowed to use. It exists so a member's editor resolves
`from vine import say` and so `python -m unittest` runs with no browser. The
engine overwrites it at runtime, so the drift cannot reach a player, but it can
absolutely waste a member's afternoon.

Ask: publish `vine.py` and `grape.py` somewhere this repo can pull them from, or
add a sync step. Right now the only thing keeping them together is that somebody
remembers.

## 9. The manifest carries none of P18's content fields

`what`, `when`, `how_to_join`, the four-to-six word blurb, one sticker id, real
meeting times and rooms as data, and a sourced-or-explicitly-unknown rule on
every fact. They are not in `island.json` because what is required and what
counts as sourced is a policy call, not a format one, and inventing it here would
be inventing the answer. The member content policy in the README is the prose
half of the same thing and it is also not authoritative.

## 10. A member cannot get onto the roster

`award(programme=...)` with a name nobody is on the roster for keeps the grade,
warns in the console, and never marks the island finished. The skeleton ships
`programme: "skeleton"` deliberately unrostered so a member sees that warning on
day one, because it is the first thing they must fix.

There is no path from "I built an island" to "my programme is in
`src/game/roster/roster.ts`" that does not involve a member opening the engine,
which is the thing the whole design says they never do.

## 11. An anchor that belongs to nobody is silent

W13. A correctly placed anchor, a correctly written handler and a correctly
spelled name produce nothing today, because `PmapScene`'s `fire()` routes doors
to `beginExit` and everything else to `stationByName`, a lookup in the Maw's
eight-entry array, and a miss returns silently. Silence is indistinguishable from
a typo in the member's own file.

The hook is narrow: dispatch is name-based and behind one function. There are
five `stationByName` call sites and a grape router has to be consistent across
all five, or the prompt and the press disagree and E is never even offered.

---

## Members: add yours below

One sentence, saying what you were trying to write when you got stuck.
