import json

from src.renderer import render_svg, svg_to_png


SAMPLE_PLAN = {
    "title": "Test Garden",
    "scale": "bed",
    "detail_level": "specific",
    "zones": [
        {
            "id": "zone-1",
            "name": "Herb Bed",
            "description": "Kitchen herbs",
            "bounds": {"x": 10, "y": 10, "width": 80, "height": 60},
            "color": "#4a6a30",
            "elements": [
                {"type": "plant", "name": "Basil", "x": 30, "y": 30, "radius": 5, "notes": ""},
                {"type": "plant", "name": "Thyme", "x": 50, "y": 40, "radius": 4, "notes": ""},
            ],
        }
    ],
    "annotations": [
        {"text": "North ↑", "x": 50, "y": 5},
    ],
    "summary": "A simple herb bed",
}


def test_render_svg_returns_string():
    svg = render_svg(SAMPLE_PLAN)
    assert isinstance(svg, str)
    assert "<svg" in svg
    assert "Herb Bed" in svg
    assert "Basil" in svg
    assert "Thyme" in svg


def test_render_svg_includes_title():
    svg = render_svg(SAMPLE_PLAN)
    assert "Test Garden" in svg


def test_render_svg_includes_annotations():
    svg = render_svg(SAMPLE_PLAN)
    assert "North" in svg


def test_svg_to_png_returns_bytes():
    svg = render_svg(SAMPLE_PLAN)
    png_bytes = svg_to_png(svg)
    assert isinstance(png_bytes, bytes)
    assert png_bytes[:4] == b"\x89PNG"
