---
date: 2025-11-02
image: swiftdata.jpeg
excerpt: Eine Schritt-für-Schritt-Anleitung zum Hinzufügen von iCloud-Synchronisierung zu einer SwiftData-App mit CloudKit, einschließlich Einrichtung, Debugging und häufiger Fallstricke.
title: SwiftData auf iCloud
tags: tech
translation: de
source_language: en
source_hash: 38d5ec309a4a6d51b7f694a80033d8dfa4d8c9249bcc5f4c1a5adb31ec6cbc30
translator: gpt-4o-2024-08-06
translate_date: 2026-02-28T09:40:49.980993+00:00
generated_by: simplified-translation-system
---

**Hinweis**: Das GitHub-Repo, das zu diesem Artikel gehört, findest Du [hier](https://github.com/tillg/SwiftDataOniCloud).

Während ich Swift & SwiftUI lernte und anfing, es zu nutzen, hatte ich oft Schwierigkeiten, CloudKit zu verwenden. Zu oft... Dies ist eine minimale Einrichtung, die ich verwendet habe, um mich in Zukunft daran zu erinnern, wie ich die Dinge eingerichtet habe und um meine Erkenntnisse zu dokumentieren.

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

Fast alles, was ich über SwiftUI weiß, stammt aus dem großartigen Tutorial [100 Days of SwiftUI](https://www.hackingwithswift.com/100/swiftui) von Paul Hudson. Er leistet fantastische Arbeit bei der Erklärung von SwiftUI und bietet diesen gut gepflegten Kurs kostenlos an.

Um nicht komplett von vorne anfangen zu müssen, nutze ich die Lektion aus dem Kurs, die SwiftData einführt: An [Tag 53](https://www.hackingwithswift.com/100/swiftui/53) startet Paul ein neues Projekt namens _Bookworm_, das SwiftData verwendet, um seine Buchdaten zu speichern. Am Ende von [Tag 55](https://www.hackingwithswift.com/100/swiftui/55) hat er eine niedliche kleine Anwendung gebaut, die ihre Daten in SwiftData speichert. Falls Du nicht mit SwiftData vertraut bist oder es nicht mehr erinnerst, empfehle ich dringend, die Videos dieser 3 Tage anzusehen. Seine App nutzt SwiftData, aber nicht in der Cloud, nur lokal auf dem Gerät.

Ich werde dies als Ausgangspunkt nutzen, um iCloud-Synchronisierung hinzuzufügen. Du findest die _Bookworm_-App in [Paul Hudsons GitHub-Projekt](https://github.com/twostraws/HackingWithSwift): Es ist unter [SwiftUI > project 11](https://github.com/twostraws/HackingWithSwift/tree/main/SwiftUI/project11).

Wenn Du das _project 11_-Verzeichnis klonst/kopierst und mit Xcode öffnest, musst Du Dein Team & Bundle Identifier einstellen, um es auszuführen.

Jetzt werden wir versuchen, iCloud-Synchronisierung hinzuzufügen.

## Schritt für Schritt

### Fähigkeiten zum Xcode-Projekt hinzufügen

Um CloudKit für die Synchronisierung zu verwenden, müssen wir 2 Fähigkeiten hinzufügen:

- CloudKit (klar)
- Benachrichtigung: Dies ist erforderlich, damit das Gerät die Signale erhält, dass sich Daten geändert haben und erneut mit der Cloud synchronisiert werden müssen.

Wenn Du `Xcode > Project: MiniSwiftData > Target: MiniSwiftData > Signing & Capabilities` öffnest, solltest Du Folgendes sehen:

![Beschreibung](signing_wo_capabilities.png)

Klicke auf die Schaltfläche `+ Capability` oben links und suche nach iCloud:

![Beschreibung](icloud_capability.png)

Wähle dann im Abschnitt `iCloud` CloudKit als Dienst aus:

![Beschreibung](cloudkit_service.png)

Darunter benötigen wir einen Container. Klicke auf `+` und gib einen Namen ein. Der übliche Name wäre der Bundle Identifier, in meinem Fall ist das `com.grtnr.Bookworm` (ich kopiere & füge es einfach aus dem _Bundle Identifier_-Feld ein).

![Beschreibung](create_new_container.png)

Das führt zu Folgendem:

![Beschreibung](new_container.png)

Es ist rot, weil es noch nicht erstellt wurde, das dauert einfach etwas Zeit.

Um Geräte synchron zu halten, verwendet iCloud die _Remote Push Notification_, also müssen wir diesen Dienst ebenfalls hinzufügen. Klicke erneut auf `+ Capability` und suche nach _Back..._:

![Beschreibung](background_modes.png)

Wähle dann in der Liste der Dienste im Abschnitt _Background Modes_ die Option _Remote notifications_:

![Beschreibung](remote_notifications.png)

**Hinweis**: Wahrscheinlich ist der Containername inzwischen von rot zu schwarz gewechselt, da er in iCloud erstellt wurde.

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

Der Grund ist, dass ein Modell einige Einschränkungen erfüllen muss. Beim Erstellen von Modellen für die Verwendung mit CloudKit müssen wir einige Regeln beachten:

- Eigenschaften-Standardwerte: Jede Eigenschaft benötigt einen Standardwert - es sei denn, sie ist optional.
- `@Unique` kann nicht verwendet werden

Also habe ich einfach die `Book.swift`-Datei geändert:

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

![Beschreibung](cloudkit_console_overview.png)

Wähle _CloudKit Database_ und dann die Bookworm-Datenbank:

![Beschreibung](bookworm_db.png)

#### Daten abfragen

Um zu sehen, welche Bücher erstellt und gespeichert wurden, musst Du die richtigen Optionen und Filter auswählen

![Beschreibung](bookworm_record_filters.png)

- Stelle sicher, dass Du auf der obersten Ebene die Bookworm-Datenbank > Entwicklung ausgewählt hast
- Wähle **Private Datenbank**: Das bedeutet, dass wir eine benutzerspezifische Trennung der Daten haben
- Im Dropdown für die Zone wähle die, die nicht \__default_ ist, in meinem Fall ist das **com.apple.coredata.cloudkit.zone**. Ich habe keine Ahnung (noch nicht), worum es bei diesen Zonen geht...
- Wähle im _RECORD TYPE_ **CD_Book**, weil wir unsere Bücher ansehen wollen

Klicke auf _Query Records_ und erhalte einen Fehler... 😂
![Beschreibung](query_error.png)

Um das zu beheben, wähle im Menü auf der linken Seite: Schema > Record Types und sieh Dir das an:

![Beschreibung](record_types.png)

Wir sehen, dass er mit seiner Fehlermeldung recht hatte: `recordName` ist nicht als abfragbar markiert. Also lass uns das beheben.

Wähle im linken Menü Schema > Indexes und klicke auf `+`, um einen neuen Index wie folgt zu erstellen:

![Beschreibung](new_index.png)

Kehre zu Daten > Records zurück, setze Deine Filter & Schalter: Private Datenbank, Zone `com.apple.coredata.cloudkit.zone`, RECORD TYPE auf CD_Books und klicke auf **Query Records** und Baammm:

![Beschreibung](query_records.png)

### In Echtzeit synchronisieren

Eine der sehr coolen Funktionen von CloudKit ist die nahezu Echtzeit-Synchronisierung: Du änderst Daten auf einem Gerät, und die Änderungen werden auf dem anderen Gerät sehr schnell sichtbar - natürlich auf Geräten, die mit derselben AppleId angemeldet sind.

Das funktioniert so, dass eine Benachrichtigung an alle Geräte gesendet wird, die mit dieser AppleId angemeldet sind, und dann starten sie eine Synchronisierung.

Leider erhalten Simulatoren diese Benachrichtigungen nicht. Um es zu testen, musst Du also Änderungen auf einem Simulator vornehmen und dann sehen, wie sie auf Deinem echten Gerät erscheinen. Natürlich funktioniert es auch, wenn Du 2 physische Geräte verwendest.

## Lesen

Einige wertvolle Dokumente und Erklärungen, die ich gefunden habe.

### Apple

- [Enabling CloudKit in Your App](https://developer.apple.com/documentation/cloudkit/enabling-cloudkit-in-your-app): Erklärt, wie Du Deine App konfigurierst, um Daten in iCloud mit CloudKit zu speichern.
- [Managing iCloud Containers with CloudKit Database App](https://developer.apple.com/documentation/cloudkit/managing-icloud-containers-with-cloudkit-database-app#//apple_ref/doc/uid/TP40014987-CH5): Erklärt, wie Du Daten in Deinen Containern über das Apple Web Dev untersuchst und siehst.

- [TN3164: Debugging the synchronization of NSPersistentCloudKitContainer](https://developer.apple.com/documentation/technotes/tn3164-debugging-the-synchronization-of-nspersistentcloudkitcontainer): Während ich versuchte herauszufinden, warum meine App keine Verbindung zu ihrem Container herstellen konnte und ständig Zugriffsprobleme meldete, war dies der entscheidende Satz aus diesem TechNote, der mich rettete:

> Wenn das Portal zeigt, dass die Zuordnung zwischen Deinem CloudKit-Container und der App-ID korrekt ist, der Fehler jedoch weiterhin besteht, liegt es höchstwahrscheinlich daran, dass die Zuordnung nicht mit dem CloudKit-Server synchronisiert ist. In diesem Fall solltest Du in Betracht ziehen, einen neuen CloudKit-Container zu verwenden, um Deine Entwicklung fortzusetzen.

## Häufige Fehler

### Standardwerte für Felder

Die Felder eines Modells müssen Standardwerte haben, damit sie in CloudKit gespeichert werden können. Du benötigst sie nicht für SwiftData, wenn Du die Daten nur lokal auf dem Gerät speicherst.

### Nicht mit AppleId angemeldet

Wenn das Gerät nicht mit einer AppleId angemeldet ist, synchronisiert es nicht.

### Entitlements wurden während des Builds geändert

```error
Entitlements file "MiniSwiftData.entitlements" was modified during the build, which is not supported. You can disable this error by setting 'CODE_SIGN_ALLOW_ENTITLEMENTS_MODIFICATION' to 'YES', however this may cause the built product's code signature or provisioning profile to contain incorrect entitlements.
```

Natürlich habe ich die Entitlements nicht während des Builds geändert. Aber die Lösung ist ziemlich einfach:

- In Xcode gehe zu _Project > Target > Signing & Capabilities_
- Deaktiviere (deselektiere) _Automatically manage signing_
- Wähle es erneut aus
- Wähle Dein _Team_

...das war's: Xcode erstellt nun Deine Entitlement-Datei neu.

### Kann nicht ohne ein iCloud-Konto initialisiert werden (CKAccountStatusNoAccount).

Wenn Du nicht auf Deinem Gerät oder Simulator angemeldet bist, kann die iCloud-Synchronisierung nicht funktionieren.

Ich habe das gesehen und war überrascht, weil ich in iCloud angemeldet war. ABER der iCloud-Zugriff war für die App deaktiviert:

_Einstellungen > iCloud > Gespeichert in iCloud | Alle anzeigen_. So sah der fehlerhafte Typ aus:

![Beschreibung](app_setting_icloud.png)