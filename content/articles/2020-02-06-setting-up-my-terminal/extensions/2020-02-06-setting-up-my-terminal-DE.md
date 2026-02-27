---
image: terminal.png
excerpt: Eine Anleitung zur Einrichtung eines macOS-Terminals mit zsh, Oh My Zsh und powerlevel10k, die sich darauf konzentriert, wie die Teile zusammenpassen, anstatt nur eine Schritt-für-Schritt-Installation zu bieten.
title: Einrichten meines Terminals
tags: tech, Mac
translation: de
source_language: en
source_hash: 73903e9580cb1ea1f652ef2f6d4d2a0c623b05e7b5296a61c6114e14f28fc354
translator: gpt-4o-2024-08-06
translate_date: 2026-02-27T10:05:32.661000+00:00
generated_by: simplified-translation-system
---

Ich weiß, es gibt viele Artikel und Erklärungen darüber, wie man sein Terminal konfiguriert und einrichtet. Dennoch hat es bei mir mehr als 2 Stunden gedauert, bis alles so funktionierte, wie ich es wollte. Der Grund war, dass viele der Artikel und Erklärungen eine Schritt-für-Schritt-Anleitung zur Installation bieten, aber wenig Hintergrundinformationen darüber, wie die Dinge zusammenhängen und im Hintergrund funktionieren. Und genau das hat mir gefehlt...

Also hier ist ein weiterer Artikel. Oder eher eine Sammlung von Informationsschnipseln, die ich als wertvoll empfand.

## Die Ausgangssituation

Mein Ziel-Setup und meine Anforderungen sind einfach:

- macOS (Catalina 10.15.2 zum Zeitpunkt des Schreibens)
- iTerm2 (Build 3.3.8)
- zsh (wie von Apple seit einigen macOS-Versionen bereitgestellt)
- Ich möchte eine ordentliche Farbgebung
- Ich möchte sehen, in welchem Git-Branch ich mich befinde - wenn das aktuelle Verzeichnis innerhalb eines Git-Repos liegt

## Die beweglichen Teile

Was mich verloren gehen ließ, war der fehlende Überblick. Daher hier die verschiedenen Teile, die in meinem Setup involviert sind:

- **zsh**: Die Shell
- **Oh My Zsh**: Ein Framework, das die zsh-Shell mit Funktionen und Design erweitert.
- **powerlevel9k**: Ein Theme für Oh My Zsh
- **Schriften**, die von powerlevel9k benötigt werden, um Text und Symbole anzuzeigen

Die Abhängigkeiten in dieser Liste sind von oben nach unten, d.h. die Schriften werden von powerlevel9k benötigt, das auf Oh My Zsh läuft, das zsh verwendet.

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

Ich habe in der Vergangenheit bash verwendet und war damit zufrieden. Ich habe einfach mein Mac Terminal gestartet, und da war es. Später habe ich iTerm2 verwendet, und es startete auch mit bash. Warum also zu zsh wechseln?

Dieser Artikel erklärt es schön und ausführlich. Kurz gesagt:

- Apple hat in der Vergangenheit bash verwendet, da es der De-facto-Standard war
- 2007 wechselte bash zur [GNU Public License 3.0](https://www.gnu.org/licenses/gpl-3.0.en.html), was Apple aus bestimmten Gründen nicht gefiel. Also blieben sie bei der vor-2007-Version von bash. Und das ist alt - einschließlich einer [Sicherheitslücke](<https://www.wikiwand.com/en/Shellshock_(software_bug)>), die Apple zwang, bash für Macs zu aktualisieren.
- zsh wurde im Laufe der Zeit zum aufstrebenden De-facto-Standard, also wechselte Apple.

Und natürlich bietet [zsh modernere, coole Funktionen](https://www.howtogeek.com/362409/what-is-zsh-and-why-should-you-use-it-instead-of-bash/).

Wie dem auch sei, es ist der neue Standard, es sieht gut aus - lassen Sie es uns verwenden. Da es die neue macOS-Standardshell ist, müssen Sie es nicht installieren. Falls Sie einen neuen Mac haben, der mit Catalina vorinstalliert kam, verwenden Sie bereits zsh. Falls Sie Ihren Mac von Mojave aktualisiert haben, müssen Sie zsh als Ihre Terminal-Shell wie folgt einstellen:

```shell
chsh -s /bin/zsh
```

Dies setzt zsh als die Standard-Shell.

### Konfiguration

Die Konfiguration der zsh-Shell erfolgt über Einträge in `.zshrc`, die sich in Ihrem `$HOME`-Verzeichnis befindet. Wie oben beschrieben, gibt es einige Komponenten, die interagieren. Einige von ihnen bieten Konfigurationsoptionen und können an verschiedenen Stellen konfiguriert werden. Um den Überblick zu behalten, habe ich mich dafür entschieden, die Komponenten an ihrem jeweiligen Standardort zu installieren und alle Konfigurationsoptionen in der `.zshrc`-Datei zu haben.

## Oh My Zsh

> Oh My Zsh ist ein Open-Source, Community-getriebenes Framework zur Verwaltung Ihrer zsh-Konfiguration.
> -- <cite>[Oh My Zsh-Website](https://ohmyz.sh/)</cite>

Grundsätzlich macht Oh My Zsh Ihr Terminal sehr ansprechend (über [Themes](https://github.com/ohmyzsh/ohmyzsh/wiki/Themes)) und bietet viele hilfreiche Plugins. Eine Beispiel-Liste von ihrer [GitHub-Seite](https://github.com/ohmyzsh/ohmyzsh):

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

### Konfiguration von Oh My Zsh

Wie erwähnt, habe ich alle Konfigurationen in meine `$HOME/.zshrc`-Datei integriert. Die relevanten Ausschnitte aus meiner `.zshrc`-Datei:

```shell
# Pfad zu Ihrer oh-my-zsh-Installation.
export ZSH="/Users/tgartner/.oh-my-zsh"

# Name des zu ladenden Themes festlegen.
# Siehe https://github.com/robbyrussell/oh-my-zsh/wiki/Themes
ZSH_THEME="powerlevel9k/powerlevel9k"

(...)

# Welche Plugins möchten Sie laden?
# Standard-Plugins finden Sie in ~/.oh-my-zsh/plugins/*
# Benutzerdefinierte Plugins können zu ~/.oh-my-zsh/custom/plugins/ hinzugefügt werden
# Beispiel-Format: plugins=(rails git textmate ruby lighthouse)
# Wählen Sie mit Bedacht, da zu viele Plugins den Shell-Start verlangsamen.
plugins=(git python)
```

## powerlevel10k

Hinweis: Ich habe früher [powerlevel9k](https://github.com/Powerlevel9k/powerlevel9k) verwendet, aber als ich meinen Mac im Mai 2025 installierte, war 9k veraltet und verwies auf [powerlevel10k](https://github.com/romkatv/powerlevel10k).

Installieren Sie powerlevel10k gemäß ihrer [Installationsanleitung für zsh](https://github.com/romkatv/powerlevel10k?tab=readme-ov-file#oh-my-zsh).