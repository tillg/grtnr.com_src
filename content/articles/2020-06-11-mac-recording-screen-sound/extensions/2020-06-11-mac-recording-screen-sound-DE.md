---
date: 2020-06-11
image: MacSoundFlower.png
excerpt: Wie du deinen Mac-Bildschirm zusammen mit dem Systemton mit Soundflower und QuickTime Player aufnimmst.
title: Mac: Bildschirm & Ton aufnehmen
translation: de
source_language: en
source_hash: bcc4d96f6e1758f39feebd99e7a7c3ae49209e922b6925af0eff06fe14ea80c0
translator: gpt-4o-2024-08-06
translate_date: 2026-02-28T09:26:48.844481+00:00
generated_by: simplified-translation-system
---

**Kurzfassung** Um den Bildschirm deines Macs zusammen mit dem Ton (z.B. eine Zoom-Sitzung) aufzunehmen, kannst du Soundflower verwenden.

Hier ist, was ich erreichen wollte: Eine (Video-)Aufnahme dessen, was auf dem Bildschirm meines Macs passiert, **einschließlich des Tons**. Und das alles, während ich gleichzeitig hören kann, was passiert. In meinem Fall wollte ich eine Zoom-Klasse aufnehmen, aber ich denke, diese Einrichtung könnte in vielen Situationen nützlich sein.

macOS kommt mit einem großartigen eingebauten Bildschirmaufnahme-Tool: [QuickTime Player](https://support.apple.com/en-us/HT208721) (ja, es nimmt auf, auch wenn der Name _Player_ sagt 😀).

Das einzige Problem bei der Verwendung von QuickTime Player ist der Ton: Die Auswahlmöglichkeiten sind _Internes Mikrofon_ oder _Keiner_. Das passt gut, wenn du ein Tutorial aufnehmen möchtest, bei dem der Ton das ist, was du über das Mikrofon erklärst, aber es passt nicht zu meiner Situation.

Hier kommt [SoundFlower](https://github.com/mattingalls/Soundflower) ins Spiel. Es ist Open Source, ausgereift und zuverlässig (getestet von mir und weit erfahreneren Kollegen - und hat immer sehr gute Bewertungen erhalten). SoundFlower ist, wie es heute ist (das ist Sommer 2020), kein Programm mit einer Benutzeroberfläche, sondern nur eine macOS-Systemerweiterung. Das ist etwas, das du als Benutzer nicht siehst, aber das im Hintergrund sehr hilfreich ist.

Was es in unserem Fall macht: Es erstellt einen neuen, virtuellen Tonkanal, der den Tonstrom in 2 andere Ströme aufteilt. In meinem Fall bedeutet das, dass ich in meiner Zoom-Sitzung einen virtuellen Ausgang anstelle des Lautsprechers meines Macs auswähle. Ich nannte diesen Ausgang _MacSpkr_SndFlwr_. Und dieser virtuelle Strom teilt den Ausgang auf den Lautsprecher des Macs und den (logischen) SoundFlower-Kanal auf. Dann wähle ich den SoundFlower-Kanal als Eingang für meine QuickTime Player-Aufnahme aus und das war's.

![Flow](MacSoundFlower.svg)Die Tonströme

## Alles einrichten

**Soundflower installieren** ist gut auf der [Download-Seite auf Github](https://github.com/mattingalls/Soundflower/releases/tag/2.0b2) beschrieben. Der Prozess mag etwas umständlich erscheinen, funktioniert aber gut, wenn du ihn Schritt für Schritt befolgst. Beachte, dass es eine Weile gedauert hat, bis ich herausgefunden habe, was sie mit "_Sobald du dort bist, sollte es einen "Erlauben"-Button (\*\*) geben, den du anklicken musst, um die Erlaubnis zur Nutzung von Soundflower (Entwickler: MATT INGALLS) zu geben._" meinten. Ich erwartete ein Popup-Dialogfeld mit dem Erlauben-Button, aber es ist einfach ein Button im Fenster.

Beachte auch, dass du deinen Mac nach der Installation von Soundflower neu starten musst.

Sobald du Soundflower installiert hast, kannst du ein logisches Audiogerät erstellen, das den Tonstrom aufteilt. Öffne dazu _Audio-MIDI-Setup_. Es ist ein macOS-Dienstprogramm, das sich in /Programme/Dienstprogramme befindet. Du kannst es auch über Spotlight starten (drücke Cmd + Leertaste) und gib "_Audio Midi_" ein.

![Midi app launch](Screenshot-2020-06-11-at-11.47.25.png)

_Audio-MIDI-Setup über Spotlight starten_

Sobald du im Audio-MIDI-Setup-Programm bist, erstelle ein neues (logisches) Audiogerät: Klicke auf den "**+**"-Button in der unteren linken Ecke und wähle "_Multi-Output-Gerät erstellen_". Wähle im rechten Bereich, der erscheint, "_MacBook-Lautsprecher_" UND "_Soundflower (2ch)_" aus.

![Settings](Screenshot-2020-06-11-at-11.14.46.png)

_Das neu erstellte Multi-Output-Gerät_

Starte dann deinen QuickTime Player (dieser ist auf deinem Mac vorinstalliert) und erstelle eine neue Bildschirmaufnahme: Menü _Ablage ➡ Neue Bildschirmaufnahme_. Im unteren Teil des Bildschirms erscheint ein schwebendes Menü:

![Entire screen](macos-catalina-screenshot-menu-record.jpg)

_Das schwebende Menü bei der Aufnahme mit QuickTime Player_

Öffne die Optionsliste und wähle "Soundflower (2ch)" als Eingang für die Aufnahme. Klicke auf "Aufnehmen" und los geht's: Starte jetzt deine Zoom-Sitzung, maximiere das Fenster und deine gesamte Zoom-Sitzung wird in einer .mov-Datei aufgenommen.

Ich hoffe, diese Anleitungen waren hilfreich; zögere nicht, Fragen zu stellen, wenn du welche hast.

### Referenzen

- _Wie man den Bildschirm auf deinem Mac aufnimmt_ von [Apple Support](https://support.apple.com/en-us/HT208721)
- [Soundflower-Erklärungen](https://github.com/mattingalls/Soundflower/releases/tag/2.0b2)
- _Nimm den Bildschirm deines Computers mit Ton auf einem Mac auf_ von [c|net](https://www.cnet.com/how-to/record-your-computers-screen-with-audio-on-a-mac/)