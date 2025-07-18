---
layout: post
title: Mac: Bildschirm und Ton aufnehmen
slug: mac-recording-screen-sound
date_published: 2020-06-11T10:06:49.000Z
date_updated: 2020-06-11T17:50:04.000Z
tags: 
image: MacSoundFlower.png
translation: de
source_language: en
source_hash: a8becfef1440ee734baf4f19ba0ab9f266e0d5e3fc946e311bf73b7ec37f27e4
translator: gpt-4o-2024-08-06
translate_date: 2025-07-18T22:56:56.066162
generated_by: simplified-translation-system
---

**Zusammenfassung** Um den Bildschirm Ihres Macs zusammen mit dem Ton (z.B. eine Zoom-Sitzung) aufzunehmen, können Sie Soundflower verwenden.

Hier ist, was ich erreichen wollte: Eine (Video-)Aufnahme dessen, was auf dem Bildschirm meines Macs passiert, **einschließlich des Tons**. All das, während ich gleichzeitig hören kann, was passiert. In meinem Fall wollte ich eine Zoom-Klasse aufnehmen, aber ich denke, diese Einrichtung könnte in vielen Situationen nützlich sein.

macOS kommt mit einem großartigen integrierten Bildschirmaufnahme-Tool: [QuickTime Player](https://support.apple.com/en-us/HT208721) (ja, es nimmt auf, auch wenn der Name _Player_ sagt 😀).

Das einzige Problem bei der Verwendung von QuickTime Player ist der Ton: Die Auswahlmöglichkeiten sind _Internes Mikrofon_ oder _Kein_. Das passt gut, wenn Sie ein Tutorial aufnehmen möchten, bei dem der Ton das ist, was Sie über das Mikrofon erklären, aber es passt nicht zu meiner Situation.

Hier kommt [SoundFlower](https://github.com/mattingalls/Soundflower) ins Spiel. Es ist Open Source, ausgereift und zuverlässig (getestet von mir und weit erfahreneren Kollegen - und hat immer sehr gute Bewertungen erhalten). SoundFlower ist, wie es heute ist (das ist Sommer 2020), kein Programm mit einer Benutzeroberfläche, sondern nur eine macOS-Systemerweiterung. Das ist etwas, das Sie als Benutzer nicht sehen, aber das im Hintergrund sehr hilfreich ist.

Was es in unserem Fall tut: Es erstellt einen neuen, virtuellen Tonkanal, der den Tonstrom in 2 andere Ströme aufteilt. In meinem Fall bedeutet das, dass ich in meiner Zoom-Sitzung einen virtuellen Ausgang anstelle des Lautsprechers meines Macs auswähle. Ich nannte diesen Ausgang _MacSpkr_SndFlwr_. Und dieser virtuelle Strom teilt den Ausgang auf den Lautsprecher des Macs und den (logischen) SoundFlower-Kanal auf. Dann wähle ich den SoundFlower-Kanal als Eingang für meine QuickTime Player-Aufnahme aus und das war's.

![Fluss](MacSoundFlower.svg)Die Tonströme

## Einrichtung

**Soundflower installieren** ist gut auf der [Download-Seite auf Github](https://github.com/mattingalls/Soundflower/releases/tag/2.0b2) beschrieben. Der Prozess mag etwas umständlich erscheinen, funktioniert jedoch gut, wenn Sie ihn Schritt für Schritt befolgen. Beachten Sie, dass es eine Weile gedauert hat, bis ich herausgefunden habe, was sie mit "_Sobald Sie dort sind, sollte es eine Schaltfläche 'Zulassen' (\*\*) geben, die Sie anklicken müssen, um die Erlaubnis zur Nutzung von Soundflower (Entwickler: MATT INGALLS) zu erteilen._" Ich erwartete einen Popup-Dialog mit der Zulassen-Schaltfläche, aber es ist einfach eine Schaltfläche innerhalb des Fensters.

Beachten Sie auch, dass Sie Ihren Mac nach der Installation von Soundflower neu starten müssen.

Sobald Sie Soundflower installiert haben, können Sie ein logisches Audiogerät erstellen, das den Tonstrom aufteilt. Öffnen Sie dazu _Audio-MIDI-Setup_. Es ist ein macOS-Dienstprogramm, das sich in /Programme/Dienstprogramme befindet. Sie können es auch über Spotlight starten (drücken Sie Cmd + Leertaste) und geben Sie "_Audio Midi_" ein.

![Midi-App-Start](Screenshot-2020-06-11-at-11.47.25.png)

_Starten des Audio-MIDI-Setups über Spotlight_

Sobald Sie sich im Audio-MIDI-Setup-Programm befinden, erstellen Sie ein neues (logisches) Audiogerät: Klicken Sie auf die "**+**"-Schaltfläche in der unteren linken Ecke und wählen Sie "_Multi-Output-Gerät erstellen_". Wählen Sie im rechten Bereich "_MacBook-Lautsprecher_" UND "_Soundflower (2ch)_" aus.

![Einstellungen](Screenshot-2020-06-11-at-11.14.46.png)

_Das neu erstellte Multi-Output-Gerät_

Starten Sie dann Ihren QuickTime Player (dieser ist auf Ihrem Mac vorinstalliert) und erstellen Sie eine neue Bildschirmaufnahme: Menü _Ablage ➡ Neue Bildschirmaufnahme_. Im unteren Teil des Bildschirms erscheint ein schwebendes Menü:

![Gesamter Bildschirm](macos-catalina-screenshot-menu-record.jpg)

_Das schwebende Menü bei der Aufnahme mit QuickTime Player_

Öffnen Sie die Optionsliste und wählen Sie "Soundflower (2ch)" als Eingang für die Aufnahme. Klicken Sie auf "Aufnehmen" und los geht's: Starten Sie jetzt Ihre Zoom-Sitzung, maximieren Sie das Fenster und Ihre gesamte Zoom-Sitzung wird in einer .mov-Datei aufgezeichnet.

Ich hoffe, diese Anweisungen waren hilfreich; zögern Sie nicht, Fragen zu stellen, wenn Sie welche haben.

### Referenzen

- _Wie man den Bildschirm auf Ihrem Mac aufnimmt_ von [Apple Support](https://support.apple.com/en-us/HT208721)
- [Soundflower-Erklärungen](https://github.com/mattingalls/Soundflower/releases/tag/2.0b2)
- _Nehmen Sie den Bildschirm Ihres Computers mit Ton auf einem Mac auf_ von [c|net](https://www.cnet.com/how-to/record-your-computers-screen-with-audio-on-a-mac/)