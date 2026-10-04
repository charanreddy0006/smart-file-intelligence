from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEMO = ROOT / "data" / "demo_files"

files = {
    "education/machine_learning_notes.txt": "Machine learning notes covering regression, classification, decision trees and model evaluation.",
    "career/resume.txt": "Resume and career information including Python, SQL, data engineering and internship experience.",
    "finance/invoice_2026.txt": "Invoice for software services. Payment due within thirty days. Finance record for 2026.",
    "development/python_project.py": "def calculate_average(values):\n    return sum(values) / len(values)\n",
    "data/sales.csv": "product,region,revenue\nLaptop,West,120000\nPhone,North,95000\n",
    "documents/project_notes.md": "# Project Notes\n\nSoftware architecture and implementation notes.",
}

for relative, content in files.items():
    path = DEMO / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")

source = DEMO / "documents/project_notes.md"
duplicate = DEMO / "documents/project_notes_copy.md"
duplicate.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")

print(f"Created demo files in: {DEMO}")
