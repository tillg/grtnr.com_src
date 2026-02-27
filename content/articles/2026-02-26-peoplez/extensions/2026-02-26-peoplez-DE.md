---
date: 2026-02-26
image: address-book.svg
excerpt: Die Kontakt-App, die ich wirklich will — ein System für alle meine Leute auf iPhone, Mac und iPad, mit Listen statt Konten, intelligenter Erfassung und integrierter Konferenzvernetzung.
title: Peoplez
tags: tech, softwareweneed
translation: de
source_language: en
source_hash: c237f7a349ef05208e12c357029768aa52b6b47934421bfb12bf0e3270527102
translator: gpt-4o-2024-08-06
translate_date: 2026-02-27T10:29:59.529146+00:00
generated_by: simplified-translation-system
---

Ich habe Schwierigkeiten, meine Kontakte auf dem neuesten Stand zu halten. Die meisten sind "fast richtig" und es ist schwierig, mit Änderungen oder neuen Bekanntschaften Schritt zu halten. Ich will kein CRM. Ich möchte ein einziges Kontaktsystem, das auf meinem iPhone, Mac und iPad funktioniert — eines, das den Unterschied zwischen meinem Kollegen und meinem Nachbarn kennt, mich aber nicht zwingt, diese Trennung manuell zu verwalten.

Dieses System existiert noch nicht. Ich nenne es **Peoplez**.

## Was am Status quo falsch ist

Apples Kontakte-App unterstützt bereits mehrere Konten. Die Idee ist: Arbeitskontakte in Exchange, persönliche Kontakte in iCloud. In der Praxis schafft das mehr Probleme, als es löst:

- **Überall Duplikate** — Dieselbe Person landet in mehreren Konten, weil du sie in verschiedenen Kontexten hinzugefügt hast.
- **Falsche Standards** — Du speicherst einen Kontakt und er landet im falschen Konto. Jetzt ist er im falschen Kontext unsichtbar.
- **Keine Überschneidung** — Manche Menschen sind sowohl beruflich als auch privat. Konten erzwingen eine binäre Wahl.
- **Zerklüftete Suche** — Du kannst alle Konten gleichzeitig anzeigen, aber es gibt keine Möglichkeit, nach "zeige mir nur meine Arbeitskontakte" zu filtern, ohne ganze Konten auszublenden.

## Was Peoplez anders machen würde

### Ein System, Listen statt Konten

Alle Kontakte leben an einem Ort. Beruflich und privat sind keine separaten Konten — sie sind **Listen**. Standardmäßig sehe ich alle. Wenn ich mich konzentrieren möchte, filtere ich nach Liste.

- Ein Kontakt kann auf mehreren Listen sein: "Arbeit", "Freunde", "XConf 2026", "Skigruppe"
- Listen sind benutzerdefiniert, nicht durch die Synchronisierungsinfrastruktur vorgegeben
- Die Standardansicht zeigt alle Kontakte — kein Verstecken, kein Umschalten von Konten

### Intelligente Erfassung — Konferenzvernetzung integriert

Wenn ich auf einer Konferenz bin und jemanden treffe, erfasse ich sie auf eine von drei Arten:

**Badge-Foto** — Badges sind "kontaktähnlich", aber keine Kontakte. Ein Badge-Foto ist Rohmaterial. Peoplez würde den Namen und das Unternehmen extrahieren (OCR), einen Kontaktdraft erstellen und das Badge-Foto als Herkunft beibehalten ("getroffen bei ...").

**LinkedIn-Verknüpfung** — Der schnellste Weg, um die Identität richtig zu erfassen. [LinkedIn positioniert QR-Codes](https://www.linkedin.com/help/linkedin/answer/a525286/using-a-linkedin-qr-code-to-connect-with-members) als Möglichkeit, sich mit Menschen offline zu verbinden. Peoplez würde Verbindungen, die auf LinkedIn hergestellt wurden, aufnehmen und den Kontakt anreichern oder aktualisieren — in einer Aktion statt in drei. Peoplez würde kürzlich hinzugefügte LinkedIn-Links suchen und mir vorschlagen, sie hinzuzufügen, mit der Möglichkeit, Daten hinzuzufügen.

**Schnelle Notiz** — Manchmal möchtest du nicht mitten im Gespräch dein Handy zücken. Du merkst dir einfach: _"Anna — arbeitet bei X — sprach über iOS-Bereitstellung — im März nachfassen."_ Peoplez würde diese Notiz in einen Kontakt umwandeln (oder mit einem bestehenden abgleichen) und den Kontext als strukturierte Daten hinzufügen, nicht als zufälligen Text, der verloren geht.

In allen drei Fällen: erst erfassen, später organisieren. Der Kontakt landet in meinen Kontakten, und ich entscheide, zu welchen Listen er gehört, wenn ich bereit bin.

### Was ein Kontakt sich merken sollte

Ein nützlicher Kontakt ist nicht nur ein Name und eine Nummer. Für Menschen, die ich auf Veranstaltungen treffe, möchte ich wissen:

- **Wann** habe ich sie getroffen?
- **Wo** habe ich sie getroffen? (Veranstaltung + Stadt)
- **Worüber** haben wir gesprochen? (Themen)
- **Wo** arbeiten sie? (Unternehmen + Rolle)
- **Wann** sollte ich nachfassen?

Sowohl Apple als auch Google haben ein Notizfeld bei Kontakten — es wird nur selten genutzt, weil nichts es automatisch füllt. Peoplez würde dies zur Norm machen, nicht zur Ausnahme. Peoplez ist nur ein Tor / organisierte Leitung in meine Kontakte — die Daten des Kontakts werden immer in meiner Apple-Kontakte-App gespeichert.

### Abgleichen, Duplikate entfernen, anreichern

Wenn ein neuer Kontakt hinzukommt, würde Peoplez:

1. **Abgleichen** — "Das sieht aus wie Anna Müller, die bereits in deinen Kontakten ist — aktualisieren?"
2. **Duplikate entfernen** — Duplikate zusammenführen, die früher in separaten Konten waren
3. **Anreichern** — Unternehmen, Titel, Profil-Link (wo erlaubt) hinzufügen, die Quelle beibehalten

### Funktioniert auf allen Apple-Geräten

Peoplez speichert Kontaktdaten in Apples Kontakten, die auf iPhone, Mac und iPad synchronisiert werden. Gleiche Kontakte, gleiche Listen, gleiche Notizen. Ein System — nicht drei Apps mit drei verschiedenen Synchronisationsgeschichten.

## Die App, die ich in meinem Stack haben möchte

Peoplez ist kein CRM. Es ist keine "Networking-App". Es ist ein Tor zu Apple-Kontakten: **ein einheitliches System für alle Menschen in deinem Leben**, mit Listen statt Kontensilos, intelligenter Erfassung für die chaotische Realität, Menschen zu treffen, und reichhaltigem Kontext, damit du dich tatsächlich daran erinnerst, wer jemand sechs Monate später ist.

Das ist die Software, die ich will.