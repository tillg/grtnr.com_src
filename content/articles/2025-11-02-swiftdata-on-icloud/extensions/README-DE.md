---
title: SwiftData auf iCloud
tags: tech
image: swiftdata.jpeg
translation: de
source_language: en
source_hash: e44c9c8352d5cbd1ac7181bc0d857de0ea4bec037615628a030570ca311be20b
translator: gpt-4o-2024-08-06
translate_date: 2026-02-05T15:25:35.174017
generated_by: simplified-translation-system
---

**Hinweis**: Das zu diesem Artikel gehörende GitHub-Repository finden Sie [hier](https://github.com/tillg/SwiftDataOniCloud).

Während ich Swift & SwiftUI lernte und anfing, es zu nutzen, hatte ich oft Schwierigkeiten mit der Verwendung von CloudKit. Zu oft... Dies ist eine minimale Einrichtung, die ich verwendet habe, um mich in Zukunft daran zu erinnern, wie ich die Dinge eingerichtet habe, und um meine Erkenntnisse zu dokumentieren.

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
  - [Kann nicht ohne ein iCloud-Konto initialisiert werden (CKAccountStatusNoAccount).](#kann-nicht-ohne-ein-icloud-konto-initialisiert-werden-ckaccountstatusnoaccount)

## Ausgangspunkt

Fast alles, was ich über SwiftUI weiß, stammt aus dem großartigen Tutorial [100 Days of SwiftUI](https://www.hackingwithswift.com/100/swiftui) von Paul Hudson. Er leistet hervorragende Arbeit bei der Erklärung von SwiftUI und bietet diesen gut gepflegten Kurs kostenlos an.

Um nicht komplett von vorne anfangen zu müssen, nutze ich die Lektion aus dem Kurs, die SwiftData einführt: An [Tag 53](https://www.hackingwithswift.com/100/swiftui/53) startet Paul ein neues Projekt namens _Bookworm_, das SwiftData verwendet, um seine Buchdaten zu speichern. Am Ende von [Tag 55](https://www.hackingwithswift.com/100/swiftui/55) hat er eine niedliche kleine Anwendung erstellt, die ihre Daten in SwiftData speichert. Falls Sie nicht fließend in SwiftData sind oder sich nicht daran erinnern, empfehle ich dringend, die Videos dieser 3 Tage anzusehen. Seine App verwendet SwiftData, jedoch nicht in der Cloud, sondern nur lokal auf dem Gerät.

Ich werde dies als Ausgangspunkt nutzen, um iCloud-Synchronisierung hinzuzufügen. Sie finden die _Bookworm_-App in [Paul Hudsons Github-Projekt](https://github.com/twostraws/HackingWithSwift): Es befindet sich unter [SwiftUI > project 11](https://github.com/twostraws/HackingWithSwift/tree/main/SwiftUI/project11).

Wenn Sie das Verzeichnis _project 11_ klonen/kopieren und mit Xcode öffnen, müssen Sie Ihr Team und Ihre Bundle-ID einstellen, um es auszuführen.

Nun werden wir versuchen, die iCloud-Synchronisierung hinzuzufügen.

## Schritt für Schritt

### Fähigkeiten zum Xcode-Projekt hinzufügen

Um CloudKit für die Synchronisierung zu verwenden, müssen wir 2 Fähigkeiten hinzufügen:

- CloudKit (natürlich)
- Benachrichtigung: Dies ist erforderlich, damit das Gerät die Signale erhält, dass sich Daten geändert haben und erneut mit der Cloud synchronisiert werden müssen.

Wenn Sie `Xcode > Projekt: MiniSwiftData > Ziel: MiniSwiftData > Signing & Capabilities` öffnen, sollten Sie Folgendes sehen:

![Beschreibung](signing_wo_capabilities.png)

Klicken Sie auf die Schaltfläche `+ Capability` oben links und suchen Sie nach iCloud:

![Beschreibung](icloud_capability.png)

Wählen Sie dann im Abschnitt `iCloud` CloudKit als Dienst aus:

![Beschreibung](cloudkit_service.png)

Darunter benötigen wir einen Container. Klicken Sie auf `+` und geben Sie einen Namen ein. Der übliche Name wäre der Bundle Identifier, in meinem Fall ist das `com.grtnr.Bookworm` (ich kopiere & füge ihn einfach aus dem _Bundle Identifier_-Feld ein).

![Beschreibung](create_new_container.png)

Das führt zu diesem Ergebnis:

![Beschreibung](new_container.png)

Es ist rot, weil es noch nicht erstellt wurde, das dauert einfach einige Zeit.

Um Geräte synchron zu halten, verwendet iCloud die _Remote Push Notification_, daher müssen wir diesen Dienst ebenfalls hinzufügen. Klicken Sie erneut auf `+ Capability` und suchen Sie nach _Back..._:

![Beschreibung](background_modes.png)

Wählen Sie dann in der Liste der Dienste im Abschnitt _Background Modes_ die Option _Remote notifications_:

![Beschreibung](remote_notifications.png)

**Hinweis**: Wahrscheinlich hat sich der Containername inzwischen von rot zu schwarz geändert, da er in iCloud erstellt wurde.

### Modell CloudKit-fähig machen

Beim Starten der App erhalten wir jetzt einen Fehler ähnlich diesem:

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

Der Grund ist, dass ein Modell einige Einschränkungen erfüllen muss. Beim Erstellen von Modellen zur Verwendung mit CloudKit müssen wir einige Regeln einhalten:

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

Jetzt führe ich die App auf einem Simulator aus, gebe 3 Bücher ein, führe sie auf meinem echten iPhone aus - und voilà, die Bücher erscheinen auf meinem iPhone!! 🥰

## Untersuchen, Testen, Herumspielen, vielleicht Verstehen...

### CloudKit-Konsole

Beim Untersuchen, was passiert, gibt es ein sehr hilfreiches Tool: Die [CloudKit-Konsole](https://icloud.developer.apple.com):

![Beschreibung](cloudkit_console_overview.png)

Wählen Sie _CloudKit Database_ und dann die Bookworm-Datenbank aus:

![Beschreibung](bookworm_db.png)

#### Daten abfragen

Um zu sehen, welche Bücher erstellt und gespeichert wurden, müssen Sie die richtigen Optionen und Filter auswählen

![Beschreibung](bookworm_record_filters.png)

- Stellen Sie sicher, dass Sie auf der obersten Ebene die Bookworm-Datenbank > Entwicklung ausgewählt haben
- Wählen Sie **Private Datenbank**: Das bedeutet, dass wir eine benutzerbezogene Trennung der Daten haben
- Wählen Sie im Zonen-Dropdown diejenige aus, die nicht \__default_ ist, in meinem Fall ist das **com.apple.coredata.cloudkit.zone**. Ich habe keine Ahnung (noch nicht), worum es bei diesen Zonen geht...
- Wählen Sie im _RECORD TYPE_ **CD_Book**, da wir unsere Bücher ansehen möchten

Klicken Sie auf _Query Records_ und erhalten Sie einen Fehler... 😂
![Beschreibung](query_error.png)

Um dies zu beheben, wählen Sie im Menü auf der linken Seite: Schema > Record Types und sehen Sie dies:

![Beschreibung](record_types.png)

Wir sehen, dass er mit seiner Fehlermeldung recht hatte: `recordName` ist nicht als abfragbar markiert. Lassen Sie uns das beheben.

Wählen Sie im linken Menü Schema > Indexes und klicken Sie auf `+`, um einen neuen Index wie folgt zu erstellen:

![Beschreibung](new_index.png)

Kehren Sie zu Daten > Records zurück, stellen Sie Ihre Filter & Schalter ein: Private Datenbank, Zone `com.apple.coredata.cloudkit.zone`, RECORD TYPE auf CD_Books und klicken Sie auf **Query Records** und Baammm:

![Beschreibung](query_records.png)

### In Echtzeit synchronisieren

Eine der sehr coolen Funktionen von CloudKit ist die nahezu Echtzeit-Synchronisierung: Sie ändern Daten auf einem Gerät, und die Änderungen werden auf dem anderen Gerät sehr schnell sichtbar - natürlich auf Geräten, die mit derselben AppleId angemeldet sind.

Die Funktionsweise besteht darin, dass eine Benachrichtigung an alle Geräte gesendet wird, die mit dieser AppleId angemeldet sind, und dann starten sie eine Synchronisierung.

Leider erhalten Simulatoren diese Benachrichtigungen nicht. Um dies zu testen, müssen Sie Änderungen auf einem Simulator vornehmen und dann sehen, wie sie auf Ihrem echten Gerät erscheinen. Natürlich funktioniert es auch, wenn Sie 2 physische Geräte verwenden.

## Lesen

Einige wertvolle Dokumente und Erklärungen, die ich gefunden habe.

### Apple

- [Aktivieren von CloudKit in Ihrer App](https://developer.apple.com/documentation/cloudkit/enabling-cloudkit-in-your-app): Erklärt, wie Sie Ihre App konfigurieren, um Daten in iCloud mit CloudKit zu speichern.
- [Verwalten von iCloud-Containern mit der CloudKit-Datenbank-App](https://developer.apple.com/documentation/cloudkit/managing-icloud-containers-with-cloudkit-database-app#//apple_ref/doc/uid/TP40014987-CH5): Erklärt, wie Sie Daten in Ihren Containern über die Apple-Web-Entwicklung untersuchen und anzeigen können.

- [TN3164: Debugging der Synchronisation von NSPersistentCloudKitContainer](https://developer.apple.com/documentation/technotes/tn3164-debugging-the-synchronization-of-nspersistentcloudkitcontainer): Während ich versuchte herauszufinden, warum meine App keine Verbindung zu ihrem Container herstellen konnte und ständig Zugriffsprobleme meldete, ist dies der entscheidende Satz aus dieser TechNote, der mich gerettet hat:

> Wenn das Portal zeigt, dass die Zuordnung zwischen Ihrem CloudKit-Container und der App-ID korrekt ist, der Fehler jedoch weiterhin besteht, liegt es höchstwahrscheinlich daran, dass die Zuordnung nicht mit dem CloudKit-Server synchronisiert ist. In diesem Fall sollten Sie in Betracht ziehen, einen neuen CloudKit-Container zu verwenden, um Ihre Entwicklung fortzusetzen.

## Häufige Fehler

### Standardwerte für Felder

Die Felder eines Modells müssen Standardwerte haben, damit sie in CloudKit gespeichert werden können. Sie benötigen sie nicht für SwiftData, wenn Sie die Daten nur lokal auf dem Gerät speichern.

### Nicht mit AppleId angemeldet

Wenn das Gerät nicht mit einer AppleId angemeldet ist, erfolgt keine Synchronisierung.

### Entitlements wurden während des Builds geändert

```error
Entitlements file "MiniSwiftData.entitlements" was modified during the build, which is not supported. You can disable this error by setting 'CODE_SIGN_ALLOW_ENTITLEMENTS_MODIFICATION' to 'YES', however this may cause the built product's code signature or provisioning profile to contain incorrect entitlements.
```

Natürlich habe ich das Entitlement nicht direkt während des Builds von Xcode geändert. Aber die Lösung ist ziemlich einfach:

- Gehen Sie in Xcode zu _Projekt > Ziel > Signing & Capabilities_
- Deaktivieren Sie (abwählen) _Automatically manage signing_
- Wählen Sie es erneut aus
- Wählen Sie Ihr _Team_

...das war's: Xcode erstellt nun Ihre Entitlement-Datei neu.

### Kann nicht ohne ein iCloud-Konto initialisiert werden (CKAccountStatusNoAccount).

Wenn Sie nicht auf Ihrem Gerät oder Simulator angemeldet sind, kann die iCloud-Synchronisierung nicht funktionieren.

Ich habe dies gesehen und war überrascht, weil ich in iCloud angemeldet war. ABER der iCloud-Zugriff war für die App ausgeschaltet:

_Einstellungen > iCloud > In iCloud gespeichert | Alle anzeigen_. So sah der fehlerhafte Typ aus:

![Beschreibung](app_setting_icloud.png)