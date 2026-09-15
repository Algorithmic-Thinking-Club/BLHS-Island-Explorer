# BLHS Island Explorer

Every island in the BLHS adventure game, written in Python, one folder each. You
own a folder, nobody else edits it, and you never open the engine. What you write
is real Python running inside the real game, next to everybody else's.

## The two rules

**A word only happens if you yield it.**

```python
yield say("You made it.")     # appears in the box and waits for the click
say("You made it.")           # builds a dict, drops it, nobody sees it
```

**Nothing calls your functions. The game does.**

```python
@on_talk("greeter")
def meet_the_greeter():
    yield say("You're new here.", who="greeter")
```

Nothing anywhere calls `meet_the_greeter`. The player walks up to the anchor
named `greeter`, presses E, and the game calls it. `@on_start` runs once when the
island loads. [docs/VOCABULARY.md](docs/VOCABULARY.md) is every word you can say.

## 1. Clone

```
git clone https://github.com/Algorithmic-Thinking-Club/BLHS-Island-Explorer.git
cd BLHS-Island-Explorer
python -m unittest
```

You need Python 3.8 or later. Nothing else installs.

## 2. Run the game next door

The game is a separate repo, and it has to sit beside this one.

```
cd ..
git clone https://github.com/Algorithmic-Thinking-Club/BLHS-ADVINE.git
cd BLHS-ADVINE
npm install
npm run dev
```

That prints a URL, usually `http://localhost:5173`. `npm run dev` copies the
islands out of this repo on its way up, so the game is running your files.

## 3. Copy the skeleton

```
git checkout -b my-island
cp -r islands/skeleton islands/my-island
```

`cp -r` works in Git Bash and PowerShell. In `cmd.exe` use File Explorer. Then
open the copy and change:

- `island.json`: `programme` and `map`, your own ids in lower case with hyphens,
  different from each other and from everybody else's. Then `title`, `owner`,
  and every fact in `content`.
- `lines.py`: the anchor name at the top, and every string under it.
- `island.py`: the flag name in `finished()`, and the rows in `TASKS`.

Your programme id is not one of them: the island reads it out of your own
`island.json` with `manifest()["programme"]`, so it is written once.

Every field `island.json` takes is listed in `tools/manifest.py`, which is also
what refuses a bad one. Two rules it will not bend on: an island is one flat
folder with every `.py` file named in `modules`, and `programme` and `map` are
different key spaces, so they may never be the same string.

## 4. Name your anchors in MAPVIS

Your code addresses places by name, never by an x and a y. Those names come from
MAPVIS, where somebody draws the map and drops an anchor on each thing a player
can press.

An anchor has a **name** and a **label**. The name is what `@on_talk("greeter")`
matches; the label is what the player reads. Renaming the label cannot break your
code, which is why they are two fields.

Ask Ash for a map, and give him the list of names you need. If pressing E does
nothing, your name and the map's do not match, and the console lists the names
the map really has.

## 5. Test

```
python -m unittest
python tools/manifest.py islands/my-island
```

Run both **from the repo root**: `python -m unittest` from inside your own folder
prints `OK` having run nothing.

Copy `tests/test_skeleton.py` to `tests/test_my_island.py` and point it at your
folder. **Underscores, and the name has to start with `test`**, or `unittest`
skips the file silently. `tests/pump.py` is what runs an island with no game.

A green test proves your logic and nothing else. Nothing in the harness performs
anything, so a green test and a broken island are perfectly compatible. Play it.

## 6. Open a pull request

```
git add islands/my-island tests/test_my_island.py islands.json
git commit -m "the tide pool island talks and scores"
git push -u origin my-island
```

Add your row to `islands.json` at the root before you push, or the game cannot
see your island. `programme` and `map` have to match your `island.json`.

```json
{ "programme": "tide-pool", "map": "tide-pool-shore", "folder": "my-island",
  "name": "Tide Pool Club", "place": "atc-room", "kind": "club",
  "tags": [], "playable": true, "host": "Ms. Berwick",
  "blurb": "Thursdays, and everybody gets wet.",
  "source": "blhs.sumnersd.org/activities/clubs-activities, read 2026-09-04" }
```

Then open the PR. Ash reads every island before it reaches a student.

## What you may not put in an island

Each of these reaches a real student.

- **No fact about BLHS without a source.** Not a meeting time, not a room
  number, not a coach's name. If nobody has told us, it is not in the game.
- **Anything you invented is marked as invented**, in `content`, not in a comment.
- **No island invents an award, a cord or a criterion.**
- **No island names a real neighbouring school as an opponent.** Your own JV
  against Varsity is fine.
- **No scored item whose right answer depends on who is playing.**

## Where to look next

- `islands/atc/` is the worked example, and the one to read after the skeleton.
- `islands/panther-maw/` is the complicated one: seven handlers on one map and a
  scene long enough to live in its own file. Read it, do not copy it.
- `docs/VOCABULARY.md` is every word, generated from the engine.
- `archive/` is what this repo used to need and no longer does.

When you need a word that is not there, do not work around it and do not edit the
engine. Open an issue saying what you were trying to write.
