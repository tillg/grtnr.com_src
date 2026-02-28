---
date: 2024-04-08
image: python_on_mac.png
excerpt: Python auf einem Mac einzurichten kann knifflig sein. Die Anzahl der Optionen ist groß und sie können seltsam interagieren. Außerdem musst Du Dir merken, welche Installationsmethode Du verwendet hast, wenn Du die Version ändern oder ein Upgrade durchführen möchtest. Dieser Beitrag soll mich daran erinnern, wie ich es gemacht habe 😉
tags: tech, Mac
translation: de
source_language: en
source_hash: 4a8f45fb063e6cdd92c63bb49f28bac7e91f4cd86fa9962c74171a557061123e
translator: gpt-4o-2024-08-06
translate_date: 2026-02-28T09:40:37.308622+00:00
generated_by: simplified-translation-system
---

Python auf einem Mac einzurichten kann knifflig sein. Die Anzahl der Optionen ist groß und sie können seltsam interagieren. Außerdem musst Du Dir merken, welche Installationsmethode Du verwendet hast, wenn Du die Version ändern oder ein Upgrade durchführen möchtest. Dieser Beitrag soll mich daran erinnern, wie ich es gemacht habe 😉

## Python installieren

Es gibt viele Möglichkeiten, Python auf einem Mac zu installieren und seine Versionen zu verwalten:

- Das auf MacOS installierte Python
- `brew`
- Anaconda
- `pyenv`
- ...

Was für mich am besten funktioniert hat, ist **pyenv**:

- Installiere es: `brew install pyenv`. Ich gehe davon aus, dass Du [Homebrew](https://brew.sh) installiert hast...
- Sieh Dir die angebotenen Optionen und Befehle an: `pyenv`
- Liste alle Python-Versionen auf, die pyenv zur Verfügung stehen: `pyenv versions`
- Installiere eine Version: `pyenv install 3.12` (Das ist die Python-Version, die ich derzeit benutze)
- Setze die Version, die global verwendet wird: `pyenv global 3.12`
- Überprüfe, welche Version global gesetzt ist: `pyenv global` oder `python --version`

## Arbeitsverzeichnis erstellen

Erstelle das Verzeichnis, in dem Du im Rahmen Deines Projekts arbeiten möchtest. Ich halte alle meine Coding-Projekte unter `~/git`. So weiß ich, dass alle Projekte unter `~/git` nicht gesichert werden müssen, da sie in einem Git-Repo sind.

Beispiel:

```bash
cd ~/git
mkdir my_python_project
cd my_python_project
```

## Lokale Umgebung erstellen

Um meinem Projekt seine eigene Python-Umgebung bereitzustellen, benutze ich [Pythons Virtual Environments](https://docs.python.org/3/library/venv.html):

```bash
cd ~/git/my_python_project
python3.12 -m venv .venv
```

Auf diese Weise habe ich eine Umgebung im Unterverzeichnis `.env` erstellt. Um sie zu aktivieren, benutze `source .venv/bin/activate`.

**Hinweis**: Da mein `.env`-Unterverzeichnis nicht im Git-Repo sein sollte, muss es in der `.gitignore`-Datei aufgeführt werden.

## Jupyter Lab installieren

Jetzt, wo ich die Python-Umgebung habe, kann ich Jupyter installieren. Stelle sicher, dass ich im richtigen Verzeichnis bin und die Python-Umgebung aktiviert ist:

```bash
# Gehe in mein Projektverzeichnis und aktiviere seine Python-Umgebung
cd ~/git/my_python_project
source .venv/bin/activate

# Installiere Jupyter Lab in dieser Umgebung
pip install jupyterlab

# Sehr oft werde ich aufgefordert, pip selbst zu aktualisieren
pip install --upgrade pip

# Starte Jupyter Lab
jupyter lab
# Warte jetzt ein bisschen und Dein Browser sollte sich auf http://localhost:8888/lab öffnen
```

## Ein neues Notebook erstellen

Dein Browser sollte in einer frischen Jupyter Lab-Umgebung geöffnet sein:
![Eine leere Lab-Umgebung](jupyter_overview.png)

Klicke auf _Notebook > Python 3_ und Dein erstes Notebook sollte bereit sein:

![Ein frisches Notebook](jupyter_detail.png)

Um in Jupyter Lab loszulegen, folge ihrem [Benutzerhandbuch](https://jupyterlab.readthedocs.io/en/latest/user/interface.html).