from __future__ import annotations
from dataclasses import dataclass, asdict
from pathlib import Path
import shutil
import time

@dataclass
class Action:
    kind: str
    ts: float
    src: str | None
    dst: str | None

    def to_json(self) -> dict:
        return asdict(self)
    
    @classmethod
    def move(cls, src: Path, dst: Path) -> "Action":
        return cls("move", time.time(), str(src), str(dst))
    
    @classmethod
    def rename(cls, src: Path, dst: Path) -> "Action":
        return cls("rename", time.time(), str(src), str(dst))
    
    @classmethod
    def delete(cls, src: Path, dst: Path) -> "Action":
        return cls("delete", time.time(), str(src), str(dst))
    
    @classmethod
    def create(cls, dst: Path) -> "Action":
        return cls("create", time.time(), None, str(dst))
    

def safe_move(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(src), str(dst))

def safe_rename(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    src.rename(dst)

def safe_delete(src: Path, trash: Path) -> Path:
    trash.parent.mkdir(parents=True, exist_ok=True)
    trash = _unique_path(trash)
    shutil.move(str(src), str(trash))
    return trash

def _unique_path(p: Path) -> Path:
    if not p.exists():
        return p
    stem, suf = p.stem, p.suffix
    parent = p.parent
    i = 1
    while True:
        candidate = parent / f"{stem} ({i}){suf}"
        if not candidate.exists():
            return candidate
        i += 1