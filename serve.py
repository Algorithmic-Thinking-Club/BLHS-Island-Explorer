"""Hand your branch to the game.

The game loads an island by fetching it over HTTP. Once this repo is on GitHub
that fetch goes straight at a branch:

    https://raw.githubusercontent.com/<owner>/blhs-islands/<branch>/islands/<yours>/

While you are working, you do not want to push to see a change. So run this, and
the same fetch points at the files on your own disk instead:

    python serve.py

It prints the URL to paste into the game. Edit a file, reload the page, and your
island is different. Nothing is committed, nothing is pushed, and only your
machine can reach it.

WHAT IT SERVES IS YOUR WORKING TREE, not the last commit. That is what you want
while you build and it is worth knowing when you show somebody: they see what
you PUSHED, and you see what you SAVED.

Two things this does that `python -m http.server` does not, and both are the
reason this file exists rather than a line in the README. It sends the header
that lets a page on another port read the response at all, without which the
game's fetch fails with a message about CORS that explains nothing. And it hands
back only .py and .json, because a server that will hand a stranger any file
under it is not a thing to leave running on a school network.
"""
import os
import subprocess
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

REPO = os.path.dirname(os.path.abspath(__file__))
# The game dev server is 5173 and MAPVIS is 5274, and Vite takes the next free
# port when one of those is busy, so the 5270s fill up on their own. Starting
# clear of them and walking up from there costs nothing and saves a member an
# afternoon: a port already in use does not fail loudly, it hands the game
# somebody else's index.html and the island loads as a page of HTML.
PORT = 5280
TRIES = 20
SERVABLE = (".py", ".json")


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=REPO, **kw)

    def end_headers(self):
        # WITHOUT THIS THE GAME CANNOT READ THE ANSWER. The page is on one port
        # and this is on another, so the browser treats it as another origin and
        # throws the response away unless the response says that is allowed.
        self.send_header("Access-Control-Allow-Origin", "*")
        # your island is the file you just saved, never the one the browser kept
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.end_headers()

    def send_head(self):
        path = self.path.split("?")[0].split("#")[0]
        # THE URL THIS PROGRAM PRINTS IS THE FOLDER, because that is what the
        # loader is handed and it appends the filename itself. A member pastes
        # that line into a browser to check the server is alive, which is the
        # first thing anybody does, so the folder answers with the manifest
        # rather than with a refusal that names their own file types back at them.
        if path.startswith("/islands/") and path.endswith("/"):
            self.path = path + "island.json"
            path = self.path
        if not path.endswith(SERVABLE):
            self.send_error(404, "this server only hands out %s, and it does not list "
                                 "directories" % " and ".join(SERVABLE))
            return None
        return super().send_head()

    def log_message(self, fmt, *args):
        # one readable line per fetch, so you can see the game asking
        sys.stdout.write("  %s\n" % (fmt % args))


def branch():
    try:
        out = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"],
                             cwd=REPO, capture_output=True, text=True, timeout=5)
        return out.stdout.strip() or "(no branch)"
    except Exception:
        return "(git not found)"


def islands():
    root = os.path.join(REPO, "islands")
    if not os.path.isdir(root):
        return []
    return sorted(n for n in os.listdir(root)
                  if os.path.isfile(os.path.join(root, n, "island.json")))


def start(first, tries):
    """The first free port at or above `first`, already listening."""
    last = None
    for port in range(first, first + tries):
        try:
            return ThreadingHTTPServer(("127.0.0.1", port), Handler), port
        except OSError as e:
            last = e
    raise last


def main():
    asked = int(sys.argv[1]) if len(sys.argv) > 1 else PORT
    try:
        server, port = start(asked, 1 if len(sys.argv) > 1 else TRIES)
    except OSError as e:
        print("could not start on port %d: %s" % (asked, e))
        print("something else is using it. Try: python serve.py %d" % (asked + 1))
        return 1

    base = "http://localhost:%d" % port
    print("serving the working tree on branch %s" % branch())
    print("  %s" % REPO)
    print()
    for name in islands() or ["(no islands yet)"]:
        print("  %s/islands/%s/" % (base, name))
    print()
    print("paste one of those into the game as ?scene=grape&from=<url>")
    print("ctrl-c to stop")
    print()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nstopped")
    return 0


if __name__ == "__main__":
    sys.exit(main())
