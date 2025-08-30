---
Tags: tech
Title: SwiftUI Spickzettel
Date: 2025-08-03
image: swiftui.png
summary: Mein Spickzettel, erstellt während des [100 Days of SwiftUI](https://www.hackingwithswift.com/100/swiftui/).
translation: de
source_language: en
source_hash: 12138c658800902c8d7e342da3655fe811145e94a94130c36bd16e530e93ccea
translator: gpt-4o-2024-08-06
translate_date: 2025-08-30T15:19:16.194544
generated_by: simplified-translation-system
---

Im Juni 2025 begann ich mit dem Kurs [100 Days of SwiftUI](https://www.hackingwithswift.com/100/swiftui/). Es ist ein großartiger Kurs, und ich bin wirklich beeindruckt, wie viel qualitativ hochwertiger Inhalt und Kurse Paul Hudson bereitstellt und pflegt!! Paul, vielen Dank dafür! 🙏🏼

Aber es ist eine Menge Inhalt, daher sind hier meine Notizen – hoffentlich in einem leicht navigierbaren Spickzettel-Format. Ich habe eine grobe Struktur im Kopf, aber ich werde den Inhalt nur dann ausfüllen, wenn ich ihn benötige. Erwarten Sie also keine vollständige Übersicht!

[TOC]

## Swift

Für einen umfassenden Überblick siehe [Lernen Sie essentielles Swift in einer Stunde](https://www.hackingwithswift.com/articles/242/learn-essential-swift-in-one-hour).

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

- Optionals ermöglichen es uns, das Fehlen von Daten darzustellen, was bedeutet, dass wir sagen können „dieser Integer hat keinen Wert“ – das unterscheidet sich von einer festen Zahl wie 0.
  - Beispiel: `var str:String?` kann einen String oder nil enthalten
- Folglich hat alles, was nicht optional ist, definitiv einen Wert, selbst wenn es sich nur um einen leeren String handelt.
- Das Entpacken eines Optionals ist der Prozess, in eine Box zu schauen, um zu sehen, was sie enthält: Wenn ein Wert darin ist, wird er zur Verwendung zurückgegeben, andernfalls wird nil darin sein.
- Wir können `if let` verwenden, um Code auszuführen, wenn das Optional einen Wert hat, oder guard let, um Code auszuführen, wenn das Optional keinen Wert hat – aber mit guard müssen wir danach immer die Funktion verlassen.

```swift
func printSquare(of number: Int?) {
    guard let number = number else {
        print("Fehlende Eingabe")
        return
    }

    print("\(number) x \(number) ist \(number * number)")
}
```

- Der nil-Koaleszenzoperator, ??, entpackt und gibt den Wert eines Optionals zurück oder verwendet stattdessen einen Standardwert.

```swift
let new = captains["Serenity"] ?? "N/A"
```

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

Wenn Sie komplexere Strukturen haben, müssen Sie den Vergleich mitgeben:

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

Hinweis: Wir können nicht `ForEach(0..<5)` schreiben, weil `ForEach` einen `Range<Int>` erwartet, nicht einen `ClosedRange<Int>`!

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
Ein Stepper ist eine zweigeteilte Steuerung, die Benutzer verwenden, um einen inkrementellen Wert zu erhöhen oder zu verringern.

```swift
@State private var count: Int = 0

var body: some View {
    Stepper("\(count)",
        value: $count,
        in: 0...100
    )
}
```

- `DatePicker` für Daten. Verwenden Sie den Parameter `displayedComponents`, um Daten oder Zeiten zu steuern.
- `Form`
- `Picker`
- Navigationsleiste
-

### Text

`Text` ist ein Textfeld, das Text beschreibt.

Hinweis: Textfelder mit unterschiedlichem Styling können zusammengefügt werden, um ein großes Textfeld mit unterschiedlichen Stilelementen zu bilden:

```swift
Text(page.title)
    .font(.headline)
+ Text(": ") +
Text("Seitenbeschreibung hier")
    .italic()
```

Und Sie erhalten einen Text mit unterschiedlichen kombinierten Stilelementen:

![alt text](image-4.png)

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

Buttons in Listen: Wenn Sie einen Button in eine Liste setzen, wird das GESAMTE Listenelement anklickbar! Wenn es mehr als einen Button in einer Liste gibt, wird, wo immer Sie auf das Listenelement klicken, ALLE Buttons nacheinander geklickt!

Um das zu beheben und das gewünschte Verhalten zu erhalten, verwenden Sie `.buttonStyle(.plain)`

Dasselbe gilt für HStack:

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

![alt text](image.png)

Ersetzen Sie `ScaledToFit` durch `ScaledToFill` und erhalten Sie

![alt text](image-1.png)

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

![alt text](image-2.png)

### Werkzeugleiste

### Bundle

Lesen von Dateien aus unserem App-Bundle, indem wir ihren Pfad mit der `Bundle`-Klasse nachschlagen, einschließlich des Ladens von Strings von dort.

### Animationen

Behandelt in [Tag 32-34](https://www.hackingwithswift.com/100/swiftui/32). TODO Ich muss mir die Clips noch einmal ansehen, um meine Notizen/Spickzettel zu extrahieren.

- Erstellen von Animationen implizit mit dem `animation()`-Modifier.
- Anpassen von Animationen mit Verzögerungen und Wiederholungen sowie die Wahl zwischen Ease-in-Ease-out- und Federanimationen.
- Anhängen des `animation()`-Modifiers an Bindungen, sodass wir Änderungen direkt von UI-Steuerelementen animieren können.
- Verwenden von `withAnimation()`, um explizite Animationen zu erstellen.
- Anhängen mehrerer `animation()`-Modifier an eine einzige View, sodass wir den Animationsstapel steuern können.

### Daten laden

Wenn es synchron ist:

```swift
View...
    .onAppear(loadIt)
```

?? Wie wird es gemacht, wenn `loadIt` asynchron ist??

### Werte an Views übergeben und von Views zurückgeben

Wie gesehen in [Auswählen und Bearbeiten von Kartenanmerkungen](https://www.hackingwithswift.com/books/ios-swiftui/selecting-and-editing-map-annotations)

Stellen Sie sich vor, ich habe eine View, die als Sheet geöffnet wird und eine `Location` (eine selbst definierte `struct`) erhält:

```swift
struct EditView: View {
    @Environment(\.dismiss) var dismiss
    var location: Location

    @State private var name: String
    @State private var description: String

    var body: some View {
        NavigationStack {
            Form {
                Section {
                    TextField("Ortsname", text: $name)
                    TextField("Beschreibung", text: $description)
                }
            }
            .navigationTitle("Ortsdetails")
            .toolbar {
                Button("Speichern") {
                    dismiss()
                }
            }
        }
    }
}
```

Um die `Location` zu übergeben, mache ich einen zusätzlichen Initialisierer:

```swift
init(location: Location) {
    self.location = location

    _name = State(initialValue: location.name)
    _description = State(initialValue: location.description)
}
```

Um Daten an den aufrufenden Code _zurückzugeben_, übergebe ich eine Methode `onSave`. Zuerst erstelle ich eine zusätzliche Variable in meiner View-Struktur:

```swift
var onSave: (Location) -> Void
```

und erweitere dann den Initialisierer wie folgt:

```swift
init(location: Location, onSave: @escaping (Location) -> Void) {
    self.location = location
    self.onSave = onSave

    _name = State(initialValue: location.name)
    _description = State(initialValue: location.description)
}
```

Der Teil `@escaping` ist wichtig und bedeutet, dass die Funktion für die spätere Verwendung gespeichert wird, anstatt sofort aufgerufen zu werden, und es ist hier notwendig, weil die `onSave`-Funktion nur aufgerufen wird, wenn der Benutzer auf Speichern drückt.

## Networking

So senden Sie etwas an einen HTTPS-Endpunkt:

```swift
 func placeOrder() async {
        guard let encoded = try? JSONEncoder().encode(order) else {
            print("Bestellung konnte nicht codiert werden")
            return
        }

        let url = URL(string: "https://reqres.in/api/cupcakes")!
        var request = URLRequest(url: url)
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.httpMethod = "POST"

        do {
            let (data, other) = try await URLSession.shared.upload(for: request, from: encoded)

            let decodedOrder = try JSONDecoder().decode(Order.self, from: data)
            confirmationMessage = "Ihre Bestellung über \(decodedOrder.quantity)x \(Order.types[decodedOrder.type].lowercased()) Cupcakes ist auf dem Weg!"
            showingConfirmation = true
        } catch {
            print("Checkout fehlgeschlagen: \(error.localizedDescription)")
        }
    }
```

## SwiftData

Die beweglichen Teile, die wir haben, sind

- Das `Model`: Dies ist die Datenstruktur. Das Objekt/die Objekte und seine/ihre Felder
- Der `ModelContainer`: Dies ist der persistente Speicher. Denken Sie daran wie an die Datei, in die die Daten auf dem Server geschrieben werden.
- Der `ModelContext`: Das ist die im Speicher gehaltene Version Ihrer Daten und wo die Datenänderungen gespeichert werden, bevor sie in den `ModelContainer` gespeichert werden.

Um Ihre Software für die Verwendung von SwiftData zu aktivieren, erstellen Sie zuerst ein Modell:

```swift
import Foundation
import SwiftData

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

Verwenden Sie die Daten in Ihrer View:

```swift
struct ContentView: View {
    @Environment(\.modelContext) var modelContext
    @Query(sort: [
        SortDescriptor(\Book.title),
        SortDescriptor(\Book.author)
    ]) var books: [Book]
    ...
```

Übergeben Sie ein SwiftData-Objekt an eine nachgelagerte View:

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

Löschen eines SwiftData-Objekts:

```swift
    func deleteBook() {
        modelContext.delete(book)
        dismiss()
    }
```

Hinzufügen eines Kontexts und Beispieldaten für `#Preview`:

```swift
#Preview {
    do {
        let config = ModelConfiguration(isStoredInMemoryOnly: true)
        let container = try ModelContainer(for: Book.self, configurations: config)
        let example = Book(title: "Testbuch", author: "Testautor", genre: "Fantasy", review: "Dies war ein großartiges Buch; Ich habe es wirklich genossen.", rating: 4)

        return DetailView(book: example)
            .modelContainer(container)
    } catch {
        return Text("Vorschau konnte nicht erstellt werden: \(error.localizedDescription)")
    }
}
```

## Core Image (Bildfilter)

Es ist knifflig... Schauen Sie sich die Klasse an, die es [hier](https://www.hackingwithswift.com/books/ios-swiftui/basic-image-filtering-using-core-image) erklärt

### TODO

- Erklären Sie die verschiedenen Klassen/Objekte, die es gibt, welche Funktionalität von welchem bereitgestellt wird und wie man von einem zum anderen übergeht: SwiftUI.Image - CGImage - CIImage
- Erklären Sie das Kontext- und Filterkonzept.
- Geben Sie ein Beispiel

## MapKit

- [Maps Video](https://www.hackingwithswift.com/books/ios-swiftui/integrating-mapkit-with-swiftui)
- `import MapKit`
- `Map()` zeigt eine Karte ;)
- `.mapStyle(.imagery)` oder `.hybrid` oder `.mapStyle(.hybrid(elevation: .realistic))`
- _Eingeben_ von Standorten als `MapCameraPosition`:

```swift
let startPosition = MapCameraPosition.region(
    MKCoordinateRegion(
        center: CLLocationCoordinate2D(latitude: 56, longitude: -3),
        span: MKCoordinateSpan(latitudeDelta: 10, longitudeDelta: 10)
    )
)
```

- Erhalten von Kartentipps als Koordinaten mit `MapReader`, d.h. Berechnung von Bildschirmkoordinaten --> Länge/Breite

```swift
MapReader { proxy in
    Map(initialPosition: startPosition)
        .onTapGesture { position in
            if let coordinate = proxy.convert(position, from: .local) {
                print("Angetippt bei \(coordinate)")
            }
        }
}
```

- Haben von `Marker` auf Karten

## Weitere Themen

- Maschinelles Lernen
- Absturz Ihres Codes mit `fatalError()`, und warum das tatsächlich eine gute Sache sein könnte.
- Wie man überprüft, ob ein String korrekt geschrieben ist, mit `UITextChecker`