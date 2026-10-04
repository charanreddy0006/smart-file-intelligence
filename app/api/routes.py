from fastapi import APIRouter, Query
from sqlalchemy import func, select

from app.core.database import SessionLocal, init_db
from app.core.models import FileRecord
from app.search.engine import search_files

router = APIRouter(prefix="/api")

@router.get("/health")
def health():
    return {"status": "ok", "service": "smart-file-intelligence"}

@router.get("/stats")
def stats():
    init_db()
    with SessionLocal() as session:
        total = session.scalar(select(func.count(FileRecord.id))) or 0
        categories = session.execute(
            select(FileRecord.category, func.count(FileRecord.id))
            .group_by(FileRecord.category)
            .order_by(func.count(FileRecord.id).desc())
        ).all()

    return {
        "total_files": total,
        "categories": [{"category": category, "count": count} for category, count in categories],
    }

@router.get("/files")
def files(limit: int = Query(default=100, ge=1, le=500)):
    init_db()
    with SessionLocal() as session:
        records = session.scalars(
            select(FileRecord).order_by(FileRecord.modified_at.desc()).limit(limit)
        ).all()

    return [{
        "id": r.id,
        "name": r.name,
        "path": r.path,
        "extension": r.extension,
        "size_bytes": r.size_bytes,
        "category": r.category,
    } for r in records]

@router.get("/search")
def search(q: str = Query(min_length=1), limit: int = Query(default=10, ge=1, le=50)):
    return {"query": q, "results": search_files(q, limit)}
