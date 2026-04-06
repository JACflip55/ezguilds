import re
from typing import Literal, Optional

Scale = Literal["bed", "yard", "smallholding", "acreage"]


def classify_scale(
    site_description: Optional[str],
    goals: Optional[str],
) -> Scale:
    text = f"{site_description or ''} {goals or ''}".lower()

    # Check for explicit acreage mentions
    acre_match = re.search(r"(\d+)\s*acres?", text)
    if acre_match:
        acres = int(acre_match.group(1))
        if acres >= 10:
            return "acreage"
        if acres >= 1:
            return "smallholding"

    # Check for sq ft mentions
    sqft_match = re.search(r"(\d+)\s*(?:sq\.?\s*f(?:ee)?t|square\s*f(?:ee)?t)", text)
    if sqft_match:
        sqft = int(sqft_match.group(1))
        if sqft <= 200:
            return "bed"
        if sqft <= 5000:
            return "yard"
        return "smallholding"

    # Keyword-based classification
    bed_keywords = ["raised bed", "container", "planter", "pot", "4x8", "4x4", "window box"]
    if any(kw in text for kw in bed_keywords):
        return "bed"

    acreage_keywords = ["farm", "ranch", "pasture", "regenerative"]
    if any(kw in text for kw in acreage_keywords):
        return "acreage"

    homestead_keywords = ["homestead", "hobby farm", "smallholding", "food forest"]
    if any(kw in text for kw in homestead_keywords):
        return "smallholding"

    return "yard"
