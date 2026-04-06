from typing import Optional

SCALE_INSTRUCTIONS = {
    "bed": """This is a small-scale bed/container design (under 200 sq ft).
Focus on: individual plant placements, companion planting guilds, spacing between plants.
Do NOT include zone mapping or large-scale features.""",

    "yard": """This is a residential yard design.
Focus on: permaculture zone mapping (zones 1-3), garden bed placement, guild areas, paths, composting area.
Include named plant groupings per zone.""",

    "smallholding": """This is a smallholding/homestead design (1-10 acres).
Focus on: full zone mapping (zones 1-5), water systems, food forest areas, animal areas, structures.
Include both an overview and detail for key areas.""",

    "acreage": """This is a large-scale property design (10+ acres).
Focus on: zone overview map, water catchment and flow, pasture rotation, food forest placement, building sites, access roads.
Produce an overview zone map. Detail specific sub-areas only if requested.""",
}

DETAIL_INSTRUCTIONS = {
    "general": """Detail level: GENERAL — labeled zones and areas only.
Output zone names and purposes (e.g., "annual beds", "fruit tree area", "herb spiral near kitchen").
Do NOT specify individual plant species or spacing.""",

    "moderate": """Detail level: MODERATE — named plant groupings per zone.
Output guild compositions (e.g., "dwarf apple + comfrey + clover guild in zone 2").
Include general spacing guidelines but not exact coordinates.""",

    "specific": """Detail level: SPECIFIC — individual plant placements.
Output exact plant positions with spacing (e.g., "Honeycrisp apple at position (12,8), comfrey ring at 3ft radius").
Include species, variety when relevant, and companion relationships.""",
}


def assemble_prompt(
    scale: str,
    detail_level: str,
    location: Optional[str],
    hardiness_zone: Optional[str],
    goals: Optional[str],
    answers: list[dict],
) -> str:
    answers_text = ""
    if answers:
        answers_text = "\n".join(
            f"Q: {a['question']}\nA: {a['answer']}" for a in answers
        )

    return f"""You are an expert permaculture designer. Generate a structured site plan as JSON.

SITE CONTEXT:
- Location: {location or 'Not specified'}
- Hardiness zone: {hardiness_zone or 'Not specified'}
- Goals: {goals or 'Not specified'}

ADDITIONAL CONTEXT FROM USER:
{answers_text or 'None provided'}

SCALE: {scale}
{SCALE_INSTRUCTIONS.get(scale, SCALE_INSTRUCTIONS['yard'])}

{DETAIL_INSTRUCTIONS.get(detail_level, DETAIL_INSTRUCTIONS['moderate'])}

OUTPUT FORMAT — respond with JSON only:
{{
  "title": "Design title",
  "scale": "{scale}",
  "detail_level": "{detail_level}",
  "zones": [
    {{
      "id": "zone-1",
      "name": "Zone name",
      "description": "Purpose and contents",
      "bounds": {{"x": 0, "y": 0, "width": 100, "height": 100}},
      "color": "#hex color for this zone",
      "elements": [
        {{
          "type": "plant|structure|path|water|area",
          "name": "Element name",
          "x": 50,
          "y": 50,
          "radius": 10,
          "notes": "Optional details"
        }}
      ]
    }}
  ],
  "annotations": [
    {{"text": "Annotation text", "x": 0, "y": 0}}
  ],
  "summary": "Brief description of the overall design"
}}"""
