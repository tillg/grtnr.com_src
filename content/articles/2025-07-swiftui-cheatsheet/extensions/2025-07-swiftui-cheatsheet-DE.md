---
Tags: tech
Title: SwiftUI Spickzettel
Date: 2025-08-03
image: swiftui.png
summary: Mein Spickzettel, erstellt während ich [100 Days of SwiftUI](https://www.hackingwithswift.com/100/swiftui/) folgte.
translation: de
source_language: en
source_hash: b2137725a3734ebc8aab07a0407f106d8a722e6d32ecc800701dbcd523ba90b7
translator: gpt-4o-2024-08-06
translate_date: 2025-08-03T08:55:42.958391
generated_by: simplified-translation-system
---

Im Juni 2025 begann ich mit [100 Days of SwiftUI](https://www.hackingwithswift.com/100/swiftui/). Es ist ein großartiger Kurs, und ich bin wirklich beeindruckt, wie viel qualitativ hochwertiger Inhalt und Kurse Paul Hudson bereitstellt - und pflegt!! Paul, vielen Dank dafür! 🙏🏼

Aber es ist eine Menge Inhalt, daher sind hier meine Notizen - hoffentlich in einem leicht navigierbaren Spickzettel-Format. Ich habe eine grobe Struktur im Kopf, aber ich werde den Inhalt nur dann ausfüllen, wenn ich ihn benötige. Erwarten Sie also keine vollständige Übersicht!

## Swift

### Optionals

- Optionals ermöglichen es uns, das Fehlen von Daten darzustellen, was bedeutet, dass wir sagen können „dieser Integer hat keinen Wert“ – das unterscheidet sich von einer festen Zahl wie 0.
  - Beispiel: `var str:String?` kann einen String oder nil enthalten
- Infolgedessen hat alles, was nicht optional ist, definitiv einen Wert, selbst wenn es nur ein leerer String ist.
- Das Entpacken eines Optionals ist der Prozess, in eine Box zu schauen, um zu sehen, was sie enthält: Wenn ein Wert darin ist, wird er zur Verwendung zurückgegeben, andernfalls wird nil darin sein.
- Wir können if let verwenden, um Code auszuführen, wenn das Optional einen Wert hat, oder guard let, um Code auszuführen, wenn das Optional keinen Wert hat – aber mit guard müssen wir die Funktion danach immer verlassen.
- Der Nil-Koaleszenz-Operator, ??, entpackt und gibt den Wert eines Optionals zurück oder verwendet stattdessen einen Standardwert.
- Optional Chaining ermöglicht es uns, ein Optional innerhalb eines anderen Optionals mit einer praktischen Syntax zu lesen.
- Wenn eine Funktion Fehler werfen könnte, können Sie sie mit try? in ein Optional umwandeln – Sie erhalten entweder den Rückgabewert der Funktion oder nil, wenn ein Fehler auftritt.

### Dates

`Date`, `DateComponents` und `DateFormatter`

## SwiftUI

### Views

- Alles ist eine View in SwiftUI 😜
- Code ausführen, wenn eine View angezeigt wird, mit `onAppear()`.

### Dateneingabe

- `Stepper` für Zahlen
- `DatePicker` für Daten. Verwendung des Parameters `displayedComponents`, um Daten oder Zeiten zu steuern.

### Listen

Erstellen von scrollbaren Datentabellen mit `List`, insbesondere wie sie Zeilen direkt aus Datenarrays erstellen kann.

### Bundle

Lesen von Dateien aus unserem App-Bundle, indem wir ihren Pfad mit der `Bundle`-Klasse nachschlagen, einschließlich des Ladens von Strings von dort.

### Animationen

Behandelt in [Tag 32-34](https://www.hackingwithswift.com/100/swiftui/32). TODO Ich muss mir die Clips noch einmal ansehen, um meine Notizen/Spickzettel zu extrahieren.

- Implizite Erstellung von Animationen mit dem `animation()`-Modifikator.
- Anpassen von Animationen mit Verzögerungen und Wiederholungen und die Wahl zwischen Ease-In-Ease-Out- und Federanimationen.
- Anbringen des `animation()`-Modifikators an Bindings, sodass wir Änderungen direkt von UI-Steuerelementen aus animieren können.
- Verwenden von `withAnimation()`, um explizite Animationen zu erstellen.
- Anbringen mehrerer `animation()`-Modifikatoren an einer einzelnen View, sodass wir den Animationsstapel steuern können.

### Andere Themen

- Maschinelles Lernen
- Ihren Code mit `fatalError()` zum Absturz bringen und warum das tatsächlich eine gute Sache sein könnte.
- Wie man überprüft, ob ein String korrekt geschrieben ist, mit `UITextChecker` (es ist ein unübersichtliches Biest).
- Verwenden von `DragGesture()`, um dem Benutzer zu ermöglichen, Views zu verschieben, und sie dann an ihren ursprünglichen Ort zurückschnappen zu lassen.