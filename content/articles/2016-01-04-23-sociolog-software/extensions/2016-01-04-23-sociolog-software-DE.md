---
date: 2016-01-04
image: sociolog.png
excerpt: Ein Tool, das meine Aktivitäten über alle sozialen Medien hinweg verfolgt.
title: sociolog - Deine Spur durch soziale Medien
tags: softwareWeNeed
translation: de
source_language: en
source_hash: 291788f451d1eefc57c2d76be723c7185ab6c61f7d8d802bc1bd6cb08e182664
translator: gpt-4o-2024-08-06
translate_date: 2026-02-28T14:26:05.801379+00:00
generated_by: simplified-translation-system
---

Ich schreibe oder blogge in verschiedenen Medien:

- Twitter
- Facebook
- Ein privater Blog mit eingeschränktem Zugang (weil er Familienfotos enthält)
- Dieser [Blog](http://tillgartner.com) [Seite existiert nicht mehr]

Hin und wieder finde ich es schön, durch meine Vergangenheit zu scrollen. Am häufigsten mache ich das in unserem Familienblog, weil er den interessantesten Inhalt hat und weil es einfach ist, durchzuscrollen. Ich würde gerne durch meine gesamte Vergangenheit in allen Medien scrollen können.

Das sollte meine Software tun:

- Alle Einträge sammeln, die ich in den sozialen Medien geschrieben habe:
  - Twitter
  - Facebook
  - Wordpress
- Ein Dokument pro Eintrag in einem Github-Repo erstellen
- Doppelte Inhalte ordnungsgemäß behandeln: Seit einigen Jahren ist mein Twitter-Account mit meinem Facebook-Account _verknüpft_, sodass Twitter-Einträge auf Facebook repliziert werden. Das liegt daran, dass ich in beiden Medien Leute habe, die ich als _Publikum_ betrachte.
- Auch das Feedback zu meinen Posts sammeln
- Sie ansprechend statisch anzeigen, inklusive Übersichtsseiten

Einige technische Überlegungen:

- Ich würde es in Java schreiben, weil ich das am besten kann
- Wäre ein Headless-Programm, d.h. keine UI
- Eingabe sollte das Datum des letzten aufgezeichneten Social-Media-Eintrags sein
- Es sammelt alle Einträge (einschließlich der Kommentare dazu) auf den verschiedenen Social-Media-Kanälen seit diesem Datum
- Es entfernt Duplikate (d.h. es vereint die, die gleich sind oder Replikate voneinander auf verschiedenen Kanälen)
- Es erstellt ein Dokument / Datei pro Social-Media-Eintrag und schreibt sie in ein Ausgabeverzeichnis
- Dieses Verzeichnis wird dann in einem Github-Account repliziert / hinzugefügt
- Social-Media-Eintragsdokumente würden benannt wie `2015-12-03-Der_Titel_von_was_ich_geschrieben_habe-TWITTER.json`
- Es gäbe eine _Header-Datei_ mit einem festen Namen, z.B. `sociologs.json`. Diese Datei würde die ersten 20 Logs enthalten und auf eine Datei mit den nächsten Logs verweisen.
- Die Domain `sociolog.io` wäre [verfügbar](https://www.godaddy.com/domains/searchresults.aspx?&checkAvail=1&domainToCheck=sociolog.io) - Stand heute, 4. Jan 2016.
- Das generierte `index.html` würde die Daten über JS/AJAX-Anfragen laden und beim Herunterscrollen des Nutzers weiterladen

Wenn jemand interessiert ist oder Kommentare hat, bitte melde dich bei till`dot`gartner`at`gmail`dot`com.