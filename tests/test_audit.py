from file_space_audit.audit import audit


def test_audit_groups_identical_files_without_modifying_them(tmp_path) -> None:
    (tmp_path / "a.txt").write_text("same")
    (tmp_path / "b.txt").write_text("same")
    (tmp_path / "other.txt").write_text("other")
    report = audit(tmp_path)
    assert report["files"] == 3
    assert len(report["duplicate_groups"]) == 1
    assert report["duplicate_groups"][0]["copies"] == ["a.txt", "b.txt"]
    assert (tmp_path / "a.txt").read_text() == "same"


def test_missing_directory_is_rejected(tmp_path) -> None:
    try:
        audit(tmp_path / "missing")
    except ValueError as error:
        assert "not a directory" in str(error)
    else:
        raise AssertionError("expected validation error")
