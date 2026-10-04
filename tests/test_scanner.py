from pathlib import Path
from app.scanner.scanner import calculate_sha256, scan_directory

def test_hash_is_deterministic(tmp_path: Path):
    file = tmp_path / "sample.txt"
    file.write_text("hello world", encoding="utf-8")
    assert calculate_sha256(file) == calculate_sha256(file)

def test_scan_directory(tmp_path: Path):
    file = tmp_path / "notes.txt"
    file.write_text("machine learning notes", encoding="utf-8")
    count = scan_directory(tmp_path)
    assert count == 1
