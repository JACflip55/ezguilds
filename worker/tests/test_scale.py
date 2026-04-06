from src.scale import classify_scale


def test_classify_bed():
    assert classify_scale("10 sq ft raised bed", "grow herbs") == "bed"
    assert classify_scale("4x8 raised garden bed", "salad greens") == "bed"
    assert classify_scale("small container garden, 50 sq ft", "herbs and tomatoes") == "bed"


def test_classify_yard():
    assert classify_scale("quarter acre suburban lot", "food garden") == "yard"
    assert classify_scale("backyard, about 2000 sq ft", "family garden") == "yard"


def test_classify_smallholding():
    assert classify_scale("3 acre hobby farm", "food forest and chickens") == "smallholding"
    assert classify_scale("5 acres rural", "homestead") == "smallholding"


def test_classify_acreage():
    assert classify_scale("100 acre rural property", "regenerative farm") == "acreage"
    assert classify_scale("40 acres with buildings", "permaculture farm") == "acreage"


def test_classify_default():
    assert classify_scale(None, None) == "yard"
