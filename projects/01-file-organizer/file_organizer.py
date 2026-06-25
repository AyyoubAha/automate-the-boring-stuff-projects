"""Simple file organizer.

Usage:
    python file_organizer.py /path/to/folder

This beginner project sorts files into folders based on their file extensions.
It is intentionally simple and readable so I can improve it over time.
"""

from pathlib import Path
import shutil
import sys

FILE_CATEGORIES = {
    "images": {".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg"},
    "documents": {".pdf", ".doc", ".docx", ".txt", ".md"},
    "spreadsheets": {".csv", ".xls", ".xlsx"},
    "archives": {".zip", ".rar", ".7z", ".tar", ".gz"},
    "code": {".py", ".js", ".html", ".css", ".json"},
}


def get_category(file_path: Path) -> str:
    """Return the category folder name for a file."""
    extension = file_path.suffix.lower()

    for category, extensions in FILE_CATEGORIES.items():
        if extension in extensions:
            return category

    return "other"


def organize_folder(folder_path: Path) -> None:
    """Organize files in the given folder by file type."""
    if not folder_path.exists():
        print(f"Error: folder does not exist: {folder_path}")
        return

    if not folder_path.is_dir():
        print(f"Error: path is not a folder: {folder_path}")
        return

    moved_files = 0

    for item in folder_path.iterdir():
        if item.is_dir():
            continue

        category = get_category(item)
        target_folder = folder_path / category
        target_folder.mkdir(exist_ok=True)

        target_path = target_folder / item.name

        if target_path.exists():
            print(f"Skipped duplicate: {item.name}")
            continue

        shutil.move(str(item), str(target_path))
        moved_files += 1
        print(f"Moved {item.name} -> {category}/")

    print(f"Done. Moved {moved_files} file(s).")


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python file_organizer.py /path/to/folder")
        return

    folder_path = Path(sys.argv[1]).expanduser().resolve()
    organize_folder(folder_path)


if __name__ == "__main__":
    main()
