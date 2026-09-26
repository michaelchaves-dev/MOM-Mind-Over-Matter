"""Compassion nudges — Portuguese-proverb inspired, no guilt.

Reuse-before-invent: language drawn from README philosophy
(Progress, Not Perfection / Accountability with Compassion).
"""

from __future__ import annotations

NUDGES = (
    "Água mole em pedra dura — soft water on hard stone; small returns carve the habit.",
    "Devagar se vai ao longe — slowly one goes far; a short check-in still counts.",
    "Quem cai e levanta, mais forte fica — who falls and rises grows stronger.",
    "Approved by Maes: name the Mau Costume, then take one kinder step.",
    "You are not your habits. Your habits are what you do — not who you are.",
)


def nudge_for(streak: int) -> str:
    """Pick a compassion nudge keyed by streak (stable, no RNG invent)."""
    if streak <= 0:
        return NUDGES[2]  # fall-and-rise after a miss
    return NUDGES[streak % len(NUDGES)]
