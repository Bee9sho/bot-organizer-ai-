# 🧠 bot-organizer v0.2.1
### Automated file organizer with undo, history, and YAML rules.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Version](https://img.shields.io/badge/Version-0.2.1-orange)

---

## 🚀 Overview
**bot-organizer** automatically sorts and cleans your folders using simple YAML or JSON rules.  
Every action is tracked, so you can safely undo any move, rename, or deletion.

---

## ⚙️ Features
- ✅ Organize files by extension, type, or pattern  
- 🔄 Undo or restore moved/deleted files easily  
- 🧱 Dry-run mode for safe previews  
- 🧹 Delete empty folders automatically  
- 🕹️ CLI interface powered by [Typer](https://typer.tiangolo.com)  
- 🧾 YAML & JSON rules supported  

---

## 🧩 Example Usage

### 🔍 Preview organization (dry-run)
```bash
bot-organizer organize --src "C:\Users\<you>\Downloads" --rules "rules.yaml" --dry-run
```

### 🚚 Apply changes for real
```bash
bot-organizer organize --src "C:\Users\<you>\Downloads" --rules "rules.yaml"
```

### 🧾 View history
```bash
bot-organizer history --src "C:\Users\<you>\Downloads"
```

### 🔙 Undo the last action
```bash
bot-organizer undo --src "C:\Users\<you>\Downloads" --steps 1
```

### 🧹 Remove empty folders after organizing
```bash
bot-organizer organize --src "C:\Users\<you>\Downloads" --rules "rules.yaml" --delete-empties
```

---

## 📘 Example Rules (`rules.yaml`)
```yaml
patterns:
  # Documents
  - match: "*.pdf"
    to: "Documents/PDF"
  - match: "*.docx"
    to: "Documents/Word"
  - match: "*.xlsx"
    to: "Documents/Excel"
  - match: "*.pptx"
    to: "Documents/PowerPoint"
  - match: "*.txt"
    to: "Documents/Text"

  # Images
  - match: "*.jpg"
    to: "Pictures"
  - match: "*.png"
    to: "Pictures"
  - match: "*.jpeg"
    to: "Pictures"

  # Media
  - match: "*.mp3"
    to: "Music"
  - match: "*.mp4"
    to: "Videos"

  # Archives & Installers
  - match: "*.zip"
    to: "Archives"
  - match: "*.rar"
    to: "Archives"
  - match: "*.exe"
    to: "Installers"
  - match: "*.msi"
    to: "Installers"

  # Torrents
  - match: "*.torrent"
    to: "Torrents"
```

---

## 🧰 Installation

```bash
git clone https://github.com/Bee9sho/bot-organizer-ai.git
cd bot-organizer-ai
python -m venv .venv
. .venv/Scripts/Activate.ps1
pip install -e .
```

---

## 🧾 Version History
### v0.2.1
- Added README.md  
- Minor cleanup and polish  

### v0.2.0
- Modularized project structure  
- Added undo & history system  
- Added YAML rules support  
- Implemented CLI interface with `--dry-run` and `--delete-empties`  

---

## 🧭 Roadmap (v0.3 Preview)
- ➕ `--undo-all` flag to revert all actions  
- 📊 Summary of total files moved/skipped  
- 🪵 Optional log file at `.bot_organizer/log.txt`  
- 🪟 (Future) GUI preview mode  

---

## 👤 Author
**  Bashar **  
[GitHub Profile](https://github.com/Bee9sho)

---

## 🪪 License
This project is licensed under the **MIT License**.
