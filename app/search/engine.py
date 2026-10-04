from sqlalchemy import select
from app.core.database import SessionLocal, init_db
from app.core.models import FileRecord

def search_files(query: str, limit: int = 10) -> list[dict]:
    query = query.strip()
    if not query:
        return []

    init_db()
    with SessionLocal() as session:
        records = session.scalars(select(FileRecord)).all()

    if not records:
        return []

    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity

    corpus = [f"{r.name} {r.category} {r.content}" for r in records]
    vectorizer = TfidfVectorizer(lowercase=True, stop_words="english")

    try:
        matrix = vectorizer.fit_transform(corpus)
        query_vector = vectorizer.transform([query])
    except ValueError:
        return []

    scores = cosine_similarity(query_vector, matrix).flatten()
    results = []

    for index in scores.argsort()[::-1]:
        score = float(scores[index])
        if score <= 0:
            continue
        record = records[index]
        results.append({
            "id": record.id,
            "name": record.name,
            "path": record.path,
            "category": record.category,
            "score": round(score, 4),
            "size_bytes": record.size_bytes,
        })
        if len(results) >= limit:
            break

    return results
