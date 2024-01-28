# CanSat

TODO Beschreibung:
- ENTWICKLUNGSUMGEBUNG (SIEHE UNTEN)
- Öffentlichkeitsarbeit (Bericht, ...)
- Gehäuse (mehrere wenn möglich zum Testen)
- Stromversorgung
- Fallschirme (testen mit Gehäuse)
- Akkzelerometer bei über 16G testen
- Lora-Modul senden testen 



## Entwicklungsumgebung

### Quickstart

- github account anlegen (falls nicht vorhanden)
- git installieren (siehe unten)
- python installieren
- vscode + python plugin installieren (siehe unten)

### Links

- Git
    - https://git-scm.com/download/win (command line, unbedingt notwendig)
    - https://tortoisegit.org/download/ (gui plugin für windows explorer, angenehm)

- Python
    - https://www.python.org/ftp/python/3.12.1/python-3.12.1-embed-amd64.zip
    irgendwo entpacken und in VSCode (siehe unten) beim ersten Mal starten eines Python-Programs den Pfad zu python.exe angeben

- [VSCode](https://code.visualstudio.com/)
    - [Python PlugIn](https://marketplace.visualstudio.com/items?itemName=ms-python.python), einfach direkt in VSCode suchen/installieren

### TortoiseGit mit SSH Key konfigurieren

1. Git Bash terminal öffnen
    - `ssh-keygen -t ed25519 -C "your_email@example.com"`
2. `C:\Users\YOUR_USERNAME\.ssh\id_ed25519.pub` auf github unter settings/SSH... dazufügen (New SSH Key)
3. Puttygen starten
    - File/Load Private Key   (`.ssh\id_ed25519`, das File OHNE .pub)
    - Save Private Key Button -> speichern als `.ssh\id_ed25519.ppk`
4. in tortoisegit/settings/git/remote/origin/putty-key die Datei `.ssh\id_ed25519.ppk` angeben