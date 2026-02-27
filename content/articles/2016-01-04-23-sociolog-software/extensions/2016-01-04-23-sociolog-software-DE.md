---
date: 2016-01-04
image: sociolog.png
excerpt: Ein Werkzeug, das meine Aktivitäten über alle sozialen Medienplattformen hinweg verfolgt.
title: sociolog - Ihre Spur durch soziale Medien
tags: softwareWeNeed
translation: de
source_language: en
source_hash: f74871d79814bc59a5b1c7171885bb67981c6fe570d92726c6e2abfd92f059f1
translator: gpt-4o-2024-08-06
translate_date: 2026-02-27T10:02:17.722402+00:00
generated_by: simplified-translation-system
---

Ich schreibe oder blogge in verschiedenen Medien:

- Twitter
- Facebook
- Ein privater Blog mit eingeschränktem Zugang (weil er Familienfotos enthält)
- Dieser [Blog](http://tillgartner.com)

Von Zeit zu Zeit finde ich es schön, durch meine Vergangenheit zu scrollen. Das mache ich am häufigsten in unserem Familienblog, weil er den interessantesten Inhalt enthält und weil es einfach ist, durchzuscrollen. Ich möchte in der Lage sein, durch meine gesamte Vergangenheit in allen Medien zu scrollen.

Das sollte meine Software tun:

- Alle Einträge sammeln, die ich in den sozialen Medien geschrieben habe:
  - Twitter
  - Facebook
  - Wordpress
- Ein Dokument pro Eintrag in einem Github-Repo erstellen
- Doppelte Inhalte richtig behandeln: Seit einigen Jahren ist mein Twitter-Konto mit meinem Facebook-Konto _verknüpft_, sodass Twitter-Einträge auf Facebook repliziert werden. Das liegt daran, dass ich in beiden Medien Menschen habe, die ich als _Publikum_ betrachte.
- Auch das Feedback zu meinen Beiträgen sammeln
- Diese auf statische Weise schön anzeigen, einschließlich Übersichtsseiten

Einige technische Überlegungen:

- Ich würde es in Java schreiben, weil ich das am besten kann
- Wäre ein Headless-Programm, d.h. keine Benutzeroberfläche
- Eingabe sollte das Datum des letzten aufgezeichneten Social-Media-Eintrags sein
- Es sammelt alle Einträge (einschließlich der Kommentare dazu) auf den verschiedenen Social-Media-Kanälen seit diesem Datum
- Es entfernt Duplikate (d.h. es vereint die, die gleich sind oder Replikate voneinander auf verschiedenen Kanälen sind)
- Es erstellt ein Dokument / Datei pro Social-Media-Eintrag und schreibt sie in ein Ausgabeverzeichnis
- Dieses Verzeichnis wird dann in ein Github-Konto repliziert / hinzugefügt
- Social-Media-Eintragsdokumente würden benannt wie `2015-12-03-Der_Titel_von_was_ich_geschrieben_habe-TWITTER.json`
- Es gäbe eine _Header-Datei_ mit einem festen Namen, d.h. `sociologs.json`. Diese Datei würde die ersten 20 Logs enthalten und auf eine Datei mit den nächsten Logs verweisen.
- Die Domain `sociolog.io` wäre [verfügbar](https://www.godaddy.com/domains/searchresults.aspx?&checkAvail=1&domainToCheck=sociolog.io) - Stand heute, 4. Januar 2016.
- Das generierte `index.html` würde die Daten über JS/AJAX-Anfragen laden und beim Scrollen des Benutzers weiterladen

Wenn jemand interessiert ist oder Anmerkungen hat, bitte kontaktieren Sie mich unter till`dot`gartner`at`gmail`dot`com.