from pathlib import Path

TEXT_EXTENSIONS = {
    ".txt", ".md", ".py", ".js", ".ts", ".java", ".cpp", ".c",
    ".sql", ".html", ".css", ".json", ".csv",
}

def extract_text(path: Path, max_chars: int = 100_000) -> str:
    suffix = path.suffix.lower()

    try:
        if suffix in TEXT_EXTENSIONS:
            return path.read_text(encoding="utf-8", errors="ignore")[:max_chars]

        if suffix == ".pdf":
            import fitz
            document = fitz.open(path)
            text = "\n".join(page.get_text() for page in document)
            document.close()
            return text[:max_chars]
    except Exception:
        return ""

    return ""
