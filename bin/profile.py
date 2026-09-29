#!/usr/bin/env python3
"""
buyer-eval: saved buyer context, stored locally so the next evaluation skips setup.

Stored at ~/.salespeak/buyer-eval-profile.json (override with BUYER_EVAL_PROFILE).
Never sent anywhere. Only the whitelisted fields below are kept; anything else
passed to `save` is dropped.

Subcommands:
  show [--machine]   Print the profile (one-line JSON with --machine), or "none"
  save --json STR    Merge fields into the profile (lists are replaced, not appended)
  clear              Delete the profile file
  path               Print the profile path
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

PROFILE_PATH = Path(
    os.environ.get("BUYER_EVAL_PROFILE", str(Path.home() / ".salespeak" / "buyer-eval-profile.json"))
).expanduser()

# Reusable buying context only. No personal names, emails, vendor quotes, or documents.
STRING_FIELDS = {"company_name", "company_size", "industry", "region", "last_category"}
LIST_FIELDS = {"systems", "requirements", "hard_constraints", "preferred_criteria"}
MAX_STR = 200
MAX_ITEMS = 20


def _clean(data: dict) -> dict:
    out = {}
    for k, v in data.items():
        if k in STRING_FIELDS and isinstance(v, (str, int, float)):
            s = str(v).strip()[:MAX_STR]
            if s:
                out[k] = s
        elif k in LIST_FIELDS and isinstance(v, list):
            items = [str(x).strip()[:MAX_STR] for x in v if str(x).strip()][:MAX_ITEMS]
            out[k] = items
    return out


def load() -> dict | None:
    try:
        data = json.loads(PROFILE_PATH.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else None
    except (OSError, ValueError):
        return None


def cmd_show(args) -> int:
    data = load()
    if not data:
        print("none")
        return 0
    if args.machine:
        print(json.dumps(data, separators=(",", ":"), ensure_ascii=False))
    else:
        print(json.dumps(data, indent=2, ensure_ascii=False))
        print(f"\nStored at {PROFILE_PATH}")
    return 0


def cmd_save(args) -> int:
    try:
        incoming = json.loads(args.json)
    except ValueError as e:
        print(f"ERROR: invalid JSON: {e}", file=sys.stderr)
        return 1
    if not isinstance(incoming, dict):
        print("ERROR: expected a JSON object", file=sys.stderr)
        return 1
    current = load() or {}
    current.update(_clean(incoming))
    current["updated_at"] = datetime.now().date().isoformat()
    current["schema_version"] = 1
    try:
        PROFILE_PATH.parent.mkdir(parents=True, exist_ok=True)
        tmp = PROFILE_PATH.with_suffix(".tmp")
        tmp.write_text(json.dumps(current, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        tmp.replace(PROFILE_PATH)
    except OSError as e:
        print(f"ERROR: could not save profile: {e}", file=sys.stderr)
        return 1
    print(f"SAVED {PROFILE_PATH}")
    return 0


def cmd_clear(args) -> int:
    try:
        PROFILE_PATH.unlink()
        print("CLEARED")
    except FileNotFoundError:
        print("NONE")
    return 0


def cmd_path(args) -> int:
    print(PROFILE_PATH)
    return 0


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="profile.py", description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("show")
    s.add_argument("--machine", action="store_true")
    s.set_defaults(fn=cmd_show)
    s = sub.add_parser("save")
    s.add_argument("--json", required=True)
    s.set_defaults(fn=cmd_save)
    sub.add_parser("clear").set_defaults(fn=cmd_clear)
    sub.add_parser("path").set_defaults(fn=cmd_path)
    args = p.parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
