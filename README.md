# blhs-islands

Every island in the BLHS adventure game, written in Python, one folder each.

You own a folder. Nobody edits it but you, and you never open the engine. What
you write is real Python running inside the real game, next to everybody else's.

It lives at
[Algorithmic-Thinking-Club/BLHS-Island-Explorer](https://github.com/Algorithmic-Thinking-Club/BLHS-Island-Explorer).
The game loads an island straight off a branch of it, so pushing is how somebody
else sees your work.

---

## What an island is

A folder with an `island.json` in it and some `.py` files next to it.

```
islands/skeleton/
    island.json      who this island is, and which files to load
    island.py        the handlers the game calls
    questions.py     the scored part, kept separate on purpose
```

What your island **asks** is content and **when** it asks is control flow, and
the day you want to change one without reading the other you will be glad they
were apart. That is why it is a folder and not a file.

## The one rule

**A word only happens if you yield it.**

```python
yield say("You made it.")
say("You made it.")
```

The first line appears in the dialogue box and waits for the click. The second
builds a dict, drops it, and nobody ever sees it.

`say` and everything else in `vine.py` builds a dict and does nothing at all. The
engine is on the other side of a worker, and `yield` is how the dict gets to it.
Anything that takes time gets a `yield`. Everything else is just Python.

You get told when you forget. A handler with no `yield` anywhere in it is not a
generator, and the tests name your function and say so.

## The other rule

**Nothing calls your functions. The game does.**

```python
from grape import on_talk
from vine import say

@on_talk("greeter")
def meet_the_greeter():
    yield say("You are the first person up this path all week.", who="the greeter")
```

Nothing anywhere calls `meet_the_greeter`. The player walks up to the anchor
named `greeter`, presses E, and the engine calls it. That is what makes an island
an island instead of a script: it can remember you, it can open differently on a
third visit, and it can answer a door.

`@on_start` runs once when the island loads. `@on_talk("name")` runs when the
player presses E on the anchor with that name in MAPVIS.

The engine calls your handlers today, and you can watch it:
`?scene=grape&from=<your serve.py url>` loads your island and puts a button on
screen for every anchor it registered. What is
still missing is the last hop, on a real painted map: `PmapScene` does not yet
ask a loaded island whether it owns the anchor the player pressed E on, so the
buttons in that harness are standing in for that one press. `NEEDS.md` item 11.

---

## Start here

```
git checkout -b my-island
```

Then copy the skeleton folder and rename the copy to `islands/my-island`. In
PowerShell or Git Bash `cp -r islands/skeleton islands/my-island` does it. In
`cmd.exe` there is no `cp`, so use File Explorer.

Open `islands/my-island/island.py` and start deleting.

**The skeleton is scaffolding, not a good island.** It is not the ATC island and
it is not pretending to be. When that one ships it will be the example worth
copying. This is only the shape: somebody to talk to, a choice that changes what
happens next, something scored, and a row on the player's record.

### Change these first

In `island.json`:

- `programme` and `map`: your ids, lower case with hyphens. They have to be
  different from each other and different from everyone else's.
- `title` and `owner`: yours.

In `island.py`, three strings:

- `GREETER_ANCHOR`, which has to match an anchor Ash placed in MAPVIS for your
  map. If a handler claims a name your map does not have, the game says so by
  name in the console the moment your island loads, and lists the anchors it
  does have.
- `GREETER`, which is what the player reads on the plaque.
- the flag in `set_flag(...)`, which is whatever you want to remember.

Your programme id is NOT one of them. The island reads it out of your own
`island.json` with `manifest()["programme"]`, so it is written once. Two copies
of one id drift, and when they do a student's grade lands on somebody else's
row.

## Run it

```
python -m unittest
python tools/manifest.py islands/my-island
```

Run both **from the repo root**. `python -m unittest` from inside your own folder
prints `OK` having run nothing at all.

They check different things and you want both:

- `tools/manifest.py` checks `island.json` against the package format and names
  the field it is unhappy about. Give it a folder to check only yours, or no
  arguments to sweep the repo.
- `python -m unittest` imports every island and drives your handlers.

The game runs the same manifest rules on what it fetched, so failing here means
failing there. It does not work the other way round: passing means the format is
right and your logic does what you think, and the only thing that can tell you
your island is any good is playing it.

`tests/pump.py` is what runs your island without the game. It sends the answers
your test decides on and hands back everything your island asked for, so you can
check that the right branch ran and the score came out right. Copy
`tests/test_skeleton.py` to `tests/test_my_island.py` and point it at your
folder. **Underscores, and the name has to start with `test`**, or `unittest`
skips the whole file without saying so.

It proves your logic and nothing else. In there nothing performs anything, so a
green test and a broken island are perfectly compatible.

## See it in the game

```
python serve.py
```

It prints a URL for each island. Paste it into the game after `?scene=grape&from=`:

```
http://localhost:5173/?scene=grape&from=http://localhost:5280/islands/my-island/
```

Your island loads off your own disk. Edit a file, reload the page, different
island. Nothing is committed and nothing is pushed, and only your machine can
reach it. Add `&arm=plain` to see what the other half of the class sees.

**And once you have pushed, anybody can open your branch**, which is how you show
somebody your island without them cloning anything:

```
?scene=grape&gh=Algorithmic-Thinking-Club/BLHS-Island-Explorer@my-island:islands/my-island
```

That reads the branch, not `main`, so what they see is what you pushed.

The port the game is on is whatever `npm run dev` printed, and `serve.py` prints
its own. If the game shows a page of HTML where your island should be, something
else is on the port you used, and the error will say so.

---

## The manifest

```json
{
  "format": 1,
  "programme": "skeleton",
  "map": "skeleton-shore",
  "title": "The Skeleton",
  "season": "Fall",
  "owner": "atc",
  "entry": "island.py",
  "modules": ["island.py", "questions.py"]
}
```

| field | what it is |
|---|---|
| `format` | which version of this file shape. Do not change it. |
| `programme` | the thing a student does here. This is what `award()` names. |
| `map` | the painting your island is played on. A different key space from `programme`, and the two may never be the same string. |
| `title` | what a person reads. One line, under 80 characters. |
| `season` | `Fall`, `Winter` or `Spring`, or leave it out when your island is not seasonal |
| `owner` | you |
| `entry` | the file with your handlers in it |
| `modules` | every `.py` file the game should fetch. A file you forget to list is never fetched, and the import then fails inside the game and nowhere else. |

An island is one flat folder. No subfolders, no `.py` file that is not in
`modules`, and no file named `vine.py`, `grape.py` or anything Python already
uses like `random.py` or `json.py`.

## The words

`vine.py` has twenty-five, which is everything the engine understands. These nine
are what the skeleton uses, and they are the ones that have been watched working
from Python inside the game:

| word | what it does |
|---|---|
| `say(text, who=)` | one line in the dialogue box |
| `choose(options, prompt=)` | buttons, comes back as the index picked |
| `open(ui)` | one of the game's panels |
| `play(beat)` | a scored activity the engine builds, comes back as the grade |
| `get(path)` | ask the run about itself |
| `set_flag(flag)` | remember one thing forever. The engine puts your programme id in front of it, so yours cannot collide with anybody else's. |
| `award(programme=, grade=)` | the row your island earned. `grade` is 0 to 4.0. |
| `log(event, data=)` | one line on the record |
| `guide_to(anchor)` | the arrow, along ground that can be walked |

The other sixteen move the world and direct a scene. Six of them have been there
a while: `walk_to`, `look_at`, `show`, `fx`, `enter` and `cutscene`. Ten more are
for DIRECTING rather than walking through: `pose` and `wait` and `wait_for` and
`sound`, `route` and `framing` for a line or a shot somebody drew on the map in
MAPVIS, and `actor_move`, `actor_face`, `actor_look` and `actor_release` for
driving somebody who is already standing there.

They all need a map, so none of them does anything in a test. Read the top of
`vine.py`, and if one refuses, the refusal will say why on your own line, with a
list of the names that map really does carry.

**`islands/panther-maw/` is the worked example for a room-sized island.** It is
the game's own home base, written in this same python against these same words,
and it is here to be read rather than copied: it is the machine, not your first
file. `tests/test_the_maw.py` beside it is what testing an island of that size
looks like. The one you copy to start is the skeleton, and after that the ATC
island.

It does not use all twenty-five. It uses twelve: `say` with a face on it,
`choose`, `get`, `open`, `play`, `set_flag`, `log`, `show`, `look_at`,
`actor_face`, `cutscene` and `wait`. What it shows that a short island cannot is
the SHAPE: seven handlers on one map, content in one file and control flow in
another, and one scene long enough to live in its own file and be pulled in with
`yield from`.

The other thirteen are in `vine.py` with what each one does. For `route`,
`framing`, `pose`, `guide_to`, `wait_for` and `sound` inside one running scene,
read the beach opening in the engine at `public/grapes/castaway/island.py`. The
Maw does not use those because the room it is written for carries no drawn paths
and no named camera shots yet, and a word aimed at a name the map does not have
is refused on the line that asked for it.

`python tools/sync.py` pulls `vine.py`, `grape.py` and the vine's own islands
from the engine. You should not need it: the copies here are current when you
clone. Whoever changed the engine runs it.

Two of them come back as something that is not a value. `choose` comes back as
`-1` when nobody answered at all, and `play` comes back as `None` when the player
closed the activity without finishing it. Neither is a zero and neither is an
index. A `play` that could not run at all does not come back: it is refused, and
the refusal is raised on your own line.

## The scored thing renders twice

Half the class plays the game and half reads the same content as plain text with
a plain check. The whole study is the comparison between those two halves, and it
only means anything if both halves are reading **the same thing**.

So anything you score subclasses `Scored` and writes `as_plain()`. Same
questions, same options, same order. What changes between the two is who is
speaking and what happens around it, never what is asked. Read
`islands/skeleton/questions.py`, then read the test called
`test_asks_the_same_questions_in_both_arms`, which is the one test every island
needs and which will fail the moment the two arms drift apart.

This is in from the first day because it cannot be added later.

## What you may not put in an island

These are not style notes. Each one reaches a real student.

- **No fact about BLHS without a source.** Not a meeting time, not a room number,
  not a coach's name. If nobody has told us, it is not in the game.
- **Anything you invented is marked as invented**, in the data, not in a comment.
- **No island invents an award, a cord or a criterion.** Those came from the
  school and their gaps are written down as gaps.
- **No island gets its own rival**, and no island names a real neighbouring
  school as an opponent. That is a district and permission question and nobody
  has asked it. Your school's own JV against Varsity is real and costs nothing.
- **No scored thing takes a timing input.** Reaction time confounds the whole
  study, and an island with a stopwatch in it leaves the study.
- **No streak mechanic**, and no scored item whose right answer depends on who is
  playing.

## When you finish

```
git add islands/my-island tests/test_my_island.py
git commit -m "the tide pool island talks and scores"
git push -u origin my-island
```

Then open a pull request. **Ash reads every island before it reaches a student**,
and what he is reading for is the `award`: whether the programme is on the roster
and whether the grade a student can get is the grade they earned.

## Getting on the roster

Until your island has a row in `islands.json` at the root of THIS repo, the game
cannot see it. `python tools/manifest.py` tells you so, and it is not an error:
build for as long as you like before anybody merges anything.

The row is your programme as the rest of the game sees it:

```json
{
  "programme": "tide-pool", "map": "tide-pool-shore", "folder": "my-island",
  "name": "Tide Pool Club", "place": "atc-room", "kind": "club",
  "tags": [], "playable": true,
  "blurb": "Thursdays, and everybody gets wet.",
  "host": "Ms. Berwick",
  "source": "blhs.sumnersd.org/activities/clubs-activities, read 2026-09-04"
}
```

`programme` and `map` have to match your `island.json`, and the checker says so
when they do not. `source` is where the blurb and the host came from, and there
is no version of this without one.

You add the row here. Ash merges it and carries it into the engine with
`tools/sync.py`. **You never open the engine**, which is the whole point.

## When you need something that is not here

Do not work around it and do not edit the engine. Add it to the bottom of
`NEEDS.md`, in one sentence saying what you were trying to write. That file is
read.
