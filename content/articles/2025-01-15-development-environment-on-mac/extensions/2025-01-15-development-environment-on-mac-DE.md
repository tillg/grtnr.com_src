---
date: 2025-01-15
excerpt: I use different dev tools (Java, Python, Docker...) but I use some of them only rarely. So I forget how I installed them, what version manager I used etc. So this is the note to future me to look it up.
image: dev_tools.png
tags: Mac
updates: 2025-05-05
Translation: de
Source-Language: en
Translator: gpt-4o
Translate-Date: 2025-07-09T08:08:30.721892
Source-File: /Users/tgartner/git/grtnr.com_src/content/articles/2025-01-15-development-environment-on-mac/2025-01-15-development-environment-on-mac.md
Generated-By: automatic-translation-plugin
---

![Lustiges Bild von KI](dev_tools.png)

Ich bin kein professioneller Entwickler, ich mache es zum Spaß. Und ich mag es, herumzuspielen, neue Technologien zu entdecken und alle möglichen kleinen Dinge zu entwickeln. Manchmal brauche ich Python, manchmal React/Typescript, Java und mehr. Für jedes Entwicklungstool oder jede Sprache gibt es mehrere Optionen, wie man sie installiert und ihre Versionen verwaltet. Da ich dazu neige, Dinge wie "Wie habe ich Python auf diesem Rechner installiert?" zu vergessen, ist dies eine Notiz an mein zukünftiges Ich, die mir sagt, wie ich jedes Entwicklungstool installiert habe.

Da sich die Art und Weise, wie bestimmte Pakete installiert werden, im Laufe der Zeit ändern kann, werde ich meinen Installationsentscheidungen Daten hinzufügen.

[TOC]

## Xcode

Xcode ist das grundlegende Entwicklungstool auf dem Mac. Es enthält git und andere grundlegende Werkzeuge und Compiler.

Ich installiere es aus dem Apple App Store.

## Terminal

Mein bevorzugtes Terminal ist [iTerm2](https://iterm2.com), und ich installiere es einfach von der Website. Siehe [hier](/setting-up-my-terminal/) für die Konfiguration.

## zsh Shell

Auf einem neuen Mac mache ich Folgendes:

```shell
# Überprüfen, welche Shell ich habe
echo "$SHELL"

# Falls es nicht zsh ist, als Standard setzen
chsh -s "$(which zsh)"

```

## VSCode

... oder VSCode-insiders

## Docker

**Januar 2025:** Ich bin von [Docker Desktop](https://www.docker.com/products/docker-desktop/) zu [Rancher Desktop](https://rancherdesktop.io) gewechselt.

Installationshinweis: Ich habe die Apple Silicon-Version heruntergeladen, das DMG geöffnet und es in mein Anwendungsverzeichnis kopiert. Das einzige Detail, das ich tun musste, war, das Kontrollkästchen "Administrative Access" in den Einstellungen zu aktivieren.
![alternativer Text](rancher_prefs.png)

_Registry_: Ich verwende verschiedene Registries, wenn ich an verschiedenen Projekten arbeite.

_Frage_: Wie konfiguriere ich Docker so, dass es Images aus einer bestimmten Registry zieht?

## Java

Dies sind die Optionen, die ich gesehen habe:

- [jenv](https://github.com/jenv/jenv)
- [SDK man](https://sdkman.io)

**Januar 2025**: Ich habe mich entschieden, SDK Man zu verwenden, da es auch Maven abdeckt.

**Mini-Cheatsheet**

- `sdk install java 17.0.12-jbr` installiert diese spezifische Java-Version
- `sdk list java` zeigt alle verfügbaren Java-Versionen (zum Installieren) an
- Um die installierten Java-Versionen aufzulisten:
  - `sdk offline enable`, so werden nur lokal installierte Versionen aufgelistet
  - `sdk list java`
  - `sdk offline disable`
- `sdk default java 21.0.6-amzn` setzt diese Version als Standard
  Um eine Java-Version als Standard in einem Verzeichnis festzulegen, siehe den [Env-Befehl](https://sdkman.io/usage/#env-command)

## Maven

Ich verwende einfach `brew install maven`. Für ältere Versionen installiert `brew install maven30` Maven 3.0.

## Gradle

**Januar 2025**: Ich entscheide mich auch für Gradle, SDK Man zu verwenden.

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

Um eine von Pyenv installierte Python-Version auszuwählen, führen Sie einen der folgenden Befehle aus:

```shell
pyenv install 3.12
pyenv shell <version> -- nur für die aktuelle Shell-Sitzung auswählen
pyenv local <version> -- automatisch auswählen, wann immer Sie sich im aktuellen Verzeichnis (oder dessen Unterverzeichnissen) befinden
pyenv global <version> -- global für Ihr Benutzerkonto auswählen
```

## Ruby

Noch nicht darüber nachgedacht. Vermeiden Sie Ruby im Allgemeinen... 😉