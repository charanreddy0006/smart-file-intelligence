import sys
from app.scanner.scanner import scan_directory

if __name__ == "__main__":
    directory = sys.argv[1] if len(sys.argv) > 1 else "data/demo_files"
    count = scan_directory(directory)
    print(f"Scanned {count} files.")
