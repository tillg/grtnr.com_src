---
Tags: tech
Title: SwiftUI Spickzettel
Date: 2025-08-03
image: swiftui.png
summary: Mein Spickzettel, erstellt während des Kurses [100 Days of SwiftUI](https://www.hackingwithswift.com/100/swiftui/).
translation: de
source_language: en
source_hash: b2a2fd2590a98613ee14933ee2c3d3c6b963d3e1469976664a5cc7728fb11fb0
translator: gpt-4o-2024-08-06
translate_date: 2025-08-11T11:32:45.570558
generated_by: simplified-translation-system
---

Im Juni 2025 begann ich mit dem Kurs [100 Days of SwiftUI](https://www.hackingwithswift.com/100/swiftui/). Es ist ein großartiger Kurs, und ich bin wirklich beeindruckt, wie viel qualitativ hochwertiger Inhalt und Kurse Paul Hudson bereitstellt - und pflegt!! Paul, vielen Dank dafür! 🙏🏼

Aber es ist eine Menge Inhalt, daher hier meine Notizen - hoffentlich in einem leicht navigierbaren Spickzettel-Format. Ich habe eine grobe Struktur im Kopf, werde den Inhalt aber nur bei Bedarf ausfüllen. Erwarten Sie also keine vollständige Übersicht!

[TOC]

## Swift

### Optionals

- Optionals ermöglichen es uns, das Fehlen von Daten darzustellen, was bedeutet, dass wir sagen können „dieser Integer hat keinen Wert“ – das unterscheidet sich von einer festen Zahl wie 0.
  - Beispiel: `var str:String?` kann einen String oder nil enthalten
- Folglich hat alles, was nicht optional ist, definitiv einen Wert, selbst wenn es nur ein leerer String ist.
- Das Entpacken eines Optionals ist der Prozess, in eine Box zu schauen, um zu sehen, was sie enthält: Wenn ein Wert darin ist, wird er zur Verwendung zurückgegeben, andernfalls wird nil darin sein.
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

- [Interactful](https://apps.apple.com/de/app/interactful/id1528095640?l=en-GB)
- [Human Interfaces Guideline](https://developer.apple.com/design/human-interface-guidelines/components)

### Ansichten

- Alles ist eine Ansicht in SwiftUI 😜
- Code ausführen, wenn eine Ansicht angezeigt wird, mit `onAppear()`.

Sogar `ForEach` ist eine Ansicht, deshalb können wir schreiben

```swift
ForEach(0..<5) {
    Text("Zeile \($0)")
}
```

Hinweis: Wir können nicht `ForEach(0..<5)` schreiben, weil `ForEach` einen `Range<Int>` erwartet, nicht einen `ClosedRange<Int>`!

#### `ForEach` Ansicht

`ForEach` ist eine Ansicht, die aus den Unteransichten besteht, die in jeder Schleifeninstanz erstellt werden.

Wir verwenden sie typischerweise, um Unteransichten basierend auf einem Zähler oder einem Array zu erstellen.

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

![Schrittregler](stepper.png)
Ein Schrittregler ist ein zweigeteiltes Steuerelement, das Personen verwenden, um einen inkrementellen Wert zu erhöhen oder zu verringern.

```swift
@State private var count: Int = 0

var body: some View {
    Stepper("\(count)",
        value: $count,
        in: 0...100
    )
}
```

- `DatePicker` für Daten. Verwendung des Parameters `displayedComponents`, um Daten oder Zeiten zu steuern.
- `Form`
- `Picker`
- Navigationsleiste
-

### Listen

Erstellen von scrollbaren Datentabellen mit `List`, insbesondere wie sie Zeilen direkt aus Datenarrays erstellen kann.

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

![Alternativer Text](image.png)

Ersetzen Sie `ScaledToFit` durch `ScaledToFill` und erhalten Sie

![Alternativer Text](image-1.png)

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

![Alternativer Text](image-2.png)

### Werkzeugleiste

### Bundle

Lesen von Dateien aus unserem App-Bundle, indem wir ihren Pfad mit der `Bundle`-Klasse nachschlagen, einschließlich des Ladens von Strings von dort.

### Animationen

Behandelt in [Tag 32-34](https://www.hackingwithswift.com/100/swiftui/32). TODO Ich muss die Clips noch einmal ansehen, um meine Notizen/Spickzettel zu extrahieren.

- Erstellen von Animationen implizit mit dem `animation()`-Modifikator.
- Anpassen von Animationen mit Verzögerungen und Wiederholungen und die Wahl zwischen Ease-in-Ease-out- und Federanimationen.
- Anhängen des `animation()`-Modifikators an Bindungen, sodass wir Änderungen direkt von UI-Steuerelementen aus animieren können.
- Verwenden von `withAnimation()`, um explizite Animationen zu erstellen.
- Anhängen mehrerer `animation()`-Modifikatoren an eine einzelne Ansicht, sodass wir den Animationsstapel steuern können.

### Andere Themen

- Maschinelles Lernen
- Ihren Code mit `fatalError()` abstürzen lassen und warum das tatsächlich eine gute Sache sein könnte.
- Wie man überprüft, ob ein String korrekt geschrieben ist, mit `UITextChecker` (es ist ein unübersichtliches Biest).
- Verwenden von `DragGesture()`, um dem Benutzer zu ermöglichen, Ansichten zu verschieben, und sie dann an ihren ursprünglichen Ort zurückschnappen zu lassen.
- Bundles: Wie man eine Datei `whatever.txt` in Ihr Bundle legt, wie man darauf zugreift (d.h. sie liest). Dateinamen müssen im gesamten Bundle eindeutig sein.

## Fragen

- Was sind die Unterschiede zwischen einem `Form` und einem `VStack`?