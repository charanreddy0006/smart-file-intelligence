from pathlib import Path
from app.scanner.classifier import classify_file

def test_extension_classification():
    assert classify_file(Path("sales.csv")) == "Data"
    assert classify_file(Path("photo.png")) == "Images"
    assert classify_file(Path("main.py")) == "Development"

def test_keyword_classification():
    assert classify_file(Path("monthly.txt"), "This is an invoice for a software payment.") == "Finance"
