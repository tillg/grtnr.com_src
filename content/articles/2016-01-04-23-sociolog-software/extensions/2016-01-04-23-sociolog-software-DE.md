---
Translation: de
Source-Language: en
Translator: gpt-4o
Translate-Date: 2025-07-04T17:02:45.345455
Source-File: /Users/tgartner/git/grtnr.com_src/content/articles/2016-01-04-23-sociolog-software/2016-01-04-23-sociolog-software.md
Generated-By: automatic-translation-plugin
---

```markdown
---
title: sociolog - Ihr Pfad durch soziale Medien
tags: softwareWeNeed
layout: post
date: 2016-01-04
image: sociolog.png
excerpt: Ein Tool, das meine Aktivitäten auf allen sozialen Medienplattformen verfolgt.
---

Ich schreibe oder blogge in verschiedenen Medien:

- Twitter
- Facebook
- Ein privater Blog mit eingeschränktem Zugang (weil er Familienfotos enthält)
- Dieser [Blog](http://tillgartner.com)

Von Zeit zu Zeit finde ich es schön, durch meine Vergangenheit zu scrollen. Am häufigsten mache ich das in unserem Familienblog, weil er die interessantesten Inhalte enthält und weil es einfach ist, durchzuscrollen. Ich möchte in der Lage sein, durch meine gesamte Vergangenheit in allen Medien zu scrollen.

Das sollte meine Software also tun:

- Alle Einträge sammeln, die ich in den sozialen Medien geschrieben habe:
  - Twitter
  - Facebook
  - Wordpress
- Ein Dokument pro Eintrag in einem Github-Repo erstellen
- Doppelte Inhalte ordnungsgemäß behandeln: Seit einigen Jahren ist mein Twitter-Konto mit meinem Facebook-Konto _verbunden_, sodass Twitter-Einträge auf Facebook repliziert werden. Das liegt daran, dass ich Menschen habe, die ich in beiden Medien als _Publikum_ betrachte.
- Auch das Feedback zu meinen Beiträgen sammeln
- Diese auf ansprechende Weise statisch darstellen, einschließlich Übersichtsseiten

Einige technische Überlegungen:

- Ich würde es in Java schreiben, da ich das am besten kenne
- Wäre ein Headless-Programm, d.h. keine Benutzeroberfläche
- Der Input sollte das Datum des letzten aufgezeichneten Social-Media-Eintrags sein
- Es sammelt alle Einträge (einschließlich der Kommentare dazu) auf den verschiedenen Social-Media-Kanälen seit diesem Datum
- Es entfernt Duplikate (d.h. es werden die gleichen oder replizierten Einträge auf verschiedenen Kanälen zusammengeführt)
- Es erstellt ein Dokument / eine Datei pro Social-Media-Eintrag und schreibt sie in ein Ausgabeverzeichnis
- Dieses Verzeichnis wird dann in ein Github-Konto repliziert / hinzugefügt
- Social-Media-Eintragsdokumente würden wie `2015-12-03-Der_Titel_von_was_ich_geschrieben_habe-TWITTER.json` benannt
- Es gäbe eine _Header-Datei_ mit einem festen Namen, z.B. `sociologs.json`. Diese Datei würde die ersten 20 Logs enthalten und auf eine Datei mit den nächsten Logs verweisen.
- Die Domain `sociolog.io` wäre [verfügbar](https://www.godaddy.com/domains/searchresults.aspx?&checkAvail=1&domainToCheck=sociolog.io) - Stand heute, 4. Januar 2016.
- Das generierte `index.html` würde die Daten über JS/AJAX-Anfragen laden und beim Herunterscrollen des Benutzers weiterladen

Wenn jemand interessiert ist oder Anmerkungen hat, bitte kontaktieren Sie mich unter till`dot`gartner`at`gmail`dot`com.
```