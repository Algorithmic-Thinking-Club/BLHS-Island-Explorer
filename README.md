# blhs-islands

Every island in the BLHS adventure game, written in Python, one folder each.

You own a folder. Nobody edits it but you, and you never open the engine. What
you write is real Python running inside the real game, next to everybody else's.

---

## What an island is

A folder with an `island.json` in it and some `.py` files next to it.

```
islands/skeleton/
    island.json      who this island is, and which files to load
    island.py        the handlers the game calls
    questions.py     the scored part, kept separate on purpose
```

It is more than one file because it should be. What your island **asks** is
content and **when** it asks is control flow, and the day you want to change one
without reading the other you will be glad they were apart.

## The one rule

**A word only happens if you yield it.**

```python
yield say("You made it.")     the line appears, and you wait for the click
say("You made it.")           a dict gets built, dropped, and nobody sees it
```

`say` and everything else in `vine.py` builds a dict and does nothing at all.
The engine is on the other side of a worker, and `yield` is how the dict gets to
it. Anything that takes time gets a `yield`. Everything else is just Python.

You get told when you forget. A handler with no `yield` in it is not a generator
and the game says so, by name, before anything runs.

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
named `greeter` and presses E, and the engine calls it. That is what makes an
island an island instead of a script: it can remember you, it can open
differently on a third visit, and it can answer a door.

`@on_start` runs once when the island loads. `@on_talk("name")` runs when the
player presses E on the anchor with that name in MAPVIS.

---

## Start here

```
git checkout -b my-island
cp -r islands/skeleton islands/my-island
```

Then open `islands/my-island/island.py` and start deleting. The skeleton has one
of everything and no more: somebody to talk to, a choice that changes what
happens next, something scored, and a row on the player's record.

**The skeleton is scaffolding, not a good island.** It is not the ATC island and
it is not pretending to be. When that one ships it will be the example worth
copying. This is only the shape.

### Change these first

In `island.json`:

- `programme` and `map`: your ids. They have to be different from each other,
  lower case with hyphens, and different from everyone else's.
- `title`, `owner`: yours.

In `island.py`: the anchor name in `@on_talk(...)` has to match an anchor Ash
placed in MAPVIS for your map. If nothing happens when you press E, that is the
first thing to check.

## Run it

```
python -m unittest              your island's logic, no game and no browser
python tools/manifest.py        is island.json right
```

`tests/pump.py` is what runs your island without the game. It sends the answers
your test decides on and hands back everything your island asked for, so you can
check that the right branch ran and the score came out right. Copy
`tests/test_skeleton.py` and point it at your folder.

It proves your logic and it proves nothing else. In there nothing performs
anything, so a green test and a broken island are perfectly compatible. The game
is still the only place your island really runs.

## See it in the game

```
python serve.py
```

It prints a URL for each island. Paste it into the game as
`?scene=grape&from=<url>` and your island loads off your own disk. Edit, reload,
different island. Nothing is committed and nothing is pushed.

**The game side of this is still being built.** The loader that fetches an
island from a URL is not finished yet, so today `serve.py` hands out the files
and nothing is asking for them. `NEEDS.md` says exactly what is missing. Until it
lands, `python -m unittest` is how you know your island works.

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
| `title` | what a person reads |
| `season` | `Fall`, `Winter` or `Spring`, or leave it out when your island is not seasonal |
| `owner` | you |
| `entry` | the file with your handlers in it |
| `modules` | every `.py` file the game should fetch. A file you forget to list is never fetched, and the import then fails inside the game and nowhere else. |

`python tools/manifest.py` checks all of it and names the field it is unhappy
about. The engine runs the same rules when it fetches your island, so passing
here is passing there.

## The words

`vine.py` has nine. They are the ones that have been watched working end to end.

| word | what it does |
|---|---|
| `say(text, who=)` | one line in the dialogue box |
| `choose(options, prompt=)` | buttons, comes back as the index picked |
| `open(ui)` | one of the game's panels |
| `play(beat)` | a scored activity the engine builds, comes back as the grade |
| `get(path)` | ask the run about itself |
| `set_flag(flag)` | remember one thing forever |
| `award(programme=, grade=)` | the row your island earned |
| `log(event, data=)` | one line on the record |
| `guide_to(anchor)` | the arrow, along ground that can be walked |

The engine understands more than nine. The rest are attached to parts of the
game being built right now, so an island copied from this repo does not use one
yet. Ask before you reach for one, and read the top of `vine.py`.

Two of them come back as something that is not a value. `choose` comes back as
`-1` when nobody answered at all, and `play` comes back as `None` when the
activity was never finished. Neither of those is a zero and neither is an index.

## The scored thing renders twice

Half the class plays the game and half reads the same content as plain text with
a plain check. The whole study is the comparison between those two halves, and
it only means anything if both halves are reading **the same thing**.

So anything you score subclasses `Scored` and writes `as_plain()`. Same
questions, same options, same order. What changes between the two is who is
speaking and what happens around it, never what is asked. Look at
`islands/skeleton/questions.py`, and look at the test called
`test_asks_the_same_questions_in_both_arms`, which is the one test every island
needs.

This is in from the first day because it cannot be added later.

## What you may not put in an island

These are not style notes. Each one reaches a real student.

- **No fact about BLHS without a source.** Not a meeting time, not a room
  number, not a coach's name. If nobody has told us, it is not in the game.
- **Anything you invented is marked as invented**, in the data, not in a comment.
- **No island invents an award, a cord or a criterion.** Those came from the
  school and their gaps are written down as gaps.
- **No island gets its own rival**, and no island names a real neighbouring
  school as an opponent. That is a district and permission question and nobody
  has asked it. Your school's own JV against Varsity is real and costs nothing.
- **No scored thing takes a timing input.** Reaction time confounds the whole
  study, and an island with a stopwatch in it leaves the study.
- **No streak mechanic**, and no scored item whose right answer depends on who
  is playing.

## When you finish

```
git add islands/my-island
git commit -m "the tide pool island talks and scores"
git push -u origin my-island
```

Then open a pull request. Somebody reads it before it reaches a student, and the
thing they are reading for is what your island awards.

## When you need something that is not here

Do not work around it and do not edit the engine. Add it to `NEEDS.md`, at the
bottom, in one sentence saying what you were trying to write. That file is read.
