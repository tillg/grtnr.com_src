---
title: Ein Proxy für Offline-Surfen
tags: softwareweneed
translation: de
source_language: en
source_hash: 89911d066379b74cbf18df8ca224757dce75e2fe0b679d46e6dea69cf823c7c3
translator: gpt-4o-2024-08-06
translate_date: 2025-07-18T22:16:01.103894
generated_by: simplified-translation-system
---

Dies ist ein Stück Software, das ich gerne hätte: Ein Proxy, der auf meinem Notebook läuft und der intelligent bestimmte Websites zwischenspeichert, damit ich sie offline surfen kann.

Genauer gesagt:

- Ein Proxy, der auf meinem Notebook läuft
- Der Proxy weiß, welche Seiten/Sites ich verfügbar haben möchte, wenn ich offline bin
- Wenn der Browser eine dieser Seiten anfordert, überprüft der Proxy, ob die Website erreichbar ist. Falls ja, lädt er die Seite herunter und sendet sie an den Browser. Wenn der Proxy die Website nicht erreichen kann, versucht er, die Seite aus seinem lokalen Cache bereitzustellen.

Auf diese Weise könnte ich normal surfen, wenn ich online bin. Wenn ich offline bin, könnte ich nur auf einen kleinen Teil des Internets zugreifen – aber ich könnte trotzdem einige Seiten lesen.

Sobald dies erreicht ist, könnte der Proxy verbessert werden:

- Während er im Leerlauf ist und eine Internetverbindung hat, könnte er Seiten in seinem Cache aktualisieren
- Indem er zählt, welche Seiten ich häufig aufrufe, könnte er entscheiden, welche Seiten sinnvollerweise zwischengespeichert werden sollten
- Er könnte lernen, wie oft sich Seiten ändern, und die Aktualisierungsintervalle entsprechend anpassen
- …

Und hier sind die Fragen, die ich habe:

- Kennt jemand da draußen ein Tool, das diese Funktionalität bietet?
- Sieht jemand ein Killer-Problem, das ich übersehen habe?
- Irgendwelche guten Ideen, wie dies gebaut werden könnte?

Zur Vollständigkeit der Informationen: Ich benutze ein MacBook, OS X 10.6. Kommentare sind willkommen…

Einen schönen Abend,

– Till.