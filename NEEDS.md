# What this repo needs from the engine

Written 2026-08-29, while this repo was built. Everything here is an ask on
`AdventureGame`, not work that belongs in this repo. Each one says what is
missing, what it blocks, and where it lands.

**Items 1, 2, 3, 4 and 13 are DONE, 2026-08-29.** The skeleton island now loads
out of this repo over HTTP, through `serve.py`, and runs `@on_talk("greeter")`
in the real dialogue box, in both arms, with a crash in one handler leaving the
island's other handlers working. They are kept below rather than deleted,
because each one records what was measured to get there and the next person to
touch that code should not have to measure it again. What is still open starts
at item 5.

---

## 1. `grape.py` has no home in the engine — DONE

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

## 2. The protocol cannot call into a grape — DONE

`src/vine/py/protocol.ts` is `run | resume` outward and
`intent | print | done | crash` back. The engine can answer a grape and cannot
call one. Three messages are missing:

- `load`, carrying **a map of filenames to source** rather than one name and one
  string, so a multi-file island arrives whole. `runGrape.ts:97` currently strips
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
- `sys.modules` has to be purged for **every** module the island ships, and
  **every module the previously loaded island shipped**. This repo's own harness
  had that bug: leave the last island's modules or its folder reachable and
  island B imports island A's file, the test suite goes green, and the engine
  refuses it. `tests/pump.py:43-72` is the fixed version and the shape to copy.
- `inspect` **does exist** in this build, including `isgenerator` and
  `isgeneratorfunction`, so the old comment in `driver.py` saying it does not was
  wrong. It is also the wrong tool: measured, `isgeneratorfunction` answers False
  for a bound method AND for a **closure**, and a closure is what every decorator
  returns, so convicting on a False told a member whose handler was wrapped in
  their own decorator that it had no yield in it. What this build does have is a
  type name: a `def` containing a yield is type `generator` before it is ever
  called, a plain one is `function`, a closure is `closure` either way. So
  `function` is the only case that can be convicted without running anything.
  `scripts/mp-guard-spike.mjs` in the game repo is the measurement, and CPython
  has no equivalent, which is why `tests/pump.py` here judges the call instead.
- `str.isalnum` and `str.isidentifier` do **not** exist. Anchor-name validation
  has to happen on the TypeScript side.

## 3. The loader fetches one file, from the app's own origin, and validates nothing — DONE

`GrapeProof.tsx:57-73` gates a `?py=` parameter and fetches a single
`/grapes/<file>.py` from the app's own origin. There is no reader for an
`island.json` anywhere in `src/`. A member's island is a manifest plus its
modules at a base URL, which is either a branch:

```
https://raw.githubusercontent.com/<owner>/blhs-islands/<branch>/islands/<id>/
```

or their own machine while they work, which is what `serve.py` in this repo
exists for. It sends `Access-Control-Allow-Origin: *` and `Cache-Control:
no-store`, walks up from port 5280 to find a free one, hands out only `.py` and
`.json`, and answers a folder URL with that folder's `island.json`. Verified
serving this repo's skeleton.

`tools/manifest.py` is the validation, written as the thing that refuses and
names the field, and `grape-source.ts` now runs the same rules on what it
fetched. The two lists that decide those rules had drifted by four names within a
day, so `tests/test_vine_matches_the_engine.py` compares them directly rather
than trusting them. The ones that matter most:

- a `format` that is not a whole number equal to 1 is refused **by number**.
  Note `True == 1` in Python, so the check needs a type guard, and this repo's
  first version did not have one.
- a module named `vine.py` or `grape.py` is refused, because a member's copy
  would shadow the engine's on `sys.path`.
- a module named `random.py`, `json.py` or anything else Python already has is
  refused, because it replaces the real one for everything in that runtime.
- an island is one flat folder: no subdirectories, and every `.py` on disk is in
  `modules`.

**A port note worth keeping.** Port 5275 was already taken by a node dev server
on this machine while I was testing, and a static server that fails to bind does
not fail loudly: the game fetches, gets somebody else's `index.html` back, and
tries to run a page of HTML as an island. That is why `serve.py` walks the port
range, and it is an argument for the loader refusing a response whose content
type is not JSON or plain text.

