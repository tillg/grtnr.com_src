---
date: 2015-11-30
image: github.png
excerpt: Wie ich meinen Blog mit JBake als statischem Site-Generator und GitHub Pages für das Hosting eingerichtet habe.
title: Wie ich zu GitHub & JBake gewechselt bin
tags: tech, webSite
translation: de
source_language: en
source_hash: 390e4b560ef27f0c86fd9724582e98d9a83910759c6d7fd671eb722749d2bc0d
translator: gpt-4o-2024-08-06
translate_date: 2026-02-27T10:00:21.961238+00:00
generated_by: simplified-translation-system
---

**\*** Diese Seite ist ~~im Aufbau~~ unvollständig... **\***

Zuerst: Es ist nicht meine Erfindung! Viele haben es schon vorher gemacht, es gibt viele Beschreibungen da draußen. Es hat trotzdem einige Zeit gedauert ;)

[Diese](http://alexcican.com/post/guide-hosting-website-dropbox-github/) und [diese](http://alexcican.com/post/blog-dropbox-scriptogram) waren die inspirierendsten Quellen und die einfachste Erklärung (die Vertrauen gibt ;) ).

# Einrichtung

So sieht mein Gesamteinrichtung aus:

- Ein Verzeichnis auf meinem Mac, das den Inhalt enthält. Ich verwende die Grundstruktur, die [Jbake](http://jbake.org) nutzt.
- Ein git-geklontes Verzeichnis auf meinem Mac mit dem Output des jBake-Prozesses
- Ein kleines Skript, das ich jedes Mal ausführe, wenn ich etwas geändert habe. Das Skript erledigt das "Baking" und das "Git-Publishing"
- Und natürlich die Einstellungen im DNS, um meinen Domainnamen auf die Github-IPs zu verweisen

## JBake

Warum benutze ich JBake? Mir gefällt das Prinzip und ich fühle mich in Java wohler als in anderen Programmiersprachen. Ich habe den internen Code von JBake nicht angerührt, aber ich bin zuversichtlich, dass ich es könnte.
Die Funktionsweise von JBake ähnelt dem berühmten [Jekyll](https://jekyllrb.com/): Es analysiert Inhaltsdateien und erstellt daraus (statische) HTML-Dateien. Die Inhaltsdateien können Markdown oder andere Formate enthalten; ich verwende einfach Markdown.

Meine Verzeichnisstruktur sieht so aus:

```text
.
|-- assets
|   |-- favicon.gif
|   |-- robots.txt
|   |-- img
|   |   |-- logo.png
|   |-- js
|   |   |-- custom.js
|   |-- css
|       |-- style.css
|
|-- content
|   |-- about.html
|   |-- 2013
|       |-- 01
|       |   |-- hello-world.html
|       |-- 02
|           |-- weekly-links-1.ad
|           |-- weekly-links-2.md
|
|-- templates
|   |-- index.ftl
|   |-- page.ftl
|   |-- post.ftl
|   |-- feed.ftl
|
|-- jbake.properties
```

Standardmäßig erzeugt JBake das Ausgabeverzeichnis in diesem Baum. In meinem Fall backe ich meine Sachen in ein Verzeichnis, das git-synchronisiert ist.

## Die GitHub-Einrichtung

## Die DNS-Einstellungen

# Als Nächstes

Es gibt ein paar Dinge, die ich ändern möchte.