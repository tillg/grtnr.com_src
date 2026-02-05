---
date: 2025-01-15
excerpt: Ich nutze verschiedene Entwicklerwerkzeuge (Java, Python, Docker...), aber einige davon verwende ich nur selten. Daher vergesse ich, wie ich sie installiert habe, welchen Versionsmanager ich verwendet habe usw. Dies ist also die Notiz an mein zukünftiges Ich, um es nachzuschlagen.
image: dev_tools.png
tags: Mac
updates: 2025-05-05
translation: de
source_language: en
source_hash: 24d38d9c2e2f45130aedf37c7363273d49dd0e3f56191a888368eef4b0e3a296
translator: gpt-4o-2024-08-06
translate_date: 2026-02-05T15:44:28.040451
generated_by: simplified-translation-system
---

![Lustiges Bild von KI](dev_tools.png)

Ich bin kein professioneller Entwickler, ich mache es zum Spaß. Und ich spiele gerne herum, entdecke neue Technologien, entwickle alle möglichen kleinen Dinge. Manchmal brauche ich Python, manchmal React/Typescript, Java und mehr. Für jedes Entwicklungswerkzeug oder jede Sprache gibt es mehrere Möglichkeiten, wie man sie installieren und ihre Versionen verwalten kann. Da ich dazu neige, Dinge wie "Wie habe ich Python auf diesem Rechner installiert?" zu vergessen, ist dies eine Notiz an mein zukünftiges Ich, die mir sagt, wie ich jedes Entwicklungswerkzeug installiert habe.

Da sich die Art und Weise, wie bestimmte Pakete installiert werden, im Laufe der Zeit ändern kann, werde ich Daten zu meinen Installationsentscheidungen hinzufügen.

[TOC]

## Xcode

Xcode ist das grundlegende Entwicklerwerkzeug auf dem Mac. Es enthält git und andere grundlegende Werkzeuge und Compiler.

Ich installiere es aus dem Apple App Store.

## Terminal

Mein bevorzugtes Terminal ist [iTerm2](https://iterm2.com), und ich installiere es einfach von der Website. Siehe [hier](/setting-up-my-terminal/), wie ich es konfiguriere.

## zsh shell

Auf einem neuen Mac mache ich Folgendes:

```shell
# Überprüfen, welche Shell ich habe
echo "$SHELL"

# Falls es nicht zsh ist, als Standard festlegen
chsh -s "$(which zsh)"

```

## VSCode

... oder VSCode-insiders

**Erweiterungen:**

- **markdownlint** von David Anson (`davidanson.vscode-markdownlint`) - Der De-facto-Standard für Markdown-Linting mit über 10 Millionen Downloads. Unterstreicht Probleme inline und kann beim Speichern automatisch korrigieren.
  `code --install-extension davidanson.vscode-markdownlint`
  Konfigurationsdateien werden in folgender Reihenfolge gesucht: `.markdownlint.jsonc`, `.markdownlint.json`, `.markdownlint.yaml`/`.yml` oder `.markdownlintrc`. (Hinzugefügt im Januar 2026)

- **Prettier** (`esbenp.prettier-vscode`) - Code-Formatter.
  `code --install-extension esbenp.prettier-vscode`
  Formatierung beim Speichern in den VS Code-Einstellungen aktivieren:

  ```json
  {
    "[markdown]": {
      "editor.defaultFormatter": "esbenp.prettier-vscode",
      "editor.formatOnSave": true
    }
  }
  ```

  (Hinzugefügt im Januar 2026)

## Docker

**Januar 2025:** Ich bin von [Docker Desktop](https://www.docker.com/products/docker-desktop/) zu [Rancher Desktop](https://rancherdesktop.io) gewechselt.

Installationshinweis: Die Apple Silicon-Version heruntergeladen, das DMG geöffnet und in mein Anwendungsverzeichnis kopiert. Das einzige Detail, das ich tun musste, war, das Kontrollkästchen "Administrative Access" in den Einstellungen zu aktivieren.
![alt text](rancher_prefs.png)

_Registry_: Ich verwende verschiedene Registries, wenn ich an verschiedenen Projekten arbeite.

_Frage_: Wie konfiguriere ich Docker so, dass es Images aus einem bestimmten Registry zieht?

## Java

Dies sind die Optionen, die ich gesehen habe:

- [jenv](https://github.com/jenv/jenv)
- [SDK man](https://sdkman.io)

**Januar 2025**: Ich habe mich entschieden, SDK Man zu verwenden, da es auch Maven abdeckt.

**Mini-Cheatsheet**

- `sdk install java 17.0.12-jbr` installiert diese spezifische Java-Version
- `sdk list java` zeigt alle verfügbaren Java-Versionen (zum Installieren) an
- Um die installierten Java-Versionen aufzulisten:
  - `sdk offline enable`, sodass nur lokal installierte Versionen aufgelistet werden
  - `sdk list java`
  - `sdk offline disable`
- `sdk default java 21.0.6-amzn` setzt diese Version als Standard
  Um eine Java-Version als Standard in einem Verzeichnis festzulegen, siehe den [Env-Befehl](https://sdkman.io/usage/#env-command)

## Maven

Ich verwende einfach `brew install maven`. Für ältere Versionen installiert `brew install maven30` Maven 3.0.

## Gradle

**Januar 2025**: Ich habe mich entschieden, SDK Man auch für Gradle zu verwenden.

Grund: `brew install gradle` installierte Gradle Version 8.12.1, aber für das aktuelle Projekt benötigte ich 8.5.

- `sdk install gradle 8.5`: Installiert die spezifische Gradle-Version
- `sdk use gradle 8.5`

## Node und npm

**Januar 2025** Ich habe mich entschieden, [nvm](https://github.com/nvm-sh/nvm) zu verwenden.

**Mini-Cheatsheet**

- `nvm use 16`
- `node -v` zeigt die aktuell verwendete Version an
- `nvm install 12` installiert Node 12 und verwendet es

## Python

- **Sommer 2024**: Ich verwende [pyenv](https://github.com/pyenv/pyenv)
- Um pyenv zu installieren: `brew install pyenv`

**Mini-Cheatsheet**

Um eine mit Pyenv installierte Python-Version auszuwählen, führen Sie einen der folgenden Befehle aus:

```shell
pyenv install 3.12
pyenv shell <version> -- nur für die aktuelle Shell-Sitzung auswählen
pyenv local <version> -- automatisch auswählen, wenn Sie sich im aktuellen Verzeichnis (oder dessen Unterverzeichnissen) befinden
pyenv global <version> -- global für Ihr Benutzerkonto auswählen
```

## Markdown Linting

`brew install markdownlint-cli2`

## Ruby

Noch nicht durchdacht. Vermeiden Sie Ruby im Allgemeinen... 😉