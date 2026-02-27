---
date: 2026-02-27
image: hero.svg
excerpt: Wohin ist mein Speicherplatz verschwunden? Ein leiser Hintergrundprozess, der im Laufe der Zeit die Verzeichnisse Ihres Macs überwacht, damit Sie wissen, warum Ihr Speicher voll ist.
title: DiskSpaceTracker
tags: tech, softwareweneed, Mac
translation: de
source_language: en
source_hash: e6e3d5b71bde67af284ada3a80c67c01435c14f31288b1af7ca7a1eae9a0cea9
translator: gpt-4o-2024-08-06
translate_date: 2026-02-27T10:21:16.051831+00:00
generated_by: simplified-translation-system
---

Die Festplatte meines MacBooks füllt sich im Laufe der Zeit. Das passiert immer. Und jedes Mal, wenn ich die Benachrichtigung "Ihr Speicher ist fast voll" erhalte, habe ich keine Ahnung, was passiert ist. Habe ich etwas Großes heruntergeladen? Ist ein Cache explodiert? Hat eine App stillschweigend Gigabytes in die Library geworfen? Ich öffne das Festplattendienstprogramm, starre auf einen farbigen Balken und beginne zu raten.

So sollte es nicht funktionieren. Ich möchte einen Prozess, der meine Speichernutzung im Laufe der Zeit leise verfolgt — Verzeichnis für Verzeichnis — damit ich, wenn es eng wird, eine Zeitleiste betrachten kann und sehe: _Das ist gewachsen, das ist passiert, hier sollte ich nachsehen._

## Was DiskSpaceTracker tun würde

Ein leichter Hintergrund-Daemon, der nur dann läuft, wenn zwei Bedingungen erfüllt sind:

1. **Der Mac ist im Leerlauf** — keine aktive Benutzereingabe für N Minuten
2. **Der Mac ist am Stromnetz** — keine Batterieentladung für Buchhaltung

Wenn beide Bedingungen zutreffen, wacht er auf und erstellt einen Schnappschuss.

## Der Schnappschuss

Ein Schnappschuss durchläuft den Verzeichnisbaum von oben nach unten und erfasst für jedes Verzeichnis:

- **Pfad** — das Verzeichnis
- **Größe** — Gesamtgröße einschließlich Unterverzeichnisse
- **Inhalt-Hash** — ein Hash der `ls`-Ausgabe (Dateinamen, Größen, Änderungsdaten)
- **Zeitstempel** — wann der Schnappschuss erstellt wurde

Der Inhalt-Hash ist die Schlüsselidee. Wenn sich der Hash eines Verzeichnisses seit dem letzten Schnappschuss nicht geändert hat, hat sich darin nichts geändert — die Unterverzeichnisse werden übersprungen. Dies macht den Scan auch auf großen Festplatten schnell. Sie gehen nur tiefer, wo sich tatsächlich etwas bewegt hat.

```text
/Users/till           2026-02-27T03:12  148.2 GB  a3f8c1...
/Users/till/Downloads 2026-02-27T03:12   23.1 GB  9e2b44...  ← geändert
/Users/till/Library   2026-02-27T03:12   41.7 GB  7d1f09...  ← geändert
/Users/till/Documents 2026-02-27T03:12   62.3 GB  a3f8c1...  ← unverändert, Kinder überspringen
```

## Speicherformat

Eine einfache lokale Datenbank (SQLite wäre ausreichend) mit einer Tabelle:

| dir                        | date       | size_bytes  | content_hash |
| -------------------------- | ---------- | ----------- | ------------ |
| /Users/till/Downloads      | 2026-02-27 | 24851390464 | 9e2b44...    |
| /Users/till/Downloads      | 2026-02-20 | 19327352832 | f1a3c7...    |
| /Users/till/Library/Caches | 2026-02-27 | 8741281792  | 3bf812...    |

Jede Zeile ist ein Schnappschuss eines Verzeichnisses zu einem bestimmten Zeitpunkt. Abfragen Sie es, wie Sie möchten — Wachstum pro Woche, größte Veränderungen, Verzeichnisse, die aus dem Nichts aufgetaucht sind.

Wichtig: Die Datenbank sollte auch aufzeichnen, wann ein Verzeichnis _als unverändert bestätigt_ wurde. Wenn ich `/Users/till/Documents` scanne und der Hash derselbe ist wie letzte Woche, ist das ein Datenpunkt — "bestätigt, keine Änderung." Das ist grundlegend anders als ein Verzeichnis, das ich einfach seit Monaten nicht angesehen habe. Ohne diese Unterscheidung können Sie "stabil" nicht von "unbekannt" unterscheiden.

## Was ich sehen möchte

Eine einfache CLI oder Menüleistenansicht, die beantwortet:

- **Was ist am meisten gewachsen** in der letzten Woche / Monat?
- **Was ist neu** — Verzeichnisse oder Dateien, die vorher nicht existierten?
- **Zeitleiste** — wie hat sich `/Users/till/Library/Caches` in den letzten 6 Monaten verändert?
- **Benachrichtigungen** — benachrichtigen Sie mich, wenn ein einzelnes Verzeichnis in einer Woche um mehr als X GB wächst

Nichts Ausgefallenes. Ein paar sortierte Tabellen und vielleicht ein Sparklinediagramm. Die Daten sind das Produkt — die Benutzeroberfläche ist nur eine Möglichkeit, Fragen zu stellen.

## Warum das nicht existiert (oder warum bestehende Tools den Punkt verfehlen)

Es gibt Speicherplatzanalysatoren — DaisyDisk, GrandPerspective, ncdu. Sie zeigen Ihnen, was _jetzt_ groß ist. Das ist nützlich für eine einmalige Bereinigung, aber es sagt Ihnen nicht, was sich geändert hat. Wenn `/Library/Developer/CoreSimulator` 30 GB ist, war es immer 30 GB? Oder waren es letzten Monat 5 GB? Ohne Verlauf können Sie das nicht sagen.

Es gibt auch Überwachungstools, aber sie verfolgen den _gesamten_ freien Speicherplatz als eine Zahl. "Ihr Speicherplatz ging von 40 GB frei auf 12 GB frei in drei Wochen." Großartig — aber _wo_?

DiskSpaceTracker sitzt dazwischen: Es verfolgt den Speicherplatz pro Verzeichnis im Laufe der Zeit. Das ist das fehlende Stück.

## Technische Überlegungen

- **macOS-nativ** — verwendet `NSProcessInfo` für Leerlauferkennung, IOKit für den Stromzustand
- **Läuft als LaunchDaemon** — standardmäßige macOS-Methode zur Planung von Hintergrundarbeiten
- **SQLite-Speicherung** — einzelne Datei, kein Server, einfach abzufragen, einfach zu sichern
- **Ausschlussliste** — überspringen Sie `/System`, Time Machine-Schnappschüsse und andere nicht handlungsfähige Pfade
- **Minimaler Fußabdruck** — der hash-basierte Skip bedeutet, dass der größte Teil des Baums an ruhigen Tagen nie berührt wird
- **Intelligente Scan-Priorität** — der Scanner kann nicht jedes Mal alles überprüfen, daher muss er entscheiden, was als nächstes angesehen wird. Ein einfacher Algorithmus, der drei Faktoren abwägt: zuerst die größten Verzeichnisse (dort ist der Speicherplatz), dann die am wenigsten kürzlich gescannten Verzeichnisse (keine blinden Flecken lassen) und Verzeichnisse, deren übergeordneter Hash sich geändert hat (etwas hat sich bewegt). Auf diese Weise werden die wertvollsten Schnappschüsse zuerst gemacht, und im Laufe der Zeit bleibt die Abdeckung gleichmäßig.

Das Ganze könnte eine einzelne Swift-Binärdatei ohne Abhängigkeiten sein. Oder ein Python-Skript mit `osascript`-Hooks. Das spielt keine Rolle — die Idee ist einfach genug, dass die Implementierung fast trivial ist. Wichtig ist, dass es konsistent läuft und eine Historie aufbaut.

Das ist die Software, die ich möchte. Kein weiteres "was ist jetzt groß" Tool — ein stiller Beobachter, der eine Zeitleiste erstellt, wohin mein Speicherplatz geht, damit, wenn es eng wird, die Antwort bereits da ist.