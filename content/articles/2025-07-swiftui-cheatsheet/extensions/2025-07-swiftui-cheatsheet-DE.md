---
Tags: tech
Title: SwiftUI Spickzettel
Date: 2025-08-03
image: swiftui.png
summary: Mein Spickzettel, erstellt während ich [100 Days of SwiftUI](https://www.hackingwithswift.com/100/swiftui/) verfolgt habe.
translation: de
source_language: en
source_hash: 6eef7758d78403186edcaf2dad6921fdb12a1642e62e25ca022e92067b2c8a39
translator: gpt-4o-2024-08-06
translate_date: 2025-08-12T09:04:15.960670
generated_by: simplified-translation-system
---

Im Juni 2025 begann ich mit [100 Days of SwiftUI](https://www.hackingwithswift.com/100/swiftui/). Es ist ein großartiger Kurs, und ich bin wirklich beeindruckt, wie viel qualitativ hochwertiger Inhalt und Kurse Paul Hudson bereitstellt - und pflegt!! Paul, vielen Dank dafür! 🙏🏼

Aber es ist eine Menge Inhalt, daher hier meine Notizen - hoffentlich in einem leicht navigierbaren Spickzettelformat. Ich habe eine grobe Struktur im Kopf, aber ich werde den Inhalt nur dann ausfüllen, wenn ich ihn brauche. Erwarten Sie also keine vollständige Übersicht!

[TOC]

## Swift

Für einen umfassenden Überblick siehe [Lernen Sie essentielles Swift in einer Stunde](https://www.hackingwithswift.com/articles/242/learn-essential-swift-in-one-hour).

Im folgenden Kapitel habe ich nur die Teile hinzugefügt, die ich mindestens einmal überprüfen musste.

### Optionals

- Optionals ermöglichen es uns, das Fehlen von Daten darzustellen, was bedeutet, dass wir sagen können „dieser Integer hat keinen Wert“ – das ist anders als eine feste Zahl wie 0.
  - Beispiel: `var str:String?` kann einen String oder nil enthalten
- Folglich hat alles, was nicht optional ist, definitiv einen Wert, selbst wenn es nur ein leerer String ist.
- Das Entpacken eines Optionals ist der Prozess, in eine Box zu schauen, um zu sehen, was sie enthält: Wenn ein Wert darin ist, wird er zur Verwendung zurückgegeben, andernfalls ist nil darin.
- Wir können if let verwenden, um Code auszuführen, wenn das Optional einen Wert hat, oder guard let, um Code auszuführen, wenn das Optional keinen Wert hat – aber mit guard müssen wir danach immer die Funktion verlassen.
- Der nil-Koaleszenz-Operator, ??, entpackt und gibt den Wert eines Optionals zurück oder verwendet stattdessen einen Standardwert.
- Optional Chaining ermöglicht es uns, ein Optional innerhalb eines anderen Optionals mit einer praktischen Syntax zu lesen.
- Wenn eine Funktion Fehler werfen könnte, können Sie sie mit try? in ein Optional umwandeln – Sie erhalten entweder den Rückgabewert der Funktion oder nil, wenn ein Fehler auftritt.

### Protokolle und Erweiterungen

```swift
protocol Vehicle {
    func estimateTime(for distance: Int) -> Int
    func travel(distance: Int)
}
```

```swift
extension String {
    func trimmed() -> String {
        self.trimmingCharacters(in: .whitespacesAndNewlines)
    }
}
```

### Arrays & Sortierung

Alle Arrays haben eingebaute `sort()` und `sorted()` Methoden, die verwendet werden können, um das Array zu sortieren.

- `sort()` sortiert das Array an Ort und Stelle
- `sorted()` gibt ein neues, sortiertes Array zurück.

Wenn das Array einfach ist, können Sie `sort()` direkt aufrufen, um ein Array an Ort und Stelle zu sortieren:

```swift
var names = ["Jemima", "Peter", "David", "Kelly", "Isabella"]
names.sort()
```

Wenn Sie komplexere Strukturen haben, müssen Sie den Vergleich übergeben:

```swift
struct User {
    var firstName: String
}

var users = [
    User(firstName: "Jemima"),
    User(firstName: "Peter"),
    User(firstName: "David"),
    User(firstName: "Kelly"),
    User(firstName: "Isabella")
]

users.sort {
    $0.firstName < $1.firstName
}
```

Wir können unsere eigenen Typen `Comparable` konform machen, und wenn wir das tun, erhalten wir auch eine `sorted()` Methode ohne Parameter. Dies erfordert zwei Schritte:

1. Fügen Sie die `Comparable` Konformität zur Definition von User hinzu.
2. Fügen Sie eine Methode namens `<` hinzu, die zwei Benutzer nimmt und true zurückgibt, wenn der erste vor dem zweiten sortiert werden soll.

So sieht das im Code aus:

```swift
struct User: Identifiable, Comparable {
    let id = UUID()
    var firstName: String
    var lastName: String

    static func <(lhs: User, rhs: User) -> Bool {
        lhs.lastName < rhs.lastName
    }
}
```

### Strings

- Sie sind besonders, und es gibt viel zu wissen...
- Das funktioniert nicht:

```swift
let name = "Paul"
let firstLetter = name[0]
```

### Daten

`Date`, `DateComponents` und `DateFormatter`

## SwiftUI

- [Interactful](https://apps.apple.com/de/app/interactful/id1528095640?l=en-GB) ist ein schönes Tool, um die verschiedenen Views & Komponenten zu navigieren und auszuprobieren.
- [Human Interfaces Guideline](https://developer.apple.com/design/human-interface-guidelines/components)

### Views

- Alles ist eine View in SwiftUI 😜
- Code ausführen, wenn eine View angezeigt wird, mit `onAppear()`.

Sogar `ForEach` ist eine View, deshalb können wir schreiben

```swift
ForEach(0..<5) {
    Text("Zeile \($0)")
}
```

Hinweis: Wir können nicht `ForEach(0..<5)` schreiben, weil `ForEach` einen `Range<Int>` erwartet, keinen `ClosedRange<Int>`!

#### `ForEach` View

`ForEach` ist eine View, die aus den Unteransichten besteht, die in jeder Schleifeninstanz erstellt werden.

Wir verwenden es typischerweise, um Unteransichten basierend auf einem Zähler oder einem Array zu erstellen.

`ForEach` mit einem Array:

```swift
import SwiftUI

struct ContentView: View {
  let items = ["Apple", "Banana", "Cherry"]

  var body: some View {
    List {
      ForEach(items, id: \.self) { item in
        Text(item)
      }
    }
  }
}
```

### Dateneingabe

#### `Stepper`

![Stepper](stepper.png)
Ein Stepper ist ein zweigeteiltes Steuerelement, das Menschen verwenden, um einen inkrementellen Wert zu erhöhen oder zu verringern.

```swift
@State private var count: Int = 0

var body: some View {
    Stepper("\(count)",
        value: $count,
        in: 0...100
    )
}
```

- `DatePicker` für Daten. Verwenden des `displayedComponents` Parameters, um Daten oder Zeiten zu steuern.
- `Form`
- `Picker`
- Navigationsleiste
-

### Listen

Scrollende Tabellen von Daten mit `List` erstellen, insbesondere wie es Zeilen direkt aus Datenarrays erstellen kann.

### Bilder

```swift
struct ContentView: View
{
var body: some View {
Image (example)
    .resizable ()
    .scaledToFit ()
    .frame(width: 300, height: 300)}
}
```

![alternativer Text](image.png)

Ersetzen Sie `ScaledToFit` durch `ScaledToFill` und erhalten Sie

![alternativer Text](image-1.png)

```swift
struct ContentView: View {
    var body: some View {
        Image (•example)
            .resizable ()
            .scaledToFit()
            .containerRelativeFrame(horizontal) { size, axis in
            size * 0.8
            ｝
    }
}
```

![alternativer Text](image-2.png)

### Werkzeugleiste

### Bundle

Dateien aus unserem App-Bundle lesen, indem wir ihren Pfad mit der `Bundle` Klasse nachschlagen, einschließlich des Ladens von Strings von dort.

### Animationen

Behandelt in [Tag 32-34](https://www.hackingwithswift.com/100/swiftui/32). TODO Ich muss die Clips noch einmal ansehen, um meine Notizen/Spickzettel zu extrahieren.

- Animationen implizit mit dem `animation()` Modifikator erstellen.
- Animationen mit Verzögerungen und Wiederholungen anpassen und zwischen Ease-in-Ease-out und Federanimationen wählen.
- Den `animation()` Modifikator an Bindungen anhängen, sodass wir Änderungen direkt von UI-Steuerelementen animieren können.
- `withAnimation()` verwenden, um explizite Animationen zu erstellen.
- Mehrere `animation()` Modifikatoren an eine einzelne View anhängen, um den Animationsstapel zu steuern.

### Weitere Themen

- Maschinelles Lernen
- Ihren Code mit `fatalError()` abstürzen lassen und warum das tatsächlich eine gute Sache sein könnte.
- Wie man überprüft, ob ein String richtig geschrieben ist, mit `UITextChecker` (es ist ein unordentliches Biest).
- `DragGesture()` verwenden, um dem Benutzer zu ermöglichen, Ansichten zu verschieben, und sie dann an ihren ursprünglichen Ort zurückschnappen lassen.
- Bundles: Wie man eine Datei `whatever.txt` in Ihr Bundle legt, wie man darauf zugreift (d.h. sie liest). Dateinamen müssen innerhalb eines Bundles eindeutig sein.

## Fragen

- Was sind die Unterschiede zwischen einem `Form` und einem `VStack`?