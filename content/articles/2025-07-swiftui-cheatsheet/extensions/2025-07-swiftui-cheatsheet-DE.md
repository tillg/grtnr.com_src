---
Tags: tech
Title: SwiftUI Cheatsheet
Date: 2025-08-03
image: swiftui.png
summary: Mein Spickzettel, erstellt während des Kurses [100 Days of SwiftUI](https://www.hackingwithswift.com/100/swiftui/).
title: SwiftUI&nbsp;Spickzettel
translation: de
source_language: en
source_hash: af1e5f2c544add545bc814587612c9166d16e28b95a8d8835bbab8ec89b2887d
translator: gpt-4o-2024-08-06
translate_date: 2026-02-14T10:51:45.440482
generated_by: simplified-translation-system
---

Im Juni 2025 begann ich mit dem Kurs [100 Days of SwiftUI](https://www.hackingwithswift.com/100/swiftui/). Es ist ein großartiger Kurs, und ich bin wirklich beeindruckt, wie viel qualitativ hochwertige Inhalte und Kurse Paul Hudson bereitstellt und pflegt!! Paul, vielen Dank dafür! 🙏🏼

Aber es ist eine Menge Inhalt, daher hier meine Notizen - hoffentlich in einem leicht navigierbaren Spickzettelformat. Ich habe eine grobe Struktur im Kopf, werde den Inhalt jedoch nur dann ausfüllen, wenn ich ihn benötige. Erwarten Sie also keine vollständige Übersicht!

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

- Optionals ermöglichen es uns, das Fehlen von Daten darzustellen, was bedeutet, dass wir sagen können: „Dieser Integer hat keinen Wert“ – das unterscheidet sich von einer festen Zahl wie 0.
  - Beispiel: `var str:String?` kann einen String oder nil enthalten
- Folglich hat alles, was nicht optional ist, definitiv einen Wert, auch wenn es nur ein leerer String ist.
- Das Entpacken eines Optionals ist der Prozess, in eine Box zu schauen, um zu sehen, was sie enthält: Wenn ein Wert darin ist, wird er zur Verwendung zurückgegeben, andernfalls wird nil darin sein.
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

- Der Nil-Koaleszenzoperator, ??, entpackt und gibt den Wert eines Optionals zurück oder verwendet stattdessen einen Standardwert.

```swift
let new = captains["Serenity"] ?? "N/A"
```

- Optional Chaining ermöglicht es uns, ein Optional innerhalb eines anderen Optionals mit einer praktischen Syntax zu lesen.
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

`Date`, `DateComponents` und `DateFormatter`

### `enum`

`enum` werden so erstellt:

```swift
enum Weekday {
    case monday, tuesday, wednesday, thursday, friday
}
```

Eine `switch`-Anweisung mit `enum` sieht so aus:

```swift
switch loadingState {
case .loading:
    LoadingView()
case .success:
    SuccessView()
case .failed:
    FailedView()
}
```

## SwiftUI

- [Interactful](https://apps.apple.com/de/app/interactful/id1528095640?l=en-GB) ist ein nützliches Tool, um die verschiedenen Ansichten und Komponenten zu navigieren und auszuprobieren.
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

Hinweis: Wir können nicht `ForEach(0..<5)` schreiben, da `ForEach` einen `Range<Int>` erwartet, nicht einen `ClosedRange<Int>`!

#### `ForEach` Ansicht

`ForEach` ist eine Ansicht, die aus den Unteransichten besteht, die in jeder Schleifeninstanz erstellt werden.

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

#### `TextField`

#### `Picker`

`Picker` wird verwendet, um eine von vielen möglichen Auswahlmöglichkeiten zu treffen.

Ein regulärer Picker sieht so aus:

```swift
Picker("Anzahl der Personen", selection: $numberOfPeople) {
    ForEach(2 ..< 100 , id: \.self) {
        Text("\($0) Personen")
    }
}
```

![alternativer Text](image-7.png)

Ein `Picker` kann mit dem `PickerStyle`-Modifier modifiziert werden:

```swift
Picker("Trinkgeld-Prozentsatz", selection: $tipPercentage) {
    ForEach(tipPercentages, id: \.self) {
        Text($0, format: .percent)
    }
}
.pickerStyle(.segmented)
```

![alternativer Text](image-8.png)

#### `Stepper`

![Stepper](stepper.png)
Ein Stepper ist eine zweigeteilte Steuerung, die verwendet wird, um einen inkrementellen Wert zu erhöhen oder zu verringern.

```swift
@State private var count: Int = 0

var body: some View {
    Stepper("\(count)",
        value: $count,
        in: 0...100
    )
}
```

- `DatePicker` für Daten. Verwenden Sie den `displayedComponents`-Parameter, um Daten oder Zeiten zu steuern.
- `Form`
- `Picker`
- Navigationsleiste

### Warnungen & Bestätigungsdialoge

#### Warnungen

Warnungen sind eine Erweiterung einer Ansicht mit einer Bool-Variablen, die entscheidet, ob sie angezeigt werden oder nicht.

```swift
struct ContentView: View {
    @State private var showingAlert = false

    var body: some View {
        Button("Warnung anzeigen") {
            showingAlert = true
        }
        .alert("Wichtige Nachricht", isPresented: $showingAlert) {
            Button("OK") { }
        }
    }
}
```

#### Bestätigungsdialoge

Verwenden Sie sie, wenn viele Schaltflächen/Optionen verfügbar sind. Für Beispielcode siehe [dieses Repo](https://github.com/tillg/100DaysOfSwiftUI/blob/main/16.5-AlertAndConfirmation/AlertAndConfirmation/AlertAndConfirmation/ContentView.swift).

**Hinweis**: Vor iOS 26 schoben sie sich von unten herein, in iOS 26 erscheinen sie innerhalb des Bildschirms.

Bestätigungsdialog in iOS 18.5:
![alternativer Text](image-6.png)

Bestätigungsdialog in iOS 26:
![alternativer Text](image-5.png)

### Text

`Text` ist ein Textfeld, das Text beschreibt.

Hinweis: Textfelder mit unterschiedlichem Styling können zusammengefügt werden, um ein großes Textfeld mit Teilen mit unterschiedlichem Styling zu bilden:

```swift
Text(page.title)
    .font(.headline)
+ Text(": ") +
Text("Seitenbeschreibung hier")
    .italic()
```

Und Sie erhalten einen Text mit verschiedenen kombinierten Stylings:

![alternativer Text](image-4.png)

### Listen

Erstellen von scrollbaren Datentabellen mit `List`, insbesondere wie sie Zeilen direkt aus Datenarrays erstellen kann.

```swift
List {
    Section {
        Label("Sonne", systemImage: "sun.max")
        Label("Wolke", systemImage: "cloud")
        Label("Regen", systemImage: "cloud.rain")
    }
}
```

Schaltflächen in Listen: Wenn Sie eine Schaltfläche in eine Liste setzen, wird das GESAMTE Listenelement anklickbar! Wenn es mehr als eine Schaltfläche in einer Liste gibt, wo auch immer Sie auf das Listenelement klicken, werden ALLE Schaltflächen nacheinander angeklickt!

Um das zu beheben und das gewünschte Verhalten zu erhalten, verwenden Sie `.buttonStyle(.plain)`

Das Gleiche gilt für HStack:

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

- Erstellen von Animationen implizit mit dem `animation()`-Modifier.
- Anpassen von Animationen mit Verzögerungen und Wiederholungen und die Wahl zwischen Ease-in-Ease-out- und Federanimationen.
- Anhängen des `animation()`-Modifiers an Bindungen, sodass wir Änderungen direkt von UI-Steuerelementen animieren können.
- Verwenden von `withAnimation()`, um explizite Animationen zu erstellen.
- Anhängen mehrerer `animation()`-Modifier an eine einzelne Ansicht, sodass wir den Animationsstapel steuern können.

### Daten laden

Wenn es synchron ist:

```swift
View...
    .onAppear(loadIt)
```

?? Wie wird es gemacht, wenn `loadIt` asynchron ist??

### Werte an Ansichten übergeben und von ihnen zurückgeben

Wie gesehen in [Auswählen und Bearbeiten von Kartenanmerkungen](https://www.hackingwithswift.com/books/ios-swiftui/selecting-and-editing-map-annotations)

Stellen Sie sich vor, ich habe eine Ansicht, die als Sheet geöffnet wird und eine `Location` (eine selbst definierte `struct`) erhält:

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

und erweitere dann den Initialisierer so:

```swift
init(location: Location, onSave: @escaping (Location) -> Void) {
    self.location = location
    self.onSave = onSave

    _name = State(initialValue: location.name)
    _description = State(initialValue: location.description)
}
```

Dieser `@escaping`-Teil ist wichtig und bedeutet, dass die Funktion für eine spätere Verwendung gespeichert wird, anstatt sofort aufgerufen zu werden, und es ist hier notwendig, weil die `onSave`-Funktion nur aufgerufen wird, wenn der Benutzer auf Speichern drückt.

### `Sheet`s & `NavigationStack`s

Um eine Ansicht als Sheet zu öffnen:

```swift
struct ContentView: View {
    @State private var showingAddExpense = false

    var body: some View {
        NavigationStack {
            VStack {
                // Hier kommt Code
            }
            .navigationTitle("iExpense")
            .toolbar {
                Button("Ausgabe hinzufügen", systemImage: "plus") {
                    showingAddExpense = true
                }
            }
            .sheet(isPresented: $showingAddExpense) {
                AddView(expenses: expenses)
            }
        }
    }
}

```

## Netzwerk

So senden Sie etwas an einen HTTPS-Endpunkt:

```swift
 func placeOrder() async {
        guard let encoded = try? JSONEncoder().encode(order) else {
            print("Bestellung konnte nicht kodiert werden")
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

## Daten speichern

Ich kenne drei Möglichkeiten, Daten in Swift/UI zu speichern:

- UserDefaults: Am besten geeignet, um kleine Datenmengen zu speichern. Zum Beispiel App-Einstellungen.
- Schreiben in das Dokumentenverzeichnis
- SwiftData

### Schreiben & Lesen in UserDefaults

Wir benötigen ein paar Dinge:

1. Unsere Daten müssen `Codable` sein, damit wir später `JSONEncoder` erstellen können
2. UserDefaults zum Speichern und Laden unserer Daten
3. Einen benutzerdefinierten Initialisierer für die Datenklasse, damit sie automatisch geladen wird
4. Ein `didSet` für die Daten, damit sie immer gespeichert werden, wenn Daten hinzugefügt oder geändert werden.

Die Daten `Codable` zu machen, ist meistens nicht allzu schwer: Solange die Komponenten `Codable` sind, ist es auch die gesamte Klasse.

So könnte das Speichern der Daten in einem `didSet` aussehen:

```swift
var items = [ExpenseItem]() {
    didSet {
        if let encoded = try? JSONEncoder().encode(items) {
            UserDefaults.standard.set(encoded, forKey: "Items")
        }
    }
}
```

Und so könnte ein Initialisierer aussehen, der die Daten lädt:

```swift
init() {
    if let savedItems = UserDefaults.standard.data(forKey: "Items") {
        if let decodedItems = try? JSONDecoder().decode([ExpenseItem].self, from: savedItems) {
            items = decodedItems
            return
        }
    }

    items = []
}
```

### Schreiben & Lesen im Dokumentenverzeichnis

So schreiben wir:

```swift
let data = Data("Testnachricht".utf8)
let url = URL.documentsDirectory.appending(path: "message.txt")

do {
    try data.write(to: url, options: [.atomic, .completeFileProtection])
} catch {
    print(error.localizedDescription)
}
```

..und so lesen wir:

```swift
let url =