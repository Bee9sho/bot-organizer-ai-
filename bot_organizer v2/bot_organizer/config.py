from __future__ import annotations
from pathlib import Path

APP_DIRNAME = ".bot_organizer"
HISTORY_FILE = "history.jsonl"
TRASH_DIRNAME = "_trash"

def ensure_app_dirs(root: Path) -> tuple[Path, Path, Path]:
    app_dir = (root / APP_DIRNAME)
    app_dir.mkdir(exist_ok=True)
    history_path = app_dir / HISTORY_FILE
    trash_dir = app_dir / TRASH_DIRNAME
    trash_dir.mkdir(exist_ok=True)
    return app_dir, history_path, trash_dir