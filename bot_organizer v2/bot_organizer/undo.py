from __future__ import annotations
from pathlib import Path
import json
from .actions import Action, safe_move

class UndoManager:
    def __init__(self, history_path: Path, trash_dir: Path):
        self.history_path = history_path
        self.trash_dir = trash_dir

    # ───────────────────────────────
    # Save actions
    # ───────────────────────────────
    def log(self, action: Action) -> None:
        self.history_path.parent.mkdir(exist_ok=True)
        with self.history_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(action.to_json(), ensure_ascii=False) + "\n")

    # ───────────────────────────────
    # Read all actions from history
    # ───────────────────────────────
    def history(self) -> list[Action]:
        if not self.history_path.exists():
            return []
        out: list[Action] = []
        text = self.history_path.read_text(encoding="utf-8")
        for line in text.splitlines():  # fixed splitline() -> splitlines()
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                out.append(Action(**data))
            except Exception:
                # skip malformed lines
                continue
        return out

    # ───────────────────────────────
    # Undo last N actions
    # ───────────────────────────────
    def undo(self, steps: int = 1) -> list[str]:
        actions = self.history()
        if steps < 1 or not actions:
            return []

        to_undo = actions[-steps:]
        messages: list[str] = []

        for a in reversed(to_undo):
            if a.kind in {"move", "rename"}:
                src = Path(a.dst)
                dst = Path(a.src)
                if src.exists():
                    dst.parent.mkdir(parents=True, exist_ok=True)
                    safe_move(src, dst)
                    messages.append(f"Reverted {a.kind}: {src} -> {dst}")
                else:
                    messages.append(f"Skipped {a.kind}: missing {src}")

            elif a.kind == "delete":
                trashed = Path(a.dst)
                original = Path(a.src)
                if trashed.exists():
                    original.parent.mkdir(parents=True, exist_ok=True)
                    safe_move(trashed, original)
                    messages.append(f"Restored deleted file: {original}")
                else:
                    messages.append(f"Missing in trash: {trashed}")

            elif a.kind == "create":
                created = Path(a.dst)
                if created.exists():
                    created.unlink()
                    messages.append(f"Removed created file: {created}")
                else:
                    messages.append(f"Already gone: {created}")

        # rewrite shortened history
        keep = actions[:-steps]
        with self.history_path.open("w", encoding="utf-8") as f:
            for k in keep:
                f.write(json.dumps(k.to_json(), ensure_ascii=False) + "\n")

        return messages
