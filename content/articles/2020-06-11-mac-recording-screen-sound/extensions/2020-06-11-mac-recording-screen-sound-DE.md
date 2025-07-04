---
Translation: de
Source-Language: en
Translator: gpt-4o
Translate-Date: 2025-07-04T16:42:18.141426
Source-File: /Users/tgartner/git/grtnr.com_src/content/articles/2020-06-11-mac-recording-screen-sound/2020-06-11-mac-recording-screen-sound.md
Generated-By: automatic-translation-plugin
---

```markdown
---
layout: post
title: "Mac: Bildschirm und Ton aufnehmen"
slug: mac-recording-screen-sound
date_published: 2020-06-11T10:06:49.000Z
date_updated: 2020-06-11T17:50:04.000Z
tags:
image: MacSoundFlower.png
---

**Kurz gesagt** Um den Bildschirm Ihres Macs zusammen mit dem Ton (z.B. eine Zoom-Sitzung) aufzunehmen, können Sie Soundflower verwenden.

Hier ist, was ich erreichen wollte: Eine (Video-)Aufnahme dessen, was auf dem Bildschirm meines Macs passiert, **einschließlich des Tons**. All das, während ich gleichzeitig hören kann, was passiert. In meinem Fall wollte ich eine Zoom-Klasse aufnehmen, aber ich denke, diese Einrichtung könnte in vielen Situationen nützlich sein.

macOS verfügt über ein großartiges integriertes Bildschirmaufnahme-Tool: [QuickTime Player](https://support.apple.com/en-us/HT208721) (ja, es nimmt auf, auch wenn der Name _Player_ sagt 😀).

Das einzige Problem beim Verwenden von QuickTime Player ist der Ton: Die Auswahlmöglichkeiten sind _Internes Mikrofon_ oder _Kein_. Das passt gut, wenn Sie ein Tutorial aufnehmen möchten, bei dem der Ton das ist, was Sie über das Mikrofon erklären, aber es passt nicht zu meiner Situation.

Hier kommt [SoundFlower](https://github.com/mattingalls/Soundflower) ins Spiel. Es ist Open Source, ausgereift und zuverlässig (von mir und weit erfahreneren Kollegen getestet - und immer sehr gut bewertet). SoundFlower ist heute (Sommer 2020) kein Programm mit einer Benutzeroberfläche, sondern nur eine macOS-Systemerweiterung. Das ist etwas, das Sie als Benutzer nicht sehen, aber das im Hintergrund sehr hilfreich ist.

Was es in unserem Fall macht: Es erstellt einen neuen, virtuellen Tonkanal, der den Tonstrom in zwei andere Ströme aufteilt. In meinem Fall bedeutet das, dass ich in meiner Zoom-Sitzung einen virtuellen Ausgang anstelle des Lautsprechers meines Macs auswähle. Ich nannte diesen Ausgang _MacSpkr_SndFlwr_. Und dieser virtuelle Stream teilt den Ausgang auf den Lautsprecher des Macs und den (logischen) SoundFlower-Kanal auf. Dann wähle ich den SoundFlower-Kanal als Eingang für meine QuickTime Player-Aufnahme aus und das war's.

![Fluss](MacSoundFlower.svg)Die Tonströme

## Einrichtung

**Soundflower installieren** ist gut auf seiner [Download-Seite auf Github](https://github.com/mattingalls/Soundflower/releases/tag/2.0b2) beschrieben. Der Prozess mag etwas umständlich erscheinen, funktioniert jedoch gut, wenn Sie ihn Schritt für Schritt befolgen. Beachten Sie, dass es eine Weile gedauert hat, bis ich herausgefunden habe, was sie mit "_Sobald Sie dort sind, sollte es eine "Erlauben"-Schaltfläche (\*\*) geben, die Sie anklicken müssen, um die Erlaubnis zur Nutzung von Soundflower (Entwickler: MATT INGALLS) zu erteilen._" meinten. Ich erwartete ein Popup-Dialogfeld mit der Erlauben-Schaltfläche, aber es ist einfach eine Schaltfläche innerhalb des Fensters.

Beachten Sie auch, dass Sie Ihren Mac nach der Installation von Soundflower neu starten müssen.

Sobald Sie Soundflower installiert haben, können Sie ein logisches Audiogerät erstellen, das den Tonstrom aufteilt. Öffnen Sie dazu *Audio-MIDI-Setup*. Es ist ein macOS-Dienstprogramm, das sich in /Applications/Utilities befindet. Sie können es auch über Spotlight starten (drücken Sie Cmd + Leertaste) und geben Sie "_Audio Midi_" ein.

![Midi-App starten](Screenshot-2020-06-11-at-11.47.25.png)

_Starten des Audio-MIDI-Setups über Spotlight_

Sobald Sie sich im Audio-MIDI-Setup-Programm befinden, erstellen Sie ein neues (logisches) Audiogerät: Klicken Sie auf die "**+**"-Schaltfläche in der unteren linken Ecke und wählen Sie "_Multi-Output-Device erstellen_". Wählen Sie im rechten Bereich "_MacBook-Lautsprecher_" UND "_Soundflower (2ch)_" aus.

![Einstellungen](Screenshot-2020-06-11-at-11.14.46.png)

_Das neu erstellte Multi-Output-Device_

Starten Sie dann Ihren QuickTime Player (dieser ist auf Ihrem Mac vorinstalliert) und erstellen Sie eine neue Bildschirmaufnahme: Menü _Datei ➡ Neue Bildschirmaufnahme_. Im unteren Teil des Bildschirms erscheint ein schwebendes Menü:

![Gesamter Bildschirm](macos-catalina-screenshot-menu-record.jpg)

_Das schwebende Menü bei der Aufnahme mit QuickTime Player_

Öffnen Sie die Optionsliste und wählen Sie "Soundflower (2ch)" als Eingabe für die Aufnahme. Klicken Sie auf "Aufnehmen" und los geht's: Starten Sie jetzt Ihre Zoom-Sitzung, maximieren Sie das Fenster und Ihre gesamte Zoom-Sitzung wird in einer .mov-Datei aufgezeichnet.

Ich hoffe, diese Anweisungen waren hilfreich; zögern Sie nicht, Fragen zu stellen, wenn Sie welche haben.

### Referenzen

- _Wie man den Bildschirm auf Ihrem Mac aufnimmt_ von [Apple Support](https://support.apple.com/en-us/HT208721)
- [Soundflower-Erklärungen](https://github.com/mattingalls/Soundflower/releases/tag/2.0b2)
- _Nehmen Sie den Bildschirm Ihres Computers mit Ton auf einem Mac auf_ von [c|net](https://www.cnet.com/how-to/record-your-computers-screen-with-audio-on-a-mac/)
```