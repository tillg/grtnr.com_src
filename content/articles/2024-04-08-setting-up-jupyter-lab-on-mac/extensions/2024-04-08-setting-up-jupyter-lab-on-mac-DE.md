---
Translation: de
Source-Language: en
Translator: gpt-4o
Translate-Date: 2025-07-04T16:43:14.603728
Source-File: /Users/tgartner/git/grtnr.com_src/content/articles/2024-04-08-setting-up-jupyter-lab-on-mac/2024-04-08-setting-up-jupyter-lab-on-mac.md
Generated-By: automatic-translation-plugin
---

```markdown
---
layout: post
date: 2024-04-08
excerpt: Die Einrichtung von Python auf einem Mac kann knifflig sein. Die Anzahl der Optionen ist groß, und sie könnten seltsam interagieren. Außerdem müssen Sie sich merken, welche Installationsmethode Sie verwendet haben, wenn Sie die Version ändern oder ein Upgrade durchführen möchten. Dieser Beitrag sollte mich daran erinnern, wie ich es gemacht habe 😉
image: python_on_mac.png
tags: tech, Mac
---

Die Einrichtung von Python auf einem Mac kann knifflig sein. Die Anzahl der Optionen ist groß, und sie könnten seltsam interagieren. Außerdem müssen Sie sich merken, welche Installationsmethode Sie verwendet haben, wenn Sie die Version ändern oder ein Upgrade durchführen möchten. Dieser Beitrag sollte mich daran erinnern, wie ich es gemacht habe 😉

## Installation von Python

Es gibt viele Möglichkeiten, Python auf einem Mac zu installieren und seine Versionen zu verwalten:

- Das auf MacOS installierte Python
- `brew`
- Anaconda
- `pyenv`
- ...

Was für mich am besten funktioniert hat, ist **pyenv**:

- Installieren Sie es: `brew install pyenv`. Ich gehe davon aus, dass Sie [Homebrew](https://brew.sh) installiert haben...
- Sehen Sie sich die angebotenen Optionen und Befehle an: `pyenv`
- Listen Sie alle Python-Versionen auf, die für pyenv verfügbar sind: `pyenv versions`
- Installieren Sie eine Version: `pyenv install 3.12` (Das ist die Python-Version, die ich derzeit verwende)
- Legen Sie die Version fest, die global verwendet wird: `pyenv global 3.12`
- Überprüfen Sie, welche Version global festgelegt ist: `pyenv global` oder `python --version`

## Arbeitsverzeichnis erstellen

Erstellen Sie das Verzeichnis, in dem Sie im Kontext Ihres Projekts arbeiten möchten. Ich halte alle meine Coding-Projekte unter `~/git`. So weiß ich, dass alle Projekte unter `~/git` nicht gesichert werden müssen, da sie in einem Git-Repo sind.

Beispiel:

```bash
cd ~/git
mkdir my_python_project
cd my_python_project
```

## Lokale Umgebung erstellen

Um meinem Projekt seine eigene Python-Umgebung bereitzustellen, verwende ich [Pythons Virtual Environments](https://docs.python.org/3/library/venv.html):

```bash
cd ~/git/my_python_project
python3.12 -m venv .venv
```

Auf diese Weise habe ich eine Umgebung im Unterverzeichnis `.env` erstellt. Um sie zu aktivieren, verwenden Sie `source .venv/bin/activate`.

**Hinweis**: Da mein `.env`-Unterverzeichnis nicht im Git-Repo sein sollte, muss es in der `.gitignore`-Datei aufgeführt werden.

## Jupyter Lab installieren

Jetzt, da ich die Python-Umgebung habe, kann ich Jupyter installieren. Stellen Sie sicher, dass ich im richtigen Verzeichnis bin und die Python-Umgebung aktiviert ist:

```bash
# Gehen Sie in mein Projektverzeichnis und aktivieren Sie die Python-Umgebung
cd ~/git/my_python_project
source .venv/bin/activate

# Installieren Sie Jupyter Lab in dieser Umgebung
pip install jupyterlab

# Sehr oft wird mir geraten, pip selbst zu aktualisieren
pip install --upgrade pip

# Starten Sie Jupyter Lab
jupyter lab
# Warten Sie nun ein wenig und Ihr Browser sollte sich unter http://localhost:8888/lab öffnen
```

## Ein neues Notebook erstellen

Ihr Browser sollte in einer frischen Jupyter Lab-Umgebung geöffnet sein:
![Eine leere Lab-Umgebung](jupyter_overview.png)

Klicken Sie auf _Notebook > Python 3_ und Ihr erstes Notebook sollte bereit sein:

![Ein frisches Notebook](jupyter_detail.png)

Um in Jupyter Lab loszulegen, folgen Sie ihrem [Benutzerhandbuch](https://jupyterlab.readthedocs.io/en/latest/user/interface.html).
```