# blhs-islands

Every island in the BLHS adventure game, written in Python, one folder each.

You own a folder. Nobody edits it but you, and you never open the engine. What
you write is real Python running inside the real game, next to everybody else's.

**This repo is local-only right now.** There is no GitHub remote yet, because Ash
names it and creates it. Until he does, the `git push` and pull request steps at
the bottom have nowhere to go, and the loader that fetches your island into the
game is still being built. `NEEDS.md` lists exactly what is missing. What works
today is writing an island and testing it.

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

**The engine cannot do this yet.** Nothing in the game asks a loaded island
whether it owns an anchor, so pressing E today does nothing at all. That is
`NEEDS.md` items 1, 2 and 11, and it is the largest single thing between this
repo and a member seeing their island. Write your handlers anyway: the shape is
settled, and `python -m unittest` calls them exactly the way the engine will.

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

In `island.py`, five strings still say `skeleton`, and changing the manifest
without changing these is the first mistake everybody makes:

- **`award(programme="skeleton", ...)`.** This one decides whether a student's
  work lands on the right row of their transcript, and it has to match
  `programme` in your `island.json`. The island cannot read its own manifest yet
  (`NEEDS.md` item 14), so the id is written in two places and it is on you to
  keep them together. `test_says_who_it_finished_for` fails when they drift, and
  the failure names both strings.
- `GREETER_ANCHOR`, which has to match an anchor Ash placed in MAPVIS for your
  map. **Ash has the list.** Nothing in this repo can tell you which anchors your
  map has, and that gap is `NEEDS.md` item 12.
- `GREETER`, which is what the player reads on the plaque.
- the island name in `log(...)`.
- the flag in `set_flag(...)`. Flags are one flat list shared with every island
  in the game, so yours starts with your programme id or it collides with
  somebody else's.

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

**Nothing on the engine side checks any of this yet**, so these two are the only
checks there are. Passing means the format is right and your logic does what you
think. It cannot mean the game will load your island, because today nothing in
the game reads an `island.json` at all.

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

It prints a URL for each island and hands the files to anything that asks. Once
the loader lands you paste that URL into the game as `?scene=grape&from=<url>`
and your island loads off your own disk: edit, reload, different island, nothing
committed and nothing pushed.

The loader is not built yet, so today `serve.py` hands out files and nothing is
asking for them. `NEEDS.md` item 3 is the ask.

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

`vine.py` has nine. They are the ones the vine's own content already asks for,
and `say` and `choose` are the two that have been watched running from Python
inside the game.

| word | what it does |
|---|---|
| `say(text, who=)` | one line in the dialogue box |
| `choose(options, prompt=)` | buttons, comes back as the index picked |
| `open(ui)` | one of the game's panels |
| `play(beat)` | a scored activity the engine builds, comes back as the grade |
| `get(path)` | ask the run about itself |
| `set_flag(flag)` | remember one thing forever. Start it with your programme id: flags are one flat list shared with every island. |
| `award(programme=, grade=)` | the row your island earned. `grade` is 0 to 4.0. |
| `log(event, data=)` | one line on the record |
| `guide_to(anchor)` | the arrow, along ground that can be walked |

The engine understands more than nine. The rest are attached to parts of the game
being built right now, so an island copied from this repo does not use one yet.
Ask before you reach for one, and read the top of `vine.py`.

Three of them come back as something that is not a value. `choose` comes back as
`-1` when nobody answered at all. `play` comes back as `None` when the activity
was never finished. `get` comes back as `None` for everything when there is no
saved run. None of those is a zero and none of them is an index.

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

The push and the pull request do not work yet. There is no remote.

## When you need something that is not here

Do not work around it and do not edit the engine. Add it to the bottom of
`NEEDS.md`, in one sentence saying what you were trying to write. That file is
read.
