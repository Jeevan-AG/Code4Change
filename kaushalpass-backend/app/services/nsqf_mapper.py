"""Fuzzy NSQF mapping for unknown skills."""

from __future__ import annotations

from typing import Any

from Levenshtein import ratio as levenshtein_ratio

NSQF_DICT: dict[str, int] = {
    "domestic worker": 2,
    "housekeeping": 2,
    "cooking": 2,
    "home cooking": 2,
    "tailoring": 4,
    "embroidery": 4,
    "hand embroidery": 4,
    "mehendi": 4,
    "mehendi artist": 4,
    "tile laying": 3,
    "masonry": 3,
    "construction labor": 3,
    "beautician": 4,
    "salon work": 4,
    "agricultural worker": 2,
    "weaving": 5,
    "loom weaving": 5,
    "plumbing": 4,
    "electrical wiring": 5,
    "carpentry": 4,
    "childcare": 2,
    "elder care": 3,
}


def map_skill_to_nsqf(skill_name: str, threshold: float = 0.55) -> dict[str, Any] | None:
    """Fuzzy match skill_name to NSQF_DICT. Returns None if no match above threshold."""
    normalized = skill_name.strip().lower()
    if not normalized:
        return None

    best_key = ""
    best_score = 0.0
    for key in NSQF_DICT:
        score = levenshtein_ratio(normalized, key)
        if score > best_score:
            best_score = score
            best_key = key

    if best_score < threshold:
        return None

    nsqf = NSQF_DICT[best_key]
    if nsqf <= 2:
        level = "beginner"
    elif nsqf <= 4:
        level = "intermediate"
    else:
        level = "expert"

    return {
        "skill_name": skill_name,
        "nsqf_level": nsqf,
        "level": level,
        "confidence": round(best_score, 2),
        "matched_occupation": best_key,
    }
