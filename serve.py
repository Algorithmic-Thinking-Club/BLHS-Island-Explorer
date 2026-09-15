"""serve your working tree to the game so you can see a change without pushing.

run `python serve.py`, then paste the url it prints into the game as
`?scene=grape&from=<url>`. it hands out .py and .json only, to your machine only.
"""
import os
import subprocess
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

REPO = os.path.dirname(os.path.abspath(__file__))
# the first port to try; it walks up from here when one is busy
PORT = 5280
TRIES = 20
SERVABLE = (".py", ".json")


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=REPO, **kw)

    def end_headers(self):
        # lets the game, which runs on another port, read the answer
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
        # a request for a folder is answered with its island.json
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
