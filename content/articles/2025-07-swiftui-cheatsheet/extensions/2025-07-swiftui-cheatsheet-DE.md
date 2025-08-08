---
Tags: tech
Title: SwiftUI Spickzettel
Date: 2025-08-03
image: swiftui.png
summary: Mein Spickzettel, erstellt während ich [100 Days of SwiftUI](https://www.hackingwithswift.com/100/swiftui/) folgte.
translation: de
source_language: en
source_hash: 4ea71b7272600a018826a75cc835c7685e5512de376cbab0a168f774188aec16
translator: gpt-4o-2024-08-06
translate_date: 2025-08-05T08:16:07.589815
generated_by: simplified-translation-system
---

Im Juni 2025 begann ich mit dem Kurs [100 Days of SwiftUI](https://www.hackingwithswift.com/100/swiftui/). Es ist ein großartiger Kurs, und ich bin wirklich beeindruckt, wie viel qualitativ hochwertiger Inhalt und wie viele Kurse Paul Hudson bereitstellt - und pflegt!! Paul, vielen Dank dafür! 🙏🏼

Aber es ist eine Menge Inhalt, daher hier meine Notizen - hoffentlich in einem leicht navigierbaren Spickzettel-Format. Ich habe eine grobe Struktur im Kopf, werde den Inhalt jedoch nur bei Bedarf ausfüllen. Erwarten Sie also keine vollständige Übersicht!

## Swift

### Strings

- Sie sind besonders, und es gibt viel zu wissen...
- Das funktioniert nicht:

```swift
let name = "Paul"
let firstLetter = name[0]
```

### Optionals

- Optionals ermöglichen es uns, das Fehlen von Daten darzustellen, was bedeutet, dass wir sagen können „diese Ganzzahl hat keinen Wert“ – das ist anders als eine feste Zahl wie 0.
  - Beispiel: `var str:String?` kann einen String oder nil enthalten
- Folglich hat alles, was nicht optional ist, definitiv einen Wert, selbst wenn es nur ein leerer String ist.
- Das Entpacken eines Optionals ist der Prozess, in eine Box zu schauen, um zu sehen, was sie enthält: Wenn ein Wert darin ist, wird er zur Verwendung zurückgegeben, andernfalls ist nil darin.
- Wir können if let verwenden, um Code auszuführen, wenn das Optional einen Wert hat, oder guard let, um Code auszuführen, wenn das Optional keinen Wert hat – aber mit guard müssen wir danach immer die Funktion verlassen.
- Der nil-Koaleszenz-Operator, ??, entpackt und gibt den Wert eines Optionals zurück oder verwendet stattdessen einen Standardwert.
- Optional Chaining ermöglicht es uns, ein Optional innerhalb eines anderen Optionals mit einer praktischen Syntax zu lesen.
- Wenn eine Funktion Fehler werfen könnte, können Sie sie mit try? in ein Optional umwandeln – Sie erhalten entweder den Rückgabewert der Funktion oder nil, wenn ein Fehler auftritt.

### Dates

`Date`, `DateComponents` und `DateFormatter`

## SwiftUI

- [Interactful](https://apps.apple.com/de/app/interactful/id1528095640?l=en-GB)
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

Hinweis: Wir können nicht `ForEach(0..<5)` schreiben, weil `ForEach` einen `Range<Int>` erwartet, nicht einen `ClosedRange<Int>`!

### Dateneingabe

#### `Stepper`

![Stepper](stepper.png)
Ein Stepper ist ein zweigeteiltes Steuerelement, das Benutzer verwenden, um einen inkrementellen Wert zu erhöhen oder zu verringern.

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

Erstellen von scrollbaren Datentabellen mit `List`, insbesondere wie es Zeilen direkt aus Datenarrays erstellen kann.

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

### Bundle

Lesen von Dateien aus unserem App-Bundle, indem wir ihren Pfad mit der `Bundle` Klasse nachschlagen, einschließlich des Ladens von Strings von dort.

### Animationen

Behandelt in [Tag 32-34](https://www.hackingwithswift.com/100/swiftui/32). TODO Ich muss die Clips noch einmal ansehen, um meine Notizen/Spickzettel zu extrahieren.

- Erstellen von Animationen implizit mit dem `animation()` Modifier.
- Anpassen von Animationen mit Verzögerungen und Wiederholungen und die Wahl zwischen Ease-in-Ease-out und Spring-Animationen.
- Anheften des animation() Modifiers an Bindungen, um Änderungen direkt von UI-Steuerelementen zu animieren.
- Verwenden von `withAnimation()`, um explizite Animationen zu erstellen.
- Anheften mehrerer `animation()` Modifier an eine einzelne View, um den Animationsstapel zu steuern.

### Weitere Themen

- Maschinelles Lernen
- Ihren Code mit `fatalError()` abstürzen lassen und warum das tatsächlich eine gute Sache sein könnte.
- Wie man überprüft, ob ein String korrekt geschrieben ist, mit `UITextChecker` (es ist ein unordentliches Biest).
- Verwenden von `DragGesture()`, um dem Benutzer zu ermöglichen, Views zu verschieben, und sie dann an ihren ursprünglichen Ort zurückschnappen zu lassen.
- Bundles: Wie man eine Datei `whatever.txt` in Ihr Bundle legt, wie man darauf zugreift (d.h. sie liest). Dateinamen müssen innerhalb eines Bundles eindeutig sein.

## Fragen

- Was sind die Unterschiede zwischen einem `Form` und einem `VStack`?