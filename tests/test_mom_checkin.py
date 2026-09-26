"""MOM-0 Mau Costume check-in — measurable beat tests."""

from __future__ import annotations

from datetime import date, timedelta
from pathlib import Path

from mom.cli import main
from mom.nudges import nudge_for
from mom.store import CheckIn, load_checkins, streak_held


def test_name_and_checkin_streak(tmp_path: Path) -> None:
    ledger = tmp_path / "checkins.jsonl"
    assert main(["name", "late-night-scroll", "--ledger", str(ledger)]) == 0
    today = date.today()
    yesterday = today - timedelta(days=1)
    assert (
        main(
            [
                "checkin",
                "late-night-scroll",
                "held",
                "--ledger",
                str(ledger),
                "--day",
                yesterday.isoformat(),
            ]
        )
        == 0
    )
    assert (
        main(
            [
                "checkin",
                "late-night-scroll",
                "held",
                "--ledger",
                str(ledger),
                "--day",
                today.isoformat(),
            ]
        )
        == 0
    )
    records = load_checkins(ledger, "late-night-scroll")
    assert streak_held(records, "late-night-scroll") == 2
    assert main(["streak", "late-night-scroll", "--ledger", str(ledger)]) == 0


def test_slip_resets_compassion_not_shame() -> None:
    text = nudge_for(0)
    assert "levanta" in text or "Maes" in text or "habits" in text.lower()


def test_checkin_dataclass_roundtrip(tmp_path: Path) -> None:
    from mom.store import append_checkin

    ledger = tmp_path / "c.jsonl"
    append_checkin(
        ledger,
        CheckIn(mau_costume="sugar", status="slipped", day="2026-09-26", note="one cookie"),
    )
    rows = load_checkins(ledger)
    assert len(rows) == 1
    assert rows[0].status == "slipped"
    assert streak_held(rows, "sugar") == 0
