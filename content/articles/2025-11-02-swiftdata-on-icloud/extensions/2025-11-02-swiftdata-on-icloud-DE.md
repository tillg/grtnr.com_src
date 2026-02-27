---
date: 2025-11-02
image: swiftdata.jpeg
excerpt: Eine Schritt-für-Schritt-Anleitung zum Hinzufügen von iCloud-Synchronisation zu einer SwiftData-App mit CloudKit, einschließlich Einrichtung, Debugging und häufigen Fallstricken.
title: SwiftData auf iCloud
tags: tech
translation: de
source_language: en
source_hash: e72d7ff9ad962aa771f3fc92699c91da6d4bf3486cbb78ec2572e22b66b39e62
translator: gpt-4o-2024-08-06
translate_date: 2026-02-27T10:29:49.554179+00:00
generated_by: simplified-translation-system
---

**Hinweis**: Das GitHub-Repo, das zu diesem Artikel gehört, findest du [hier](https://github.com/tillg/SwiftDataOniCloud).

Während ich Swift & SwiftUI gelernt habe und es zu verwenden begann, hatte ich oft Schwierigkeiten, CloudKit zu nutzen. Zu oft... Dies ist eine minimale Einrichtung, die ich verwendet habe, um mich in Zukunft daran zu erinnern, wie ich die Dinge eingerichtet habe und um meine Erkenntnisse zu dokumentieren.

- [Ausgangspunkt](#ausgangspunkt)
- [Schritt für Schritt](#schritt-für-schritt)
  - [Fähigkeiten zum Xcode-Projekt hinzufügen](#fähigkeiten-zum-xcode-projekt-hinzufügen)
  - [Modell CloudKit-fähig machen](#modell-cloudkit-fähig-machen)
- [Untersuchen, Testen, Herumspielen, vielleicht Verstehen...](#untersuchen-testen-herumspielen-vielleicht-verstehen)
  - [CloudKit-Konsole](#cloudkit-konsole)
    - [Daten abfragen](#daten-abfragen)
  - [In Echtzeit synchronisieren](#in-echtzeit-synchronisieren)
- [Lesen](#lesen)
  - [Apple](#apple)
- [Häufige Fehler](#häufige-fehler)
  - [Standardwerte für Felder](#standardwerte-für-felder)
  - [Nicht mit AppleId angemeldet](#nicht-mit-appleid-angemeldet)
  - [Entitlements wurden während des Builds geändert](#entitlements-wurden-während-des-builds-geändert)
  - [Kann ohne iCloud-Konto nicht initialisieren (CKAccountStatusNoAccount).](#kann-ohne-icloud-konto-nicht-initialisieren-ckaccountstatusnoaccount)

## Ausgangspunkt

Fast alles, was ich über SwiftUI weiß, stammt aus dem großartigen Tutorial [100 Days of SwiftUI](https://www.hackingwithswift.com/100/swiftui) von Paul Hudson. Er leistet fantastische Arbeit bei der Erklärung von SwiftUI und bietet diesen gut gepflegten Kurs kostenlos an.

Um nicht komplett von vorne anfangen zu müssen, nutze ich die Lektion aus dem Kurs, die SwiftData einführt: An [Tag 53](https://www.hackingwithswift.com/100/swiftui/53) startet Paul ein neues Projekt namens _Bookworm_, das SwiftData verwendet, um seine Buchdaten zu speichern. Am Ende von [Tag 55](https://www.hackingwithswift.com/100/swiftui/55) hat er eine niedliche kleine Anwendung gebaut, die ihre Daten in SwiftData speichert. Falls du nicht fließend in SwiftData bist oder dich nicht daran erinnerst, empfehle ich dringend, die Videos dieser 3 Tage anzusehen. Seine App verwendet SwiftData, aber nicht in der Cloud, sondern nur lokal auf dem Gerät.

Ich werde dies als Ausgangspunkt nutzen, um iCloud-Synchronisation hinzuzufügen. Du findest die _Bookworm_-App in [Paul Hudsons GitHub-Projekt](https://github.com/twostraws/HackingWithSwift): Sie befindet sich unter [SwiftUI > project 11](https://github.com/twostraws/HackingWithSwift/tree/main/SwiftUI/project11).

Wenn du das Verzeichnis _project 11_ klonst / kopierst und mit Xcode öffnest, musst du dein Team & Bundle Identifier einstellen, um es auszuführen.

Jetzt werden wir versuchen, iCloud-Synchronisation hinzuzufügen.

## Schritt für Schritt

### Fähigkeiten zum Xcode-Projekt hinzufügen

Um CloudKit für die Synchronisation zu verwenden, müssen wir 2 Fähigkeiten hinzufügen:

- CloudKit (klar)
- Benachrichtigung: Dies ist notwendig, damit das Gerät die Signale erhält, dass sich Daten geändert haben und erneut mit der Cloud synchronisiert werden müssen.

Wenn du `Xcode > Project: MiniSwiftData > Target: MiniSwiftData > Signing & Capabilities` öffnest, solltest du Folgendes sehen:

![alt text](signing_wo_capabilities.png)

Klicke auf die Schaltfläche `+ Capability` oben links und suche nach iCloud:

![alt text](icloud_capability.png)

Wähle dann im Abschnitt `iCloud` CloudKit als Dienst aus:

![alt text](cloudkit_service.png)

Unten brauchen wir dann einen Container. Klicke auf `+` und gib einen Namen ein. Der übliche Name wäre der Bundle Identifier, in meinem Fall ist das `com.grtnr.Bookworm` (ich kopiere & füge ihn einfach aus dem _Bundle Identifier_-Feld ein).

![alt text](create_new_container.png)

Das führt zu diesem Ergebnis:

![alt text](new_container.png)

Es ist rot, weil es noch nicht erstellt wurde, das dauert einfach eine Weile.

Um Geräte synchron zu halten, verwendet iCloud die _Remote Push Notification_, daher müssen wir diesen Dienst ebenfalls hinzufügen. Klicke erneut auf `+ Capability` und suche nach _Back..._:

![alt text](background_modes.png)

Wähle dann in der Liste der Dienste im Abschnitt _Background Modes_ die Option _Remote notifications_:

![alt text](remote_notifications.png)

**Hinweis**: Wahrscheinlich ist der Containername inzwischen von rot zu schwarz gewechselt, da er in iCloud erstellt wurde.

### Modell CloudKit-fähig machen

Wenn wir die App jetzt starten, erhalten wir einen Fehler ähnlich diesem:

```bash
CoreData: error: Store failed to load.  <NSPersistentStoreDescription: 0x600000c0e670> (type: SQLite, url: file:///Users/tgartner/Library/Developer/CoreSimulator/Devices/1464DFC4-EE76-43DB-B178-C33F1FA97A91/data/Containers/Data/Application/34DEE59B-975D-4784-8A87-DC38A9D9DA37/Library/Application%20Support/default.store) with error = Error Domain=NSCocoaErrorDomain Code=134060 "A Core Data error occurred." UserInfo={NSLocalizedFailureReason=CloudKit integration requires that all attributes be optional, or have a default value set. The following attributes are marked non-optional but do not have a default value:
Book: author
Book: genre
Book: rating
Book: review
Book: title} with userInfo {
    NSLocalizedFailureReason = "CloudKit integration requires that all attributes be optional, or have a default value set. The following attributes are marked non-optional but do not have a default value:\nBook: author\nBook: genre\nBook: rating\nBook: review\nBook: title";
}
```

Der Grund ist, dass ein Modell ein paar Einschränkungen erfüllen muss. Beim Erstellen von Modellen für die Verwendung mit CloudKit müssen wir einige Regeln beachten:

- Standardwerte für Eigenschaften: Jede Eigenschaft benötigt einen Standardwert - es sei denn, sie ist optional.
- `@Unique` kann nicht verwendet werden

Also habe ich einfach die Datei `Book.swift` geändert:

```swift
import Foundation
import SwiftData

@Model
class Book {
    var title: String = ""
    var author: String = ""
    var genre: String = ""
    var review: String = ""
    var rating: Int = 3

    init(title: String, author: String, genre: String, review: String, rating: Int) {
        self.title = title
        self.author = author
        self.genre = genre
        self.review = review
        self.rating = rating
    }
}
```

Jetzt starte ich die App auf einem Simulator, gebe 3 Bücher ein, starte sie auf meinem echten iPhone - et voilà, die Bücher erscheinen auf meinem iPhone!! 🥰

## Untersuchen, Testen, Herumspielen, vielleicht Verstehen...

### CloudKit-Konsole

Beim Untersuchen, was passiert, gibt es ein sehr hilfreiches Tool: Die [CloudKit-Konsole](https://icloud.developer.apple.com):

![alt text](cloudkit_console_overview.png)

Wähle _CloudKit Database_ und dann die Bookworm-Datenbank:

![alt text](bookworm_db.png)

#### Daten abfragen

Um zu sehen, welche Bücher erstellt und gespeichert wurden, musst du die richtigen Optionen und Filter auswählen

![alt text](bookworm_record_filters.png)

- Stelle sicher, dass du auf der obersten Ebene die Bookworm-Datenbank > Entwicklung ausgewählt hast
- Wähle **Private Datenbank**: Das bedeutet, dass wir eine pro Benutzer Trennung der Daten haben
- Im Zonen-Dropdown wähle die, die nicht die \__default_ ist, in meinem Fall ist das **com.apple.coredata.cloudkit.zone**. Ich habe keine Ahnung (noch nicht), worum es bei diesen Zonen geht...
- In _RECORD TYPE_ wähle **CD_Book**, weil wir unsere Bücher ansehen wollen

Drücke _Query Records_ und erhalte einen Fehler... 😂
![alt text](query_error.png)

Um dies zu beheben, wähle im Menü auf der linken Seite: Schema > Record Types und sieh dir das an:

![alt text](record_types.png)

Wir sehen, dass er mit seiner Fehlermeldung Recht hatte: `recordName` ist nicht als abfragbar markiert. Also lass uns das beheben.

Wähle im linken Menü Schema > Indexes und klicke auf `+`, um einen neuen Index wie folgt zu erstellen:

![alt text](new_index.png)

Kehre zu den Daten > Records zurück, setze deine Filter & Schalter: Private Datenbank, Zone `com.apple.coredata.cloudkit.zone`, RECORD TYPE zu CD_Books und drücke **Query Records** und Baammm:

![alt text](query_records.png)

### In Echtzeit synchronisieren

Eine der sehr coolen Funktionen von CloudKit ist die nahezu Echtzeit-Synchronisation: Du änderst Daten auf einem Gerät, und die Änderungen werden sehr schnell auf dem anderen Gerät sichtbar - natürlich auf Geräten, die mit derselben AppleId angemeldet sind.

So funktioniert das: Eine Benachrichtigung wird an alle Geräte gesendet, die mit dieser AppleId angemeldet sind, und dann starten sie eine Synchronisation.

Leider erhalten Simulatoren diese Benachrichtigungen nicht. Um es zu testen, musst du also Änderungen auf einem Simulator vornehmen und dann sehen, wie sie auf deinem echten Gerät erscheinen. Natürlich funktioniert es auch, wenn du 2 physische Geräte verwendest.

## Lesen

Einige wertvolle Dokumente und Erklärungen, die ich gefunden habe.

### Apple

- [Enabling CloudKit in Your App](https://developer.apple.com/documentation/cloudkit/enabling-cloudkit-in-your-app): Erklärt, wie du deine App konfigurierst, um Daten in iCloud mit CloudKit zu speichern.
- [Managing iCloud Containers with CloudKit Database App](https://developer.apple.com/documentation/cloudkit/managing-icloud-containers-with-cloudkit-database-app#//apple_ref/doc/uid/TP40014987-CH5): Erklärt, wie du Daten in deinen Containern über das Apple Web Dev untersuchen und sehen kannst.

- [TN3164: Debugging the synchronization of NSPersistentCloudKitContainer](https://developer.apple.com/documentation/technotes/tn3164-debugging-the-synchronization-of-nspersistentcloudkitcontainer): Während ich versuchte herauszufinden, warum meine App nicht mit ihrem Container verbinden konnte und ständig Zugriffsprobleme meldete, war dies der Schlüsselsatz aus dieser TechNote, der mich rettete:

> Wenn das Portal zeigt, dass die Zuordnung zwischen deinem CloudKit-Container und der App-ID korrekt ist, der Fehler jedoch weiterhin besteht, liegt es höchstwahrscheinlich daran, dass die Zuordnung nicht mit dem CloudKit-Server synchronisiert ist. In diesem Fall solltest du in Betracht ziehen, einen neuen CloudKit-Container für die weitere Entwicklung zu verwenden.

## Häufige Fehler

### Standardwerte für Felder

Die Felder eines Modells müssen Standardwerte haben, damit sie in CloudKit gespeichert werden können. Du benötigst sie nicht für SwiftData, wenn du die Daten nur lokal auf dem Gerät speicherst.

### Nicht mit AppleId angemeldet

Wenn das Gerät nicht mit einer AppleId angemeldet ist, synchronisiert es nicht.

### Entitlements wurden während des Builds geändert

```error
Entitlements file "MiniSwiftData.entitlements" was modified during the build, which is not supported. You can disable this error by setting 'CODE_SIGN_ALLOW_ENTITLEMENTS_MODIFICATION' to 'YES', however this may cause the built product's code signature or provisioning profile to contain incorrect entitlements.
```

Natürlich habe ich die Entitlements nicht direkt während des Xcode-Builds geändert. Aber die Lösung dafür ist ziemlich einfach:

- Gehe in Xcode zu _Project > Target > Signing & Capabilities_
- Deaktiviere (deselektiere) _Automatically manage signing_
- Wähle es erneut aus
- Wähle dein _Team_

...das war's: Xcode erstellt nun deine Entitlement-Datei neu.

### Kann ohne iCloud-Konto nicht initialisieren (CKAccountStatusNoAccount).

Wenn du nicht auf deinem Gerät oder Simulator angemeldet bist, kann die iCloud-Synchronisation nicht funktionieren.

Ich habe dies gesehen und war überrascht, weil ich bei iCloud angemeldet WAR. ABER der iCloud-Zugriff war für die App deaktiviert:

_Einstellungen > iCloud > In iCloud gespeichert | Alle anzeigen_. So sah der fehlerhafte Typ aus:

![alt text](app_setting_icloud.png)