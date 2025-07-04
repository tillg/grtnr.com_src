---
title: Autocomplete für meinen Blog
tags: blog, tech, softwareweneed
summary: Ich habe jetzt einen auf Pelican basierten Blog und möchte automatisch Inhalte hinzufügen oder korrigieren: Bildtags, Artikelzusammenfassungen, Übersetzungen... Endlich eine Möglichkeit, KI 🤖 zu nutzen
Translation: de
Source-Language: en
Translator: gpt-4o
Translate-Date: 2025-07-04T16:42:01.956446
Source-File: /Users/tgartner/git/grtnr.com_src/content/articles/2025-05-04-autocompleting-my-blog/2025-05-04-autocompleting-my-blog.md
Generated-By: automatic-translation-plugin
---

[TOC]

Seit letzter Woche basiert mein Blog auf [Pelican](https://getpelican.com), dem Python-basierten statischen Blog-Generator. Jetzt, da der Blog in einer Sprache erstellt wird, die ich mehr oder weniger beherrsche, kann ich darüber nachdenken, den Prozess des Schreibens und Erstellens selbst zu verbessern. Und natürlich gibt es viele Werkzeuge, die ich mir vorstellen kann, um mein Leben und das Leben meiner Leser zu erleichtern. Hier sind einige Beispiele für diese Helfer.

## Werkzeuge, die ich gerne hätte

### Bildtag-Autovervollständigung (KI)

Immer wenn ich ein Bild ohne Alt-Text hinzufüge, ist das schlecht für blinde Menschen. Aber ich bin faul, also warum nicht eine KI das Bild beschreiben lassen und es als ALT-Text hinzufügen?

### Link-Checker

Ich habe viele Links, die auf externe Standorte verweisen. Und manchmal verschwinden Webseiten, so dass meine Links ins Nirwana führen könnten. Es wäre schön, wenn

- mein Benutzer nicht auf defekte Links klicken müsste
- ich einen Hinweis bekäme, dass ich den einen oder anderen Link reparieren muss
- ich die Situation vielleicht verhindern könnte, indem ich eine Kopie der Seite, auf die ich in meinem eigenen Blog verlinke, aufbewahre. Oder ist das böses Scraping und Content-Diebstahl?

### Auszugsgenerator (KI)

Ich schreibe oft Artikel, ohne die Zusammenfassung / den Auszug anzugeben, der in der Artikelliste angezeigt wird. Standardmäßig nehmen Pelican (und andere statische Generatoren) den ersten Absatz oder die ersten 30 Wörter und verwenden sie als Auszug.

Wäre es nicht viel schöner, ein LLM zu bitten, eine vernünftige Zusammenfassung von 3 Zeilen zu generieren?

### Übersetzer (KI-ähnlich)

In meinem Blog schreibe ich manchmal englische, manchmal deutsche Artikel. Vielleicht gibt es hier und da sogar einen französischen Artikel. Wäre es nicht schön, jeden Artikel in jeder Sprache zu haben? Es fühlt sich so an, als ob das heutzutage ein Standard sein sollte, angesichts der guten Qualität der heutigen Übersetzungswerkzeuge.

Also schreibe ich meine Artikel in der Sprache, die mir gerade in den Sinn kommt, und das System sollte die fehlenden Sprachen generieren.

### Artikelillustration (KI)

Ich versuche, für die meisten meiner Artikel Bilder zu haben, da es einfach ein schöneres Leseerlebnis ist und angenehm für das Auge. Ich finde oft etwas im Internet, aber nicht immer - auch weil ich manchmal nicht einmal die Mühe mache, ein Bild zu suchen. Aber die KI könnte suchen oder sogar ein schönes Bild für meine _nackten_ Artikel generieren.

## Wir brauchen eine Build-Pipeline

Um diese Dinge zu bauen, habe ich das Gefühl, dass ich so etwas wie eine _Build-Pipeline_ brauche:

![Build-Pipeline](https://insights.mgm-tp.com/wp-content/uploads/2023/08/mgm-CI-CD-Pipeline.png)
_Eine moderne CI/CD-Build-Pipeline, entnommen von [mgm technology partners](https://mgm-tp.com)_

Einige Gedanken zur Struktur, zur Verarbeitung und zur Organisation von Daten.

### Zwischendaten

Was Pelican macht, ist, die Quelle der Artikel zusammen mit der Konfiguration zu nehmen und die Webseiten zu generieren. Dies geschieht durch seine Standardverarbeitung und durch potenzielle Plugins. Plugins können von Dritten oder selbst entwickelt sein. In meinem Fall habe ich beides.

Viele der Werkzeuge, die ich mir vorstelle, erzeugen zusätzliche Daten, und oft ist die Erstellung aufwendig und zeitaufwändig. Denken Sie an das Erstellen eines Auszugs aus einem Artikel: Der gesamte Text muss an eine KI gesendet und verarbeitet werden. Dies dauert mehrere Sekunden und kostet echtes Geld. Daher ist es sicherlich nicht etwas, das wir bei jedem Build ausführen wollen. Daher müssen wir die Daten zwischen den verschiedenen Build-Läufen aufbewahren.

### Integrität des verfassten Inhalts

Eine Möglichkeit, dies zu lösen, könnte darin bestehen, den von der KI generierten Auszug einfach zum ursprünglichen Markdown hinzuzufügen (in diesem Fall würde er im Front Matter als `summary` Feld gehen).

Aber das gefällt mir überhaupt nicht: Ich möchte nicht, dass die KI in dem Text und Inhalt herumpfuscht, den ich persönlich erstellt habe. Daher möchte ich die folgende Regel für mein System festlegen:

**Meine von mir verfassten Markdown-Dateien sollten niemals von automatisierten Werkzeugen modifiziert werden.**

### Wo Daten aufbewahren

Das lässt mich mit der Frage zurück, wo ich die Daten wie von KI generierte Zusammenfassungen aufbewahren soll. Der natürliche Ort ist, sie neben den Markdown-Dateien aufzubewahren, aber in einer eigenen Datei. Da ich separate Verzeichnisse für jeden meiner Artikel habe, komme ich zu dieser Form von Verzeichnissen und Dateien:

```file
content
    articles
    ...
    2025-04-18-digital-garden
        2025-04-18-ditigal-garden.md
        2025-04-18-digital-garden.picture-tags.json
        2025-04-18-digital-garden.summary.json
        digital-garden.jpg
```

Einige Gedanken und Argumente für diese Struktur:

- Jedes Werkzeug hat seine eigene Datei, um die Dinge getrennt zu halten.
- Ich verwende JSON-Dateien: Einfach zu verarbeiten und einfach zu lesen.
- Die Dateien liegen neben dem Originalartikel, so dass alles, was dazu gehört, in der Nähe und _eingekapselt_ ist.
- Die JSON-Dateien sind auch versionskontrolliert und in Git gespeichert, so dass ich den Build-Prozess auf meiner lokalen Entwicklungs-Maschine oder in Github Actions oder einem anderen CI/CD-Prozessor ausführe, verwendet es die zuvor generierten Daten.

### Verarbeitungsreihenfolge

Dieses Datenlayout erfordert einen mehrstufigen Build-Prozess:

1. **Zusätzliche Daten erstellen:** Die Zusammenfassungen generieren, die Bildbeschreibungen, die Bilder, die Links überprüfen (und das Ergebnis dieser Überprüfungen speichern)... Dieser Prozess ist potenziell zeitaufwändig, erzeugt viele zusätzliche Daten und erfordert intelligente Caching- und Cache-Validierungsmechanismen. D.h. "Wie überprüfe ich, ob ich die Zusammenfassung eines Artikels neu erstellen muss oder ob ich die in der JSON-Datei neben dem Markdown-Artikel verwenden kann?".
2. **Die Seite erstellen:** Dies ist der grundlegende Pelican-Erstellungsprozess, wie wir ihn kennen, mit der Ausnahme, dass er auch die zusätzlichen Daten, die jetzt in den JSON-Dateien sind, _integrieren_ muss. Ich werde dies mit einem oder mehreren Pelican-Plugins tun, die ich entwickeln werde.