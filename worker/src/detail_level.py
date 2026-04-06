from typing import Literal, Optional

DetailLevel = Literal["general", "moderate", "specific"]

SPECIFIC_KEYWORDS = [
    "exact", "specific", "detailed planting", "plant by plant",
    "spacing", "exactly what", "precisely",
]

GENERAL_KEYWORDS = [
    "big picture", "overview", "lay out zones", "general plan",
    "broad strokes", "zone layout",
]

SCALE_DEFAULTS: dict[str, DetailLevel] = {
    "bed": "specific",
    "yard": "moderate",
    "smallholding": "moderate",
    "acreage": "general",
}


def infer_detail_level(
    goals: Optional[str],
    scale: str,
) -> DetailLevel:
    if goals:
        text = goals.lower()
        if any(kw in text for kw in SPECIFIC_KEYWORDS):
            return "specific"
        if any(kw in text for kw in GENERAL_KEYWORDS):
            return "general"

    return SCALE_DEFAULTS.get(scale, "moderate")
