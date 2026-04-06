from src.detail_level import infer_detail_level


def test_specific_from_goals():
    assert infer_detail_level("I want a detailed planting plan with exact spacing", "bed") == "specific"
    assert infer_detail_level("tell me exactly what to plant where", "bed") == "specific"


def test_general_from_goals():
    assert infer_detail_level("help me lay out zones for my property", "acreage") == "general"
    assert infer_detail_level("big picture overview of the land", "smallholding") == "general"


def test_defaults_by_scale():
    assert infer_detail_level("grow some food", "bed") == "specific"
    assert infer_detail_level("grow some food", "yard") == "moderate"
    assert infer_detail_level("grow some food", "smallholding") == "moderate"
    assert infer_detail_level("grow some food", "acreage") == "general"


def test_none_goals():
    assert infer_detail_level(None, "yard") == "moderate"
