---
title: Einrichten meines Terminals
tags: tech, Mac
image: terminal.png
translation: de
source_language: en
source_hash: d4e2f6c72df431d523448eec775c1c31c8e93ef1de0bbf69636297aa134ba4fc
translator: gpt-4o-2024-08-06
translate_date: 2025-07-18T22:26:47.006374
generated_by: simplified-translation-system
---

Ich weiß, es gibt viele Artikel und Erklärungen darüber, wie man sein Terminal konfiguriert und einrichtet. Trotzdem hat es mich mehr als 2 Stunden gekostet, alles so zum Laufen zu bringen, wie ich es wollte. Der Grund war, dass viele der Artikel und Erklärungen eine Schritt-für-Schritt-Anleitung zur Installation bieten, aber zu wenig Hintergrundinformationen darüber, wie die Dinge im Hintergrund zusammenhängen und funktionieren. Und genau das hat mir gefehlt...

Hier ist also ein weiterer Artikel. Oder eher eine Sammlung von Informationsschnipseln, die ich als wertvoll empfand.

## Die Ausgangssituation

Meine Zielkonfiguration und Anforderungen sind einfach:

- macOS (Catalina 10.15.2 zum Zeitpunkt des Schreibens)
- iTerm2 (Build 3.3.8)
- zsh (wie von Apple seit einigen macOS-Versionen bereitgestellt)
- Ich möchte eine ordentliche Farbgebung
- Ich möchte sehen, in welchem Git-Branch ich mich befinde - wenn das aktuelle Verzeichnis innerhalb eines Git-Repos liegt

## Die beweglichen Teile

Was mich verwirrt hat, war der fehlende Überblick. Daher sind hier die verschiedenen Bestandteile, die an meiner Konfiguration beteiligt sind:

- **zsh**: Die Shell
- **Oh My Zsh**: Ein Framework, das die zsh-Shell mit Funktionen und Design erweitert.
- **powerlevel9k**: Ein Theme für Oh My Zsh
- **Schriftarten**, die von powerlevel9k benötigt werden, um Text und Symbole anzuzeigen

Die Abhängigkeiten in dieser Liste sind von oben nach unten, d.h. die Schriftarten werden von powerlevel9k benötigt, das auf Oh My Zsh läuft, welches zsh verwendet.

## Verzeichnisstruktur

Bevor wir die verschiedenen Komponenten einzeln durchgehen, hier die Verzeichnisstruktur, die wir nach der Installation aller Bestandteile haben werden:

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

Früher habe ich bash verwendet und war damit zufrieden. Ich startete einfach mein Mac-Terminal, und da war es. Später nutzte ich iTerm2, und es startete ebenfalls mit bash. Warum also zu zsh wechseln?

Dieser Artikel erklärt es schön und ausführlich. Kurz gesagt:

- Apple verwendete früher bash, da es der De-facto-Standard war
- 2007 wechselte bash zur [GNU Public License 3.0](https://www.gnu.org/licenses/gpl-3.0.en.html), was Apple aus bestimmten Gründen nicht gefiel. Daher blieben sie bei der Vor-2007-Version von bash. Und das ist alt - einschließlich [einer Sicherheitslücke](<https://www.wikiwand.com/en/Shellshock_(software_bug)>), die Apple zwang, bash für Macs zu aktualisieren.
- zsh wurde im Laufe der Zeit zum aufkommenden De-facto-Standard, also wechselte Apple.

Und natürlich bietet [zsh modernere, coole Funktionen](https://www.howtogeek.com/362409/what-is-zsh-and-why-should-you-use-it-instead-of-bash/).

Also, es ist der neue Standard, es sieht gut aus - nutzen wir es. Da es die neue Mac-Standardshell ist, müssen Sie es nicht installieren. Falls Sie einen neuen Mac haben, der mit Catalina vorinstalliert kam, verwenden Sie bereits zsh. Falls Sie Ihren Mac von Mojave aktualisiert haben, müssen Sie zsh als Ihre Terminal-Shell wie folgt festlegen:

```shell
chsh -s /bin/zsh
```

Dies setzt zsh als die Standard-Shell.

### Konfiguration

Die Konfiguration der zsh-Shell erfolgt über Einträge in `.zshrc`, die sich in Ihrem `$HOME`-Verzeichnis befindet. Wie oben beschrieben, gibt es einige Komponenten, die interagieren. Einige von ihnen bieten Konfigurationsoptionen und können an verschiedenen Orten konfiguriert werden. Um den Überblick zu behalten, habe ich mich entschieden, die Komponenten an ihrem jeweiligen Standardort zu installieren und alle Konfigurationsoptionen in der `.zshrc`-Datei zu haben.

## Oh My Zsh

> Oh My Zsh ist ein Open-Source-, Community-getriebenes Framework zur Verwaltung Ihrer zsh-Konfiguration.
> -- <cite>[Oh My Zsh Webseite](https://ohmyz.sh/)</cite>

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

Wie erwähnt, habe ich alle Konfigurationen in meiner `$HOME/.zshrc`-Datei integriert. Die relevanten Ausschnitte aus meiner `.zshrc`-Datei:

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