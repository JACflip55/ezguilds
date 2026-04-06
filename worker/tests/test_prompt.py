from src.prompt import assemble_prompt


def test_prompt_includes_scale():
    prompt = assemble_prompt(
        scale="bed",
        detail_level="specific",
        location="Portland, OR",
        hardiness_zone="8b",
        goals="Herb garden",
        answers=[{"question": "Sun?", "answer": "Full sun"}],
    )
    assert "bed" in prompt
    assert "specific" in prompt
    assert "Portland" in prompt
    assert "8b" in prompt
    assert "Herb garden" in prompt
    assert "Full sun" in prompt


def test_prompt_acreage_general():
    prompt = assemble_prompt(
        scale="acreage",
        detail_level="general",
        location="Vermont",
        hardiness_zone="4a",
        goals="Regenerative farm",
        answers=[],
    )
    assert "acreage" in prompt
    assert "general" in prompt
    assert "zone overview" in prompt.lower() or "zones" in prompt.lower()


def test_prompt_handles_none():
    prompt = assemble_prompt(
        scale="yard",
        detail_level="moderate",
        location=None,
        hardiness_zone=None,
        goals=None,
        answers=[],
    )
    assert "yard" in prompt
    assert "moderate" in prompt
