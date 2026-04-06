import json
from datetime import datetime

from src.firestore import get_project, update_project
from src.gemini import generate_design
from src.prompt import assemble_prompt
from src.renderer import render_svg, svg_to_png
from src.scale import classify_scale
from src.detail_level import infer_detail_level
from src.storage import upload_design


def run_generation(project_id: str) -> None:
    project = get_project(project_id)
    if project is None:
        return

    update_project(project_id, {"design.status": "generating"})

    try:
        context = project.get("context", {})
        goals = project.get("goals")
        location = project.get("location")
        answers = context.get("answers", [])

        # Classify scale
        site_description = location or ""
        scale = project.get("scale") or classify_scale(site_description, goals)

        # Infer detail level
        detail_level = project.get("detail_level") or infer_detail_level(goals, scale)

        # Infer hardiness zone (placeholder — would use a geocoding API in production)
        hardiness_zone = project.get("hardiness_zone")

        # Assemble and send prompt
        prompt = assemble_prompt(
            scale=scale,
            detail_level=detail_level,
            location=location,
            hardiness_zone=hardiness_zone,
            goals=goals,
            answers=answers,
        )
        plan = generate_design(prompt)

        # Render outputs
        svg_string = render_svg(plan)
        png_bytes = svg_to_png(svg_string)
        metadata_json = json.dumps(plan, indent=2).encode("utf-8")

        # Upload to GCS
        svg_path = upload_design(project_id, "plan.svg", svg_string.encode("utf-8"), "image/svg+xml")
        png_path = upload_design(project_id, "plan.png", png_bytes, "image/png")
        meta_path = upload_design(project_id, "metadata.json", metadata_json, "application/json")

        # Update project
        update_project(project_id, {
            "scale": scale,
            "detail_level": detail_level,
            "design.status": "complete",
            "design.gcs_path": svg_path,
            "design.png_path": png_path,
            "design.metadata_path": meta_path,
            "design.generated_at": datetime.utcnow().isoformat(),
        })

    except Exception as e:
        update_project(project_id, {
            "design.status": "failed",
        })
        raise