## 4. Nothing on the wire has a deadline or a version — DONE

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

## Still open. Smaller, and each one is a real defect

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

`intent-engine.ts:48-50` passes a grape's flag string straight through. Two
members both shipping `done` collide, silently, in a student's save. This repo's
README tells members to prefix by hand, in the word table and in the list of
things to change first, and the skeleton's test derives the expected prefix from
the manifest. That is a convention with a test behind it, which is not a fence.
P4 is the fence.

## 8. `vine.py` is vendored here, and it has already drifted once

There is a copy of `vine.py` at the root of this repo, cut down to the nine words
the skeleton is allowed to use. It exists so a member's editor resolves
`from vine import say` and so `python -m unittest` runs with no browser.

**The drift can reach a player and it already started.** This repo's first commit
gave `say` a `portrait=` argument the engine's `say(text, who=None)` does not
have. A member writing `say(..., portrait="x")` would have got a green test here
and a `TypeError` in the game, on a line that looks correct. Fixed, and
`tests/test_vine_matches_the_engine.py` now compares every signature against
`../AdventureGame/src/vine/py/vine.py` when a checkout is next door and skips
loudly when it is not.

Ask: publish `vine.py` and `grape.py` somewhere this repo can pull from, or add a
sync step, so the check is a formality rather than the only thing holding them
together.

## 9. The manifest carries none of P18's content fields

`what`, `when`, `how_to_join`, the four-to-six word blurb, one sticker id, real
meeting times and rooms as data, and a sourced-or-explicitly-unknown rule on
every fact. They are not in `island.json` because what is required and what
counts as sourced is a policy call, not a format one, and inventing it here would
be inventing the answer. The member content policy in the README is the prose
half of the same thing and it is also not authoritative.

## 10. A member cannot get onto the roster

`award(programme=...)` with a name nobody is on the roster for keeps the grade,
warns in the console at `intent-engine.ts:78`, and never marks the island
finished. The skeleton ships `programme: "skeleton"` deliberately unrostered so a
member sees that warning on day one, because it is the first thing they must fix.

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
**five** `stationByName` call sites and a grape router has to be consistent
across all of them, or the prompt and the press disagree and E is never even
offered. The one that decides whether the prompt appears at all is the
availability test that sets `canFire`.

## 12. Nothing tells a member which anchors their map has

The other half of item 11, on the authoring side rather than the runtime one. A
member types a name into `@on_talk("...")` and has no way to know whether that
anchor exists, and `tools/manifest.py` will happily accept a `map` id for a
painting nobody has made. So a typo and a correct name look identical before the
game runs and identical after it, which is two invisible failures stacked.

Cheapest fix: export an anchor list per map out of MAPVIS into this repo as data,
and have `tools/manifest.py` warn when an `@on_talk` name is not in the file for
the declared map. Until then the README says the list comes from Ash.

## 13. The forgotten-yield check runs the member's body first — DONE

`driver.py:34` calls `getattr(__import__(module), entry)()` and then checks
`type(_gen).__name__ != "generator"`. For a handler with no `yield` in it that
call runs the entire function body, so every side effect happens and only then is
the member told nothing ran. `inspect.isgeneratorfunction` exists in this build
and answers before the call. `tests/pump.py:96-101` does it that way and has a
test that the body did not run.

## 14. An island cannot read its own manifest

`award(programme="skeleton")` in `island.py` and `"programme": "skeleton"` in
`island.json` are the same id written twice, and nothing but a test keeps them
together. Measured by walking the README's own path: a member who changes the
manifest and not the code ships an island whose grade lands on somebody else's
row, or on no row at all.

The manifest is already fetched by the loader, so handing it to the island costs
one `globals.set` in the worker. Something like a `manifest()` word, or a module
constant the driver fills in before the import. Then `programme` is written once
and the two cannot drift.

---

## Members: add yours below

One sentence, saying what you were trying to write when you got stuck.
