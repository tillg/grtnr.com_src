---
Tags: tech
Title: SwiftUI Spickzettel
Date: 2025-08-03
image: swiftui.png
summary: Mein Spickzettel, erstellt während ich dem Kurs [100 Days of SwiftUI](https://www.hackingwithswift.com/100/swiftui/) folgte.
translation: de
source_language: en
source_hash: be0412ee015ec415443ee3637866a75252354173dc7c0d0ac6fea67760b195ab
translator: gpt-4o-2024-08-06
translate_date: 2025-08-15T15:43:23.199587
generated_by: simplified-translation-system
---

Im Juni 2025 begann ich mit dem Kurs [100 Days of SwiftUI](https://www.hackingwithswift.com/100/swiftui/). Es ist ein großartiger Kurs, und ich bin wirklich beeindruckt, wie viel qualitativ hochwertiger Inhalt und Kurse Paul Hudson bereitstellt und pflegt!! Paul, vielen Dank dafür! 🙏🏼

Aber es ist eine Menge Inhalt, daher hier meine Notizen - hoffentlich in einem leicht navigierbaren Spickzettelformat. Ich habe eine grobe Struktur im Kopf, aber ich werde den Inhalt nur dann ausfüllen, wenn ich ihn brauche. Erwarten Sie also keine vollständige Übersicht!

[TOC]

## Swift

Für einen umfassenden Überblick siehe [Learn essential Swift in one hour](https://www.hackingwithswift.com/articles/242/learn-essential-swift-in-one-hour).

Im folgenden Kapitel habe ich nur die Teile hinzugefügt, die ich mindestens einmal überprüfen musste.

### `struct` & berechnete Eigenschaften

```swift
struct Employee {
    let name: String
    var vacationAllocated = 14
    var vacationTaken = 0

    var vacationRemaining: Int {
        vacationAllocated - vacationTaken
    }
}
```

### Optionals

- Optionals ermöglichen es uns, das Fehlen von Daten darzustellen, was bedeutet, dass wir sagen können: „Dieser Integer hat keinen Wert“ – das ist anders als eine feste Zahl wie 0.
  - Beispiel: `var str:String?` kann einen String oder nil enthalten
- Folglich hat alles, was nicht optional ist, definitiv einen Wert, auch wenn es nur ein leerer String ist.
- Das Entpacken eines Optionals ist der Prozess, in eine Box zu schauen, um zu sehen, was sie enthält: Wenn ein Wert darin ist, wird er zur Verwendung zurückgegeben, andernfalls wird nil enthalten sein.
- Wir können `if let` verwenden, um Code auszuführen, wenn das Optional einen Wert hat, oder `guard let`, um Code auszuführen, wenn das Optional keinen Wert hat – aber bei `guard` müssen wir danach immer die Funktion verlassen.

```swift
func printSquare(of number: Int?) {
    guard let number = number else {
        print("Eingabe fehlt")
        return
    }

    print("\(number) x \(number) ist \(number * number)")
}
```

- Der Nil-Coalescing-Operator, ??, entpackt und gibt den Wert eines Optionals zurück oder verwendet stattdessen einen Standardwert.

```swift
let new = captains["Serenity"] ?? "N/A"
```

- Optional Chaining ermöglicht es uns, ein Optional innerhalb eines anderen Optionals mit einer bequemen Syntax zu lesen.
- Wenn eine Funktion Fehler werfen könnte, können Sie sie mit `try?` in ein Optional umwandeln – Sie erhalten entweder den Rückgabewert der Funktion oder nil, wenn ein Fehler auftritt.

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

Wenn das Array einfach ist, können Sie einfach `sort()` direkt aufrufen, um ein Array an Ort und Stelle zu sortieren:

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

1. Fügen Sie die `Comparable`-Konformität zur Definition von User hinzu.
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

`Date`, `DateComponents`, und `DateFormatter`

## SwiftUI

- [Interactful](https://apps.apple.com/de/app/interactful/id1528095640?l=en-GB) ist ein nettes Tool, um die verschiedenen Views & Komponenten zu navigieren und auszuprobieren.
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
  let items = ["Apfel", "Banane", "Kirsche"]

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
Ein Stepper ist ein zweigeteiltes Steuerelement, das verwendet wird, um einen inkrementellen Wert zu erhöhen oder zu verringern.

```swift
@State private var count: Int = 0

var body: some View {
    Stepper("\(count)",
        value: $count,
        in: 0...100
    )
}
```

- `DatePicker` für Daten. Verwenden des Parameters `displayedComponents`, um Daten oder Zeiten zu steuern.
- `Form`
- `Picker`
- Navigationsleiste
-

### Listen

Erstellen von scrollbaren Datentabellen mit `List`, insbesondere wie es Zeilen direkt aus Datenarrays erstellen kann.

```swift
List {
    Section {
        Label("Sonne", systemImage: "sun.max")
        Label("Wolke", systemImage: "cloud")
        Label("Regen", systemImage: "cloud.rain")
    }
}
```

Buttons in Listen: Wenn Sie einen Button in eine Liste setzen, wird das GESAMTE Listenelement klickbar! Wenn es mehr als einen Button in einer Liste gibt, wird, wo immer Sie auf das Listenelement klicken, ALLE Buttons nacheinander geklickt!

Um das zu beheben und das gewünschte Verhalten zu erhalten, verwenden Sie `.buttonStyle(.plain)`

Das gleiche gilt für HStack:

```swift
HStack {
    if label.isEmpty == false {
        Text(label)
    }

    ForEach(1..<maximumRating + 1, id: \.self) { number in
        Button {
            rating = number
        } label: {
            image(for: number)
                .foregroundStyle(number > rating ? offColor : onColor)
        }
    }
}
.buttonStyle(.plain)
```

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

Lesen von Dateien aus unserem App-Bundle, indem wir ihren Pfad mit der `Bundle`-Klasse nachschlagen, einschließlich des Ladens von Strings von dort.

### Animationen

Behandelt in [Tag 32-34](https://www.hackingwithswift.com/100/swiftui/32). TODO Ich muss die Clips noch einmal ansehen, um meine Notizen/Spickzettel zu extrahieren.

- Erstellen von Animationen implizit mit dem `animation()`-Modifikator.
- Anpassen von Animationen mit Verzögerungen und Wiederholungen und die Wahl zwischen Ease-in-Ease-out und Federanimationen.
- Anhängen des `animation()`-Modifikators an Bindungen, sodass wir Änderungen direkt von UI-Steuerelementen animieren können.
- Verwenden von `withAnimation()`, um explizite Animationen zu erstellen.
- Anhängen mehrerer `animation()`-Modifikatoren an eine einzelne Ansicht, sodass wir den Animationsstapel steuern können.

## SwiftData

?? Was ist die Beziehung zwischen Model, ModelContext und ModelContainer??

Erstellen Sie zuerst ein Modell:

```swift
@Model
class Book {  // Modelle MÜSSEN Klassen sein!
    var title: String
    var author: String
    var genre: String
    var review: String
    var rating: Int
}
```

Fügen Sie den `modelContainer` auf App-Ebene hinzu

```swift

import SwiftData
import SwiftUI

@main
struct BookwormApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
        .modelContainer(for: Book.self)
    }
}
```

Verwenden Sie die Daten in Ihrer Ansicht:

```swift
struct ContentView: View {
    @Environment(\.modelContext) var modelContext
    @Query(sort: [
        SortDescriptor(\Book.title),
        SortDescriptor(\Book.author)
    ]) var books: [Book]
    ...
```

Übergeben Sie ein SwiftData-Objekt an eine nachgelagerte Ansicht:

```swift
struct DetailView: View {
    @Environment(\.modelContext) var modelContext

    let book: Book
    ...
```

Fügen Sie ein SwiftData-Objekt hinzu:

```swift

struct AddBookView: View {
    @Environment(\.modelContext) var modelContext
    var body: some View {
        NavigationStack {
            Form {
                // Dateneingabe hier
                Section {
                    Button("Speichern") {
                        let newBook = Book(title: title, author: author, genre: genre, review: review, rating: rating)
                        modelContext.insert(newBook)
                        dismiss()
                    }
                }
            }
            .navigationTitle("Buch hinzufügen")
        }
    }
}
```

Löschen Sie ein SwiftData-Objekt:

```swift
    func deleteBook() {
        modelContext.delete(book)
        dismiss()
    }
```

Hinzufügen eines Kontexts und Beispieldaten für `#Preview:

```swift
#Preview {
    do {
        let config = ModelConfiguration(isStoredInMemoryOnly: true)
        let container = try ModelContainer(for: Book.self, configurations: config)
        let example = Book(title: "Testbuch", author: "Testautor", genre: "Fantasy", review: "Das war ein großartiges Buch; ich habe es wirklich genossen.", rating: 4)

        return DetailView(book: example)
            .modelContainer(container)
    } catch {
        return Text("Vorschau konnte nicht erstellt werden: \(error.localizedDescription)")
    }
}
```

## Weitere Themen

- Maschinelles Lernen
- Ihren Code mit `fatalError()` zum Absturz bringen und warum das tatsächlich eine gute Sache sein könnte.
- Wie man überprüft, ob ein String richtig geschrieben ist, mit `UITextChecker` (es ist ein unordentliches Biest).
- Verwenden von `DragGesture()`, um dem Benutzer zu ermöglichen, Ansichten zu verschieben, und sie dann wieder an ihren ursprünglichen Ort zu schnappen.
- Bundles: Wie man eine Datei `whatever.txt` in Ihr Bundle legt, wie man darauf zugreift (d.h. sie liest). Dateinamen müssen im gesamten Bundle eindeutig sein.

## Fragen & Todos

- Was sind die Unterschiede zwischen einem `Form` und einem `VStack`?
- Multi-Screen-Setups: `Sheet` und `NavigationStack` und wie man sich bewegt
  - `NavigationStack(path)`
- Binding: `@State`, `@Bindable`, `@Binding`
- Wie man Daten in Multi-Screen-Setups weitergibt