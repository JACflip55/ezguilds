from src.models import Project, FileRef, Answer, DesignState


def test_project_defaults():
    p = Project(id="abc-123", owner_uid="user-1")
    assert p.status == "uploading"
    assert p.scale is None
    assert p.detail_level is None
    assert p.context.files == []
    assert p.context.answers == []
    assert p.design.status == "pending"
    assert p.chat_history == []


def test_file_ref():
    f = FileRef(name="site.pdf", gcs_path="uploads/abc/site.pdf", type="site_map")
    assert f.name == "site.pdf"
    assert f.type == "site_map"


def test_answer():
    a = Answer(question="Sun exposure?", answer="Full sun", order=1)
    assert a.order == 1


def test_project_to_dict_roundtrip():
    p = Project(id="abc-123", owner_uid="user-1", location="Portland, OR")
    d = p.model_dump()
    p2 = Project(**d)
    assert p2.id == p.id
    assert p2.location == p.location
