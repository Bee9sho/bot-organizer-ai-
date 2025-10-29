# ==========================
# bot-organizer v0.2


Organize files by YAML rules and safely undo operations.


```bash
bot-organizer organize --src D:\Downloads --rules rules.yaml
bot-organizer undo --steps 1
bot-organizer history
```


Rules example (rules.yaml):


```yaml
patterns:
- match: "*.jpg"
to: "Pictures"
- match: "*.pdf"
to: "Documents/PDF"
```

