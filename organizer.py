from __future__ import annotations
import argparse
import os
import shutil
from pathlib import Path

EXT_MAP = {
    # Images
    ".jpg": "Images", ".jpeg": "Images", ".png": "Images", ".gif": "Images", ".webp": "Images", ".svg": "Images",
    # Videos
    ".mp4": "Videos", ".mov": "Videos", ".avi": "Videos", ".mkv": "Videos",
    # Audio
    ".mp3": "Audio", ".wav": "Audio", ".flac": "Audio", ".m4a": "Audio",
    # Documents
    ".pdf": "Docs", ".doc": "Docs", ".docx": "Docs", ".xls": "Docs", ".xlsx": "Docs",
    ".ppt": "Docs", ".pptx": "Docs", ".txt": "Docs", ".csv": "Docs",
    # Archives
    ".zip": "Archives", ".rar": "Archives", ".7z": "Archives", ".tar": "Archives", ".gz": "Archives",
    # Code
    ".py": "Code", ".js": "Code", ".ts": "Code", ".html": "Code", ".css": "Code",
    ".json": "Code", ".yml": "Code", ".yaml": "Code", ".ini": "Code",
}
DEFAULT_CATEGORY = "Other"

def choose_category(path: Path) -> str:
    return EXT_MAP.get(path.suffix.lower(), DEFAULT_CATEGORY)

def ensure_folder(root: Path, category: str) -> Path:
    dest = root / category
    dest.mkdir(exist_ok=True)
    return dest

def uniquify(dest_dir: Path, name: str) -> Path:
    """If file exists, append (1), (2), ... before the extension."""
    base = Path(name).stem
    ext = Path(name).suffix
    candidate = dest_dir / name
    i = 1
    while candidate.exists():
        candidate = dest_dir / f"{base} ({i}){ext}"
        i += 1
    return candidate

def iter_files(root: Path, recursive: bool):
    if recursive:
        for p in root.rglob("*"):
            if p.is_file():
                yield p
    else:
        for p in root.iterdir():
            if p.is_file():
                yield p

def organize(root: Path, apply: bool, recursive: bool) -> tuple[int, int]:
    moved = 0
    skipped = 0

    for entry in iter_files(root, recursive):
        # skip files already inside our category folders at the root
        if entry.parent == root and entry.name in EXT_MAP.values():
            skipped += 1
            continue

        category = choose_category(entry)
        dest_dir = ensure_folder(root, category)
        target = uniquify(dest_dir, entry.name)

        # Don’t move if source and target are the same file
        if entry.resolve() == target.resolve():
            skipped += 1
            continue

        if apply:
            shutil.move(str(entry), str(target))
            print(f"[OK ] {entry.relative_to(root)}  →  {target.relative_to(root)}")
            moved += 1
        else:
            print(f"[DRY] {entry.relative_to(root)}  →  {target.relative_to(root)}")

    return moved, skipped

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Neat File Organizer — sorts files by type into subfolders."
    )
    parser.add_argument(
        "--path", "-p",
        type=Path,
        default=Path.home() / "Downloads",
        help="Target folder to organize (default: your Downloads)."
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Actually move files (default is dry-run)."
    )
    parser.add_argument(
        "--recursive", "-r",
        action="store_true",
        help="Include files inside subfolders."
    )
    return parser.parse_args()

def main():
    args = parse_args()
    root = args.path.expanduser().resolve()
    print(f"Organizing folder: {root}")
    moved, skipped = organize(root, apply=args.apply, recursive=args.recursive)
    label = "APPLIED" if args.apply else "dry-run"
    print(f"\nSummary ({label}): moved={moved}, skipped={skipped}")

if __name__ == "__main__":
    main()
