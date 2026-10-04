import hashlib
from datetime import datetime
from pathlib import Path

from sqlalchemy import select

from app.core.database import SessionLocal, init_db
from app.core.models import FileRecord
from .classifier import classify_file
from .extractor import extract_text

IGNORED_DIRECTORIES = {".git", ".venv", "__pycache__", ".pytest_cache"}

def calculate_sha256(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        while chunk := file.read(chunk_size):
            digest.update(chunk)
    return digest.hexdigest()

def iter_files(root: Path):
    for path in root.rglob("*"):
        if path.is_file() and not any(part in IGNORED_DIRECTORIES for part in path.parts):
            yield path

def scan_directory(directory: str | Path) -> int:
    root = Path(directory).expanduser().resolve()
    if not root.exists() or not root.is_dir():
        raise ValueError(f"Directory does not exist: {root}")

    init_db()
    scanned = 0

    with SessionLocal() as session:
        for path in iter_files(root):
            file_hash = calculate_sha256(path)
            existing = session.scalar(select(FileRecord).where(FileRecord.path == str(path)))
            content = extract_text(path)
            stat = path.stat()

            if existing:
                existing.name = path.name
                existing.extension = path.suffix.lower()
                existing.size_bytes = stat.st_size
                existing.category = classify_file(path, content)
                existing.sha256 = file_hash
                existing.content = content
                existing.modified_at = datetime.fromtimestamp(stat.st_mtime)
            else:
                session.add(FileRecord(
                    path=str(path),
                    name=path.name,
                    extension=path.suffix.lower(),
                    size_bytes=stat.st_size,
                    category=classify_file(path, content),
                    sha256=file_hash,
                    content=content,
                    modified_at=datetime.fromtimestamp(stat.st_mtime),
                ))
            scanned += 1

        session.commit()

    return scanned
