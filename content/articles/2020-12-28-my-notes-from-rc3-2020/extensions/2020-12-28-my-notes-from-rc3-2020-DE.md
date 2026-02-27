---
image: image-1-rc3.png
title: Meine Notizen von der RC3 2020
translation: de
source_language: en
source_hash: 3f331ccbf78ad8a586c4e3cc6edadcaff49a25311e10dd4b5185c9fa796bd357
translator: gpt-4o-2024-08-06
translate_date: 2026-02-27T10:06:41.073834+00:00
generated_by: simplified-translation-system
---

Dieses Jahr (Dez 2020) hatte ich ein Ticket für die RC3. Sie wurden kostenlos verteilt, waren aber schnell vergriffen. Daher war ich stolz und verbrachte viel Zeit damit, die CCC-Sitzungen anzusehen.

Alle Vorträge sind [hier](https://media.ccc.de/c/rc3) verfügbar. Ich habe einige davon teilweise oder ganz angesehen.

Neben den Vorträgen gab es eine _2D-Welt_ - die für mich nie funktionierte 😢 (und meine Netzwerkverbindung war ziemlich gut!):
![Verbindung verloren](image-8.png)

### Eine Einführung in Tox

Ein neuer Messaging-Dienst. Besser als E-Mail, Matrix und alle anderen Messenger-Plattformen. Vorteile:

- Keine zentralen Server, keine Möglichkeit, Verschlüsselungsfunktionen zu deaktivieren.
- Funktionen von Tox: Instant Messaging, Sprach- und Videoanrufe, Bildschirmfreigabe, Dateifreigabe, Gruppen.

Es war interessant zu erfahren, dass es VIELE Chat-Protokolle gibt. Und viele von ihnen haben ähnliche Ziele: Die Daten sicher zu halten und manchmal sogar die Metadaten. Es scheint eine Entscheidung zu sein, ob Ihr Protokoll wirklich die Metadaten verbirgt (normalerweise wird dies durch die Verwendung von Tor erreicht) oder ob es niedrige Latenzzeiten bietet, um auch Sprach- und Videoanrufe zu ermöglichen.

Fragen, die mir in den Sinn kommen:

- Bietet es wirklich Videoanrufe an, oder startet es einfach andere Videoanrufe (z.B. Jitsi) - genau wie Matrix?
- Sind die Sprach- und Videoanrufe auch wirklich verschlüsselt? Denn Cisco Webex verschlüsselt seine Videoanrufe nicht (nur Chats).

![Hauptmerkmale](image-rc3.png)

Über den Typen:

![Über](image-10.png)

![Kontaktaufnahme](image-11.png)

### Der netzpolitische Wetterbericht

Live angehört, von Markus Beckedahl (von [netzpolitik.org](https://netzpolitik.org))

Was ist letztes Jahr so passiert, welche Themen sind heiß?

- Regierungen wollen Schlüssel, um verschlüsselte Kommunikation abzuhören.
- Staatstrojaner nutzen Sicherheitslücken - anstatt dass man diese schnell stopfen würde.
- SmartHome-Geräte wurden als Zeugen vor Gericht vorgeladen: Alexa hat erzählt, was ihr aufgetragen wurde.
- Das BND-Gesetz wurde als verfassungswidrig klassifiziert - schönes Erlebnis 😀. Aber ein neues BND-Gesetz wurde flott durchgepeitscht...
- Der [Podcast mit Idil Baydar](https://podcasts.apple.com/lu/podcast/npp-211-zu-fünft-mit-i-dil-baydar/id1281525246?i=1000492613815) - etwas derb, aber recht interessant, in Summe empfehlenswert.

Habe dann abgebrochen, war recht dröge...

![Zu fünft...](image-2.png)

### Digitale Integrität der menschlichen Person, ein neues Grundrecht 2020 Update

Der Typ (Alexis Roussel, Schweizer) erklärt, wie die Menschenrechte auf den digitalen Raum ausgeweitet werden sollten/könnten.

Einige interessante Punkte, die er machte:

- Es gibt einen Fehler in der DSGVO (Artikel 2): Die Regierung kann im Falle einer Gefahr auf alle Daten zugreifen. Zu vage als Beschreibung und bricht die Grundidee der DSGVO.
- In der Schweiz aktualisieren einige Kantone ihre Verfassung, um sie auf den digitalen Raum auszuweiten.

Ich habe nur 15 Minuten reingeschaut, nicht bis zum Ende zugehört...

![Wikipedia](image-3.png)

### Bausteine der Dezentralisierung

Der Typ, der spricht, ist [Will Scott](https://www.linkedin.com/in/willrscott/). Er scheint ein IPFS-Typ zu sein.

- Das derzeit größte dezentrale System ist BitTorrent

![BitTorrent-Zahlen](image-4.png)

- Ein weiteres großes verteiltes System ist [Mastodon](https://github.com/tootsuite/mastodon) "Das Fediverse". _Was zum Teufel ist das?_

![Mastodon](image-5.png)

![Mastodon-Zahlen](image-6.png)

- IPFS hat 2M Nutzer überschritten
- SSB (Secure Scuttlebutt) 100K Nutzer
- Bitcoin: 1M aktive Konten

![Modelle der Dezentralisierung](Screenshot-2020-12-28-at-19.37.34.png)

- Zentralisiert: Facebook. Föderiert: Matrix. Dezentrales Mesh?

Die eigentlichen Bausteine der Dezentralisierung:

- DHT: Distributed Hash Tables
- BFT (Byzantine Fault Tolerance) Konsens. Es scheint eine Erklärung [hier](https://academy.binance.com/en/articles/byzantine-fault-tolerance-explained) zu geben.
- Konsens kann durch _Proof of Work_ oder durch _Proof of Stake_ erreicht werden.

Er diskutierte dann die Einschränkungen dieser Bausteine: Volumen, Anzahl der Entitäten, wie viele Hops --> Latenz, Bandbreite (insbesondere Upload im Vergleich zu Download),

![Metadaten-Exposition](image-7.png)

### Weitere Vorträge...

...die ich gerne anhören würde:

- [Verwaltung von Projekten mit Gitea](https://media.ccc.de/v/rc3-channels-2020-70-verwaltung-von-projekten-mit-gitea): Nach dem Verkauf von Github an Microsoft werden sich viele die Frage gestellt haben, ob es nicht Alternativen gibt, über die man selbst die volle Kontrolle hat. Ich verwende seit zwei Jahren die Go-Anwendung Gitea sowohl für berufliche Projekte als auch für Open Source. Gitea hat den Vorteil, dass die Hürden für Installation, Wartung und Bedienung übersichtlich und schnell zu meistern sind.
  Bemerkung: ich habe den Link am 28.12.20 probiert, da schien er falsch zu sein, es wurde über ganz andere Themen gesprochen (auch interessant: Internationale Netzpolitik)
- [Digitales Klassenzimmer](https://media.ccc.de/v/rc3-11591-digitales_klassenzimmer): In diesem Workshop können Lehrerinnen und Lehrer, Schüler.innen und andere Interessierte in Freie Schulsoftware reinschnuppern. BigBlueButton? Moodle? Nextcloud? Das sind die digitalen Klassenzimmer der Zukunft.
- [rC3 Eröffnung](https://media.ccc.de/v/rc3-11583-rc3_eroffnung)

Und das war mein Fahrplan für Tag 3 (Di, 29. Dez):

![Fahrplan Tag 3](image-9.png)