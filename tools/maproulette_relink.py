"""Repoint old skfd.github.io links in the text fields of a MapRoulette project's challenges.

    python maproulette_relink.py <project_id> [--apply] [--only <challenge_id>]

Dry run by default. Needs MAPROULETTE_API_KEY (a User variable on Windows is read from the
registry, so no restart is needed). Only the text fields that actually change are sent.
"""
import json
import os
import re
import sys
import urllib.request

API = "https://maproulette.org/api/v2"
FIELDS = ("instruction", "description", "blurb")
OLD = re.compile(
    r"skfd(\.github\.io)?/(toronto-2-address-import|toronto-addresses-import|"
    r"toronto-addresses-layer|toronto-open-poi|toronto-parks-layer|"
    r"toronto-poster-columns-layer|toronto-streets-layer|toronto-streets-osm|"
    r"toronto-waterways-layer)(?![a-z0-9-])"
)


def key():
    k = os.environ.get("MAPROULETTE_API_KEY")
    if not k and os.name == "nt":
        import winreg
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as h:
                k = winreg.QueryValueEx(h, "MAPROULETTE_API_KEY")[0]
        except OSError:
            k = None
    if not k:
        sys.exit("MAPROULETTE_API_KEY is not set")
    return k


def call(method, path, body=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(API + path, data=data, method=method)
    req.add_header("apiKey", key())
    req.add_header("Content-Type", "application/json")
    req.add_header("User-Agent", "maproulette-relink/1.0")
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read() or b"null")


def main():
    args = sys.argv[1:]
    project = args[0]
    apply = "--apply" in args
    only = int(args[args.index("--only") + 1]) if "--only" in args else None
    challenges = call("GET", f"/project/{project}/challenges?limit=1000")
    changed = 0
    for c in challenges:
        if only and c["id"] != only:
            continue
        update = {}
        for f in FIELDS:
            old = c.get(f) or ""
            new = OLD.sub(lambda m: "toronto-maps" + (m.group(1) or "") + "/" + m.group(2), old)
            if new != old:
                update[f] = new
        if not update:
            continue
        changed += 1
        if apply:
            call("PUT", f"/challenge/{c['id']}", update)
        print(("updated " if apply else "would update ") + f"{c['id']} {c['name']}: {', '.join(update)}")
    print(f"{changed} of {len(challenges)} challenges " + ("updated" if apply else "need updating"))


if __name__ == "__main__":
    main()
