from __future__ import annotations
from pathlib import Path
from .rules import Rules
from .actions import Action, safe_move, safe_delete
from .config import ensure_app_dirs, TRASH_DIRNAME
from .undo import UndoManager


def organize_path(root: Path, rules: Rules, dry_run: bool = False) -> list[str]:
    app_dir, history_path, trash_dir = ensure_app_dirs(root)
    undo = UndoManager(history_path, trash_dir)
    logs: list[str] = []

    for p in root.rglob("*"):
        if not p.is_file():
            continue
        #skip app internals
        if app_dir in p.parents:
            continue
        rel = p.relative_to(root)
        target_subdir = rules.match_target(rel)

        if not target_subdir:
            continue
        dst = root / target_subdir / p.name
        if dst == p:
            continue  # already in the right place  
        if dry_run:
            logs.append(f'DRY : move {rel} -> {dst.relative_to(root)}')
        else:
            safe_move(p, dst)
            undo.log(Action.move(src=p, dst=dst))
            logs.append(f'Moved: {rel} -> {dst.relative_to(root)}')
    return logs

def delete_empty_dirs(root: Path, dry_run: bool = False) -> list[str]:
    app_dir, history_path, trash_dir = ensure_app_dirs(root)
    undo = UndoManager(history_path, trash_dir)
    logs: list[str] = []

    # walk bottom-up (deepest first)
    for d in sorted((p for p in root.rglob("*") if p.is_dir()),
                    key=lambda p: len(p.parts), reverse=True):
        # skip our internal dir
        if d == app_dir or app_dir in d.parents:
            continue

        if any(d.iterdir()):
            continue

        rel = d.relative_to(root)
        if dry_run:
            logs.append(f"DRY: delete dir {rel}")
            continue

        trash_dest = trash_dir / rel
        moved_to = safe_delete(d, trash_dest)
        undo.log(Action.delete(src=d, dst=moved_to))
        logs.append(f"Deleted empty dir {rel}")

    return logs

                
           