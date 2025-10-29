from __future__ import annotations
from pathlib import Path
import typer
from typing import Optional
from .rules import load_rules
from .organizer import organize_path, delete_empty_dirs
from .config import ensure_app_dirs
from .undo import UndoManager


app = typer.Typer(add_completion=False, help ="Organize files by rules with undo support.")

@app.command()
def organize(
    src: Path = typer.Option(..., "--src", help="Folder to organize"),
    rules: Path = typer.Option(..., "--rules", help="YAML/JSON rules file"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Preview without changing files"),
    delete_empties: bool = typer.Option(False, "--delete-empties", help="Also remove now-empty folders"),
):
    r = load_rules(rules)
    logs = organize_path(src, r, dry_run=dry_run)
    if delete_empties:
        logs += delete_empty_dirs(src, dry_run=dry_run)

    # <-- always print results
    if logs:
        for line in logs:
            typer.echo(line)
    else:
        typer.echo("No actions. Nothing matched your rules.")

    
@app.command()
def undo(steps: int = typer.Option(1, "--steps", help="How many actions to undo"), src: Path = typer.Option(..., "--src", help="Project root used for history")):
    _, history_path, trash_dir = ensure_app_dirs(src)
    um = undo = UndoManager(history_path, trash_dir)
    msgs = um.undo(steps=steps)
    for m in msgs:
        typer.echo(m)


@app.command()
def history(src: Path = typer.Option(..., "--src", help="Project root used for history")):
    _, history_path, trash_dir = ensure_app_dirs(src)
    um = UndoManager(history_path, trash_dir)
    for a in um.history():
        typer.echo(f'{a.kind}: {a.src} -> {a.dst}')

if __name__ == "__main__":
    app()

