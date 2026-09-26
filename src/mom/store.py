"""JSONL habit ledger — append-only check-ins (reuse horus jsonl append shape)."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Iterable, List, Optional


@dataclass
class CheckIn:
    """One Mau Costume daily check-in transmission."""

    mau_costume: str
    status: str  # held | slipped | named
    day: str  # ISO date
    note: str = ""
    recorded_at: str = ""

    def __post_init__(self) -> None:
        if not self.recorded_at:
            self.recorded_at = datetime.now(timezone.utc).isoformat()


def default_ledger_path() -> Path:
    return Path.home() / ".mom" / "checkins.jsonl"


def append_checkin(path: Path, record: CheckIn) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(asdict(record), ensure_ascii=False) + "\n")


def load_checkins(path: Path, mau_costume: Optional[str] = None) -> List[CheckIn]:
    if not path.exists():
        return []
    out: List[CheckIn] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        data = json.loads(line)
        rec = CheckIn(**data)
        if mau_costume is None or rec.mau_costume == mau_costume:
            out.append(rec)
    return out


def streak_held(records: Iterable[CheckIn], mau_costume: str) -> int:
    """Count consecutive calendar days ending today where status == held."""
    days = {
        r.day
        for r in records
        if r.mau_costume == mau_costume and r.status == "held"
    }
    if not days:
        return 0
    cursor = date.today()
    streak = 0
    while cursor.isoformat() in days:
        streak += 1
        cursor = date.fromordinal(cursor.toordinal() - 1)
    return streak
