# archive

What this repo used to need and no longer does.

Nothing in here is an instruction. These files are kept as a record of what was
asked for and what it cost to get, so that nobody has to work it out twice. If
something here contradicts the README, the README is right.

| file | what it was | why it is here |
|---|---|---|
| [NEEDS.md](NEEDS.md) | every hole in the engine that stopped an island loading, written while this repo was built | all fourteen are closed. The measurements behind them are worth keeping: what the MicroPython build really has, how a multi-file island has to be written into the runtime, and which checks only work on one side of the wire |

## Things that were taken out rather than archived

These left no file behind, so they are written down here instead.

- **The plain arm, and `Scored`.** Every island used to render twice: once as the
  game and once as flat text with no character, because the two were being
  compared. That comparison is not part of this project any more. `grape.py` no
  longer has the `Scored` base class, the skeleton no longer has a second
  branch, and `tests/test_skeleton.py` no longer checks that the two agree.
  `play(beat, as_plain=True)` still exists in `vine.py` and still works; it is an
  author's choice about one moment now, not half of a design.
- **`islands/skeleton/questions.py`.** The old template kept its questions in a
  third file so the two renderings could share them. With one rendering left, the
  questions moved into `lines.py` beside everything else the island says.
- **`tools/sync.py`'s island copier.** It used to carry whole islands from the
  engine into this repo, back when the engine was where they were written. They
  are written here now and the engine vendors them at build time, so the copier
  had nothing left to copy.
