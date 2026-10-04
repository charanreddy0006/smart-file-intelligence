# Smart File Intelligence

Smart File Intelligence is a Python-based file management system that automatically classifies files, detects duplicate files, extracts searchable content, and provides TF-IDF based semantic-style search.

The project combines a file scanning engine, SQLite database, FastAPI REST API, and Streamlit dashboard into a single application.

## Features

- Recursive file and directory scanning
- Automatic file classification based on content and extension
- SHA-256 based duplicate detection
- Text extraction from supported text and PDF files
- TF-IDF based content search
- SQLite database for file metadata and extracted content
- FastAPI REST API
- Interactive Streamlit dashboard
- File category statistics
- Recent file tracking
- Automated test suite with pytest

## Architecture

```text
Files / Directories
        |
        v
   File Scanner
        |
        +------------------+
        |                  |
        v                  v
 Classification       SHA-256 Hash
        |                  |
        +--------+---------+
                 |
                 v
             SQLite
                 |
        +--------+--------+
        |                 |
        v                 v
    TF-IDF Search      FastAPI
        |                 |
        +--------+--------+
                 |
                 v
        Streamlit Dashboard
```

## Technology Stack

| Technology | Purpose |
|------------|---------|
| Python | Core application development |
| FastAPI | REST API |
| Streamlit | Web dashboard |
| SQLAlchemy | Database ORM |
| SQLite | Local data storage |
| PyMuPDF | PDF text extraction |
| Scikit-learn | TF-IDF search |
| Pandas | Data processing and dashboard tables |
| Pytest | Testing |

## Project Structure

```text
smart-file-intelligence/
|
+-- app/
|   +-- api/
|   |   +-- routes.py
|   |
|   +-- core/
|   |   +-- config.py
|   |   +-- database.py
|   |   +-- models.py
|   |
|   +-- scanner/
|   |   +-- classifier.py
|   |   +-- extractor.py
|   |   +-- scanner.py
|   |
|   +-- search/
|   |   +-- engine.py
|   |
|   +-- main.py
|
+-- dashboard/
|   +-- dashboard.py
|
+-- scripts/
|   +-- create_demo_files.py
|   +-- scan.py
|
+-- tests/
|   +-- test_classifier.py
|   +-- test_scanner.py
|   +-- test_search.py
|
+-- data/
|   +-- demo_files/
|
+-- .env.example
+-- .gitignore
+-- LICENSE
+-- pyproject.toml
+-- requirements.txt
+-- README.md
```

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/charanreddy0006/smart-file-intelligence.git
cd smart-file-intelligence
```

### 2. Create a virtual environment

Windows:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## Running the Project

### Create Demo Files

The project includes a small demo dataset for testing the complete pipeline.

```bash
python scripts/create_demo_files.py
```

### Scan Files

```bash
python -m scripts.scan data/demo_files
```

Expected output:

```text
Scanned 7 files.
```

The scanner stores file metadata, extracted content, categories, and SHA-256 hashes in the SQLite database.

## Run the FastAPI Backend

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

### Available API Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /api/health` | Check application health |
| `GET /api/stats` | Get file statistics |
| `GET /api/files` | List indexed files |
| `GET /api/search` | Search indexed file content |

Example search request:

```text
GET /api/search?q=invoice
```

## Run the Dashboard

In a separate terminal:

```bash
streamlit run dashboard/dashboard.py
```

The dashboard provides:

- File statistics
- Storage information
- Duplicate detection summary
- File category visualization
- Content search
- Recent file listing

The dashboard will be available at:

```text
http://localhost:8501
```

## Testing

Run the complete test suite:

```bash
pytest -q
```

The project includes tests for:

- File classification
- SHA-256 hashing
- Directory scanning
- Search functionality

## File Classification

Files are classified using a combination of filename/content keywords and file extensions.

Supported categories include:

- Finance
- Career
- Education
- Data
- Development
- Images
- Archives
- Documents
- Other

Content-based keywords take priority over extension-based classification when applicable.

## Duplicate Detection

Each indexed file is assigned a SHA-256 hash based on its contents.

Files with identical hashes are considered potential duplicates.

For example:

```text
project_notes.md
project_notes_copy.md
```

contain identical content and are therefore detected as duplicates.

## Search

The search engine uses TF-IDF vectorization and cosine similarity to rank files according to their textual relevance to a search query.

Example queries:

```text
machine learning
invoice
python
```

The search results include:

- File name
- File path
- Category
- Relevance score
- File size

## Configuration

The application uses SQLite by default:

```text
sqlite:///data/files.db
```

A custom database URL can be configured through the `DATABASE_URL` environment variable.

Example:

```text
DATABASE_URL=sqlite:///data/files.db
```

See `.env.example` for the available configuration.

## Future Improvements

Potential extensions include:

- Support for additional document formats
- Improved natural-language search
- File preview functionality
- Advanced duplicate grouping
- Background directory monitoring
- PostgreSQL support
- Authentication and user-specific file indexing
- Search filters by category, file type, and date

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
