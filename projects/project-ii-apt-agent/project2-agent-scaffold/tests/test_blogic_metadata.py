from pathlib import Path

from src.blogic_metadata import collect_blogic_metadata


def test_missing_blogic_metadata_is_bounded(tmp_path):
    metadata = collect_blogic_metadata(tmp_path / "missing-blogic")

    assert metadata.exists is False
    assert metadata.file_kind == "missing"
    assert metadata.phase_hint == "unknown"


def test_non_elf_metadata_is_safe(tmp_path):
    target = tmp_path / "blogic.copy"
    target.write_text("MOCK_BLOGIC\n", encoding="utf-8")

    metadata = collect_blogic_metadata(target)

    assert metadata.exists is True
    assert metadata.file_kind == "non-elf"
    assert metadata.size_bytes > 0
    assert len(metadata.sha256_prefix) == 16
