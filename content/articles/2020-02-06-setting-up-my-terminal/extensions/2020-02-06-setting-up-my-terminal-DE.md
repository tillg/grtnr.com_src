---
date: 2020-02-06
image: terminal.png
excerpt: Ein Leitfaden zur Einrichtung eines macOS-Terminals mit zsh, Oh My Zsh und powerlevel10k, der sich darauf konzentriert, wie die Teile zusammenpassen, anstatt nur Schritt-für-Schritt-Installationen zu zeigen.
title: Mein Terminal einrichten
tags: tech, Mac
translation: de
source_language: en
source_hash: f5c7f9c12d9c9b0aeb9d00bc77b5b34acb82f9b431a67135717df0f2c366bf27
translator: gpt-4o-2024-08-06
translate_date: 2026-02-28T09:26:48.283641+00:00
generated_by: simplified-translation-system
---

Ich weiß, es gibt viele Artikel und Erklärungen darüber, wie man sein Terminal konfiguriert und einrichtet. Trotzdem hat es bei mir mehr als 2 Stunden gedauert, bis alles so lief, wie ich es wollte. Der Grund war, dass viele der Artikel und Erklärungen eine Schritt-für-Schritt-Anleitung zur Installation bieten, aber zu wenig Hintergrundinformationen darüber, wie die Dinge im Hintergrund zusammenhängen und funktionieren. Und genau das hat mir gefehlt...

Also hier ist noch ein weiterer Artikel. Oder eher eine Sammlung von Schnipseln der Informationen, die ich als wertvoll empfand.

## Die Ausgangssituation

Mein Ziel-Setup & Anforderungen sind einfach:

- macOS (Catalina 10.15.2 zum Zeitpunkt des Schreibens)
- iTerm2 (Build 3.3.8)
- zsh (wie von Apple seit einigen macOS-Versionen bereitgestellt)
- Ich möchte ordentliche Farbgebung
- Ich möchte sehen, in welchem Git-Branch ich mich befinde - wenn das aktuelle Verzeichnis innerhalb eines Git-Repos liegt

## Die beweglichen Teile

Was mich verloren gehen ließ, war der fehlende Überblick. Daher hier die verschiedenen Teile, die in meinem Setup involviert sind:

- **zsh**: Die Shell
- **Oh My Zsh**: Ein Framework, das die zsh-Shell mit Funktionen und Design erweitert.
- **powerlevel9k**: Ein Theme für Oh My Zsh
- **Schriftarten**, die von powerlevel9k benötigt werden, um Text und Symbole anzuzeigen

Die Abhängigkeiten in dieser Liste sind von oben nach unten, d.h. die Schriftarten werden von powerlevel9k benötigt, das auf Oh My Zsh läuft, das zsh verwendet.

## Verzeichnisstruktur

Bevor wir die verschiedenen Komponenten einzeln durchgehen, hier die Verzeichnisstruktur, die wir nach der Installation aller Teile haben werden:

```text
├── $HOME
│   └── .oh-my-zsh/
│   │   └── custom/
│   │   │   └── themes/
│   │   │       └── powerlevel9k/
│   │   └── themes/
│   └── .zsh/
├── .zshrc
```

## zsh

Ich habe in der Vergangenheit bash verwendet und war zufrieden damit. Ich habe einfach mein Mac Terminal gestartet, und da war es. Und später habe ich iTerm2 verwendet, und es startete auch mit bash. Warum also zu zsh wechseln?

Dieser Artikel erklärt es schön und ausführlich. Kurz gesagt:

- Apple hat in der Vergangenheit bash verwendet, da es der De-facto-Standard war
- 2007 wechselte bash zur [GNU Public License 3.0](https://www.gnu.org/licenses/gpl-3.0.en.html), was Apple aus bestimmten Gründen nicht gefiel. Also blieben sie bei der Vor-2007-Version von bash. Und das ist alt - einschließlich [einer Sicherheitslücke](<https://www.wikiwand.com/en/Shellshock_(software_bug)>), die Apple zwang, bash für Macs zu aktualisieren.
- zsh wurde im Laufe der Zeit zum aufstrebenden De-facto-Standard, also wechselte Apple.

Und natürlich bietet [zsh modernere, coole Features](https://www.howtogeek.com/362409/what-is-zsh-and-why-should-you-use-it-instead-of-bash/).

Wie auch immer, es ist der neue Standard, es sieht gut aus - lass es uns verwenden. Da es die neue Mac-Standardshell ist, musst du es nicht installieren. Falls du einen neuen Mac hast, der mit Catalina vorinstalliert kam, verwendest du bereits zsh. Falls du deinen Mac von Mojave aktualisiert hast, musst du zsh als deine Terminal-Shell so einstellen:

```shell
chsh -s /bin/zsh
```

Das setzt zsh als die Standard-Shell.

### Konfiguration

Die Konfiguration der zsh-Shell erfolgt über Einträge in `.zshrc`, die sich in deinem `$HOME`-Verzeichnis befindet. Wie oben beschrieben, gibt es einige Komponenten, die interagieren. Einige von ihnen bieten Konfigurationsoptionen und können an verschiedenen Orten konfiguriert werden. Um den Überblick zu behalten, habe ich mich entschieden, die Komponenten an ihrem jeweiligen Standardort zu installieren und alle Konfigurationsoptionen in der `.zshrc`-Datei zu haben.

## Oh My Zsh

> Oh My Zsh ist ein Open-Source, Community-getriebenes Framework zur Verwaltung deiner zsh-Konfiguration.
> -- <cite>[Oh My Zsh website](https://ohmyz.sh/)</cite>

Grundsätzlich macht Oh My Zsh dein Terminal sehr schön (über [Themes](https://github.com/ohmyzsh/ohmyzsh/wiki/Themes)) und bietet viele hilfreiche Plugins. Eine Beispiel-Liste von ihrer [GitHub-Seite](https://github.com/ohmyzsh/ohmyzsh):

```bash
plugins=(
  git
  bundler
  dotenv
  osx
  rake
  rbenv
  ruby
)
```

Ich verwende derzeit das git-Plugin, das Abkürzungen für häufig verwendete git-Befehle bietet.

### Oh My Zsh konfigurieren

Wie erwähnt, habe ich alle Konfigurationen in meiner `$HOME/.zshrc`-Datei integriert. Die relevanten Schnipsel aus meiner `.zshrc`-Datei:

```shell
# Pfad zu deiner oh-my-zsh-Installation.
export ZSH="/Users/tgartner/.oh-my-zsh"

# Name des zu ladenden Themes festlegen.
# Siehe https://github.com/robbyrussell/oh-my-zsh/wiki/Themes
ZSH_THEME="powerlevel9k/powerlevel9k"

(...)

# Welche Plugins möchtest du laden?
# Standard-Plugins findest du in ~/.oh-my-zsh/plugins/*
# Benutzerdefinierte Plugins können zu ~/.oh-my-zsh/custom/plugins/ hinzugefügt werden
# Beispiel-Format: plugins=(rails git textmate ruby lighthouse)
# Weise hinzufügen, da zu viele Plugins den Shell-Start verlangsamen.
plugins=(git python)
```

## powerlevel10k

Hinweis: Ich habe früher [powerlevel9k](https://github.com/Powerlevel9k/powerlevel9k) verwendet, aber als ich meinen Mac im Mai 2025 installiert habe, war 9k veraltet und verwies auf [powerlevel10k](https://github.com/romkatv/powerlevel10k).

Installiere powerlevel10k gemäß ihrer [Installationsanleitung für zsh](https://github.com/romkatv/powerlevel10k?tab=readme-ov-file#oh-my-zsh).