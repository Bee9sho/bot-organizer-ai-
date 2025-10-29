from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from fnmatch import fnmatch
import json
import yaml

@dataclass
class Rule:
    match : str
    to : str

@dataclass
class Rules:
    patterns: list[Rule]
    @classmethod
    def from_dict(cls, data: dict) -> "Rules":
        pats = [Rule(**r) for r in data.get("patterns", [])]
        return cls(patterns=pats)
    
    def match_target(self, rel_path: Path) -> str | None:
        s = str(rel_path)
        for r in self.patterns:
            if fnmatch(s, r.match):
                return Path(r.to)
        return None

def load_rules(path: Path) -> Rules:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() in [".yml", ".yaml"]:
        data = yaml.safe_load(text)
    else:
        data = json.loads(text)
    return Rules.from_dict(data)