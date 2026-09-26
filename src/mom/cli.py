"""Mau Costume check-in CLI — tiny argparse surface (reuse horus label_cli shape)."""

from __future__ import annotations

import argparse
import sys
from datetime import date
from pathlib import Path

from mom.nudges import nudge_for
from mom.store import CheckIn, append_checkin, default_ledger_path, load_checkins, streak_held

STATUSES = ("held", "slipped", "named")


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="mom",
        description="MOM Mind Over Matter — name a Mau Costume and check in with compassion.",
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    name = sub.add_parser("name", help="Name (flag) a Mau Costume bad habit")
    name.add_argument("mau_costume", help="short name for the bad habit")
    name.add_argument("--note", default="", help="optional context")
    name.add_argument("--ledger", type=Path, default=None)

    check = sub.add_parser("checkin", help="Daily check-in: held or slipped")
    check.add_argument("mau_costume", help="which Mau Costume")
    check.add_argument(
        "status",
        choices=("held", "slipped"),
        help="held = stayed free today; slipped = Progress, Not Perfection",
    )
    check.add_argument("--note", default="")
    check.add_argument("--ledger", type=Path, default=None)
    check.add_argument("--day", default=None, help="ISO date override (tests)")

    streak = sub.add_parser("streak", help="Show held streak + compassion nudge")
    streak.add_argument("mau_costume")
    streak.add_argument("--ledger", type=Path, default=None)

    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    ledger: Path = args.ledger or default_ledger_path()

    if args.cmd == "name":
        rec = CheckIn(
            mau_costume=args.mau_costume,
            status="named",
            day=date.today().isoformat(),
            note=args.note,
        )
        append_checkin(ledger, rec)
        print(f"Mau Costume named: {args.mau_costume}")
        print(nudge_for(0))
        return 0

    if args.cmd == "checkin":
        day = args.day or date.today().isoformat()
        rec = CheckIn(
            mau_costume=args.mau_costume,
            status=args.status,
            day=day,
            note=args.note,
        )
        append_checkin(ledger, rec)
        records = load_checkins(ledger, args.mau_costume)
        s = streak_held(records, args.mau_costume)
        print(f"check-in [{args.status}] {args.mau_costume} @ {day}  streak={s}")
        print(nudge_for(s if args.status == "held" else 0))
        return 0

    if args.cmd == "streak":
        records = load_checkins(ledger, args.mau_costume)
        s = streak_held(records, args.mau_costume)
        print(f"{args.mau_costume}: held streak = {s}")
        print(nudge_for(s))
        return 0

    return 2


if __name__ == "__main__":
    sys.exit(main())
