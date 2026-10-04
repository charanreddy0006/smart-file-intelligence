from pathlib import Path

CATEGORY_EXTENSIONS = {
    "Data": {".csv", ".json", ".parquet", ".xlsx", ".xls"},
    "Development": {".py", ".js", ".ts", ".java", ".cpp", ".c", ".sql", ".html", ".css"},
    "Images": {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"},
    "Archives": {".zip", ".tar", ".gz", ".rar", ".7z"},
    "Documents": {".pdf", ".docx", ".doc", ".txt", ".md"},
}

KEYWORD_CATEGORIES = {
    "Finance": ("invoice", "bank", "finance", "payment", "salary", "tax"),
    "Career": ("resume", "cv", "interview", "career", "job", "internship"),
    "Education": ("lecture", "assignment", "exam", "notes", "course", "university"),
}


def classify_file(path: Path, content: str = "") -> str:
    haystack = f"{path.name} {content}".lower()

    # Check meaningful keywords first
    for category, keywords in KEYWORD_CATEGORIES.items():
        if any(keyword in haystack for keyword in keywords):
            return category

    # Fall back to extension-based classification
    extension = path.suffix.lower()
    for category, extensions in CATEGORY_EXTENSIONS.items():
        if extension in extensions:
            return category

    return "Other"