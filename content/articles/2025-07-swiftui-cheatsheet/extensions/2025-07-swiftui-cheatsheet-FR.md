---
Tags: tech
Title: SwiftUI Cheatsheet
Date: 2025-08-03
image: swiftui.png
summary: Mon aide-mémoire, construit en suivant [100 Days of SwiftUI](https://www.hackingwithswift.com/100/swiftui/).
title: SwiftUI&nbsp;Cheatsheet
translation: fr
source_language: en
source_hash: af1e5f2c544add545bc814587612c9166d16e28b95a8d8835bbab8ec89b2887d
translator: gpt-4o-2024-08-06
translate_date: 2026-02-14T10:52:19.473376
generated_by: simplified-translation-system
---

En juin 2025, j'ai commencé à travailler à travers [100 Days of SwiftUI](https://www.hackingwithswift.com/100/swiftui/). C'est un excellent cours, et je suis vraiment impressionné par la qualité du contenu et des cours que Paul Hudson fournit - et maintient !! Paul, merci beaucoup pour cela ! 🙏🏼

Mais c'est beaucoup de contenu, alors voici mes notes - j'espère dans un format d'aide-mémoire facile à naviguer. J'ai une structure générale en tête, mais je ne remplirai le contenu que lorsque j'en aurai besoin. Ne vous attendez donc pas à une vue d'ensemble complète !

[TOC]

## Swift

Pour une vue d'ensemble complète, voir [Learn essential Swift in one hour](https://www.hackingwithswift.com/articles/242/learn-essential-swift-in-one-hour).

Dans le chapitre suivant, j'ai juste ajouté les parties que j'avais besoin de vérifier au moins une fois.

### `struct` & propriétés calculées

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

### Optionnels

- Les optionnels nous permettent de représenter l'absence de données, ce qui signifie que nous pouvons dire "cet entier n'a pas de valeur" – c'est différent d'un nombre fixe tel que 0.
  - Exemple : `var str:String?` peut contenir une chaîne ou nil
- En conséquence, tout ce qui n'est pas optionnel a définitivement une valeur à l'intérieur, même si ce n'est qu'une chaîne vide.
- Déballer un optionnel est le processus de regarder à l'intérieur d'une boîte pour voir ce qu'elle contient : s'il y a une valeur à l'intérieur, elle est renvoyée pour être utilisée, sinon il y aura nil à l'intérieur.
- Nous pouvons utiliser `if let` pour exécuter du code si l'optionnel a une valeur, ou `guard let` pour exécuter du code si l'optionnel n'a pas de valeur – mais avec guard, nous devons toujours quitter la fonction ensuite.

```swift
func printSquare(of number: Int?) {
    guard let number = number else {
        print("Entrée manquante")
        return
    }

    print("\(number) x \(number) est \(number * number)")
}
```

- L'opérateur de coalescence nil, ??, déballe et renvoie la valeur d'un optionnel, ou utilise une valeur par défaut à la place.

```swift
let new = captains["Serenity"] ?? "N/A"
```

- Le chaînage optionnel nous permet de lire un optionnel à l'intérieur d'un autre optionnel avec une syntaxe pratique.
- Si une fonction peut générer des erreurs, vous pouvez la convertir en optionnel en utilisant try? – vous obtiendrez soit la valeur de retour de la fonction, soit nil si une erreur est générée.

### Protocoles et Extensions

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

### Tableaux & tri

Tous les tableaux ont des méthodes intégrées `sort()` et `sorted()` qui peuvent être utilisées pour trier le tableau.

- `sort()` trie le tableau sur place
- `sorted()` renvoie un nouveau tableau trié.

Si le tableau est simple, vous pouvez simplement appeler `sort()` directement, comme ceci, pour trier un tableau sur place :

```swift
var names = ["Jemima", "Peter", "David", "Kelly", "Isabella"]
names.sort()
```

Si vous avez des structures plus complexes, vous devez passer la comparaison :

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

Nous pouvons faire en sorte que nos propres types soient conformes à `Comparable`, et lorsque nous le faisons, nous obtenons également une méthode `sorted()` sans paramètres. Cela prend deux étapes :

1. Ajoutez la conformité `Comparable` à la définition de User.
2. Ajoutez une méthode appelée `<` qui prend deux utilisateurs et renvoie true si le premier doit être trié avant le second.

Voici à quoi cela ressemble en code :

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

### Chaînes

- Elles sont spéciales et il y a beaucoup à savoir...
- Cela ne fonctionne pas :

```swift
let name = "Paul"
let firstLetter = name[0]
```

### Dates

`Date`, `DateComponents`, et `DateFormatter`

### `enum`

Les `enum` sont créés comme ceci :

```swift
enum Weekday {
    case monday, tuesday, wednesday, thursday, friday
}
```

Une instruction `switch` avec `enum` ressemble à ceci :

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

- [Interactful](https://apps.apple.com/de/app/interactful/id1528095640?l=en-GB) est un outil sympa pour naviguer et explorer les différentes vues et composants.
- [Human Interfaces Guideline](https://developer.apple.com/design/human-interface-guidelines/components)

### Vues

- Tout est une vue dans SwiftUI 😜
- Exécuter du code lorsqu'une vue est affichée, en utilisant `onAppear()`.

Même `ForEach` est une vue, c'est pourquoi nous pouvons écrire

```swift
ForEach(0..<5) {
    Text("Ligne \($0)")
}
```

Remarque : Nous ne pouvons pas écrire `ForEach(0..<5)`, car `ForEach` attend un `Range<Int>`, pas un `ClosedRange<Int>` !

#### Vue `ForEach`

`ForEach` est une vue, composée des sous-vues créées à chaque instance de boucle.

Nous l'utilisons généralement pour créer des sous-vues basées sur un compteur ou un tableau.

`ForEach` avec un tableau :

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

### Entrée de données

#### `TextField`

#### `Picker`

`Picker` est utilisé pour choisir une option parmi plusieurs sélections possibles.

Un sélecteur régulier ressemble à ceci :

```swift
Picker("Nombre de personnes", selection: $numberOfPeople) {
    ForEach(2 ..< 100 , id: \.self) {
        Text("\($0) personnes")
    }
}
```

![texte alternatif](image-7.png)

Un `Picker` peut être modifié avec le modificateur `PickerStyle` :

```swift
Picker("Pourcentage de pourboire", selection: $tipPercentage) {
    ForEach(tipPercentages, id: \.self) {
        Text($0, format: .percent)
    }
}
.pickerStyle(.segmented)
```

![texte alternatif](image-8.png)

#### `Stepper`

![Stepper](stepper.png)
Un stepper est un contrôle à deux segments que les gens utilisent pour augmenter ou diminuer une valeur incrémentale.

```swift
@State private var count: Int = 0

var body: some View {
    Stepper("\(count)",
        value: $count,
        in: 0...100
    )
}
```

- `DatePicker` pour les dates. Utilisation du paramètre `displayedComponents` pour contrôler les dates ou les heures.
- `Form`
- `Picker`
- Barre de navigation

### Alertes et Dialogues de Confirmation

#### Alertes

Les alertes sont une extension d'une vue avec une variable Booléenne qui décide si elles sont affichées ou non.

```swift
struct ContentView: View {
    @State private var showingAlert = false

    var body: some View {
        Button("Afficher l'alerte") {
            showingAlert = true
        }
        .alert("Message important", isPresented: $showingAlert) {
            Button("OK") { }
        }
    }
}
```

#### Dialogues de Confirmation

Utilisez-les lorsque de nombreux boutons/options sont disponibles. Pour un exemple de code, consultez [ce dépôt](https://github.com/tillg/100DaysOfSwiftUI/blob/main/16.5-AlertAndConfirmation/AlertAndConfirmation/AlertAndConfirmation/ContentView.swift).

**Remarque** : Avant iOS 26, ils glissaient depuis le bas, dans iOS 26, ils apparaissent à l'intérieur de l'écran.

Dialogue de Confirmation dans iOS 18.5 :
![texte alternatif](image-6.png)

Dialogue de Confirmation dans iOS 26 :
![texte alternatif](image-5.png)

### Texte

`Text` est un champ de texte qui décrit du texte.

Remarque : Les champs de texte avec un style différent peuvent être _additionnés_ pour former un grand champ de texte avec des parties de style différent à l'intérieur :

```swift
Text(page.title)
    .font(.headline)
+ Text(": ") +
Text("Description de la page ici")
    .italic()
```

Et vous obtenez un texte avec différents styles combinés :

![texte alternatif](image-4.png)

### Listes

Construire des tables de données défilantes en utilisant `List`, en particulier comment elle peut créer des lignes directement à partir de tableaux de données.

```swift
List {
    Section {
        Label("Soleil", systemImage: "sun.max")
        Label("Nuage", systemImage: "cloud")
        Label("Pluie", systemImage: "cloud.rain")
    }
}
```

Boutons dans les listes : Lorsque vous placez un bouton dans une liste, TOUT l'élément de la liste devient cliquable ! S'il y a plus d'un bouton dans une liste, où que vous cliquiez sur l'élément de la liste, cela clique sur TOUS les boutons les uns après les autres !

Pour corriger cela et obtenir le comportement souhaité, utilisez `.buttonStyle(.plain)`

Il en va de même pour HStack :

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

### Images

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

![texte alternatif](image.png)

Remplacez `ScaledToFit` par `ScaledToFill` et obtenez

![texte alternatif](image-1.png)

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

![texte alternatif](image-2.png)

### Barre d'outils

### Bundle

Lire des fichiers depuis notre bundle d'application en recherchant leur chemin en utilisant la classe `Bundle`, y compris le chargement de chaînes à partir de là.

### Animations

Couvert dans [Jour 32-34](https://www.hackingwithswift.com/100/swiftui/32). TODO Je dois revoir les clips pour extraire mes notes/aide-mémoire.

- Créer des animations implicitement en utilisant le modificateur `animation()`.
- Personnaliser les animations avec des délais et des répétitions, et choisir entre des animations ease-in-ease-out et spring.
- Attacher le modificateur animation() aux liaisons, afin que nous puissions animer les changements directement depuis les contrôles UI.
- Utiliser `withAnimation()` pour créer des animations explicites.
- Attacher plusieurs modificateurs `animation()` à une seule vue afin que nous puissions contrôler la pile d'animations.

### Chargement des Données

Si c'est synchrone :

```swift
View...
    .onAppear(loadIt)
```

?? Comment est-ce fait, lorsque `loadIt` est asynchrone ??

### Passer et retourner des valeurs vers/depuis des vues

Comme vu dans [Sélection et édition des annotations de carte](https://www.hackingwithswift.com/books/ios-swiftui/selecting-and-editing-map-annotations)

Imaginez que j'ai une vue qui est ouverte en tant que feuille et reçoit un `Location` (étant une `struct` définie par l'utilisateur) :

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
                    TextField("Nom du lieu", text: $name)
                    TextField("Description", text: $description)
                }
            }
            .navigationTitle("Détails du lieu")
            .toolbar {
                Button("Enregistrer") {
                    dismiss()
                }
            }
        }
    }
}
```

Pour passer le `Location`, je fais un initialiseur supplémentaire :

```swift
init(location: Location) {
    self.location = location

    _name = State(initialValue: location.name)
    _description = State(initialValue: location.description)
}
```

Pour _retourner_ des données au code appelant, je passe une méthode `onSave`. Créez d'abord une variable supplémentaire dans ma structure de vue :

```swift
var onSave: (Location) -> Void
```

puis étendez l'initialiseur comme suit :

```swift
init(location: Location, onSave: @escaping (Location) -> Void) {
    self.location = location
    self.onSave = onSave

    _name = State(initialValue: location.name)
    _description = State(initialValue: location.description)
}
```

Cette partie `@escaping` est importante et signifie que la fonction est mise de côté pour une utilisation ultérieure, plutôt que d'être appelée immédiatement, et elle est nécessaire ici car la fonction `onSave` sera appelée uniquement lorsque l'utilisateur appuie sur Enregistrer.

### `Sheet`s et `NavigationStack`s

Pour ouvrir une vue en tant que feuille :

```swift
struct ContentView: View {
    @State private var showingAddExpense = false

    var body: some View {
        NavigationStack {
            VStack {
                // Du code ici
            }
            .navigationTitle("iExpense")
            .toolbar {
                Button("Ajouter une dépense", systemImage: "plus") {
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

## Réseau

Voici comment vous envoyez quelque chose à un point de terminaison HTTPS :

```swift
 func placeOrder() async {
        guard let encoded = try? JSONEncoder().encode(order) else {
            print("Échec de l'encodage de la commande")
            return
        }

        let url = URL(string: "https://reqres.in/api/cupcakes")!
        var request = URLRequest(url: url)
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.httpMethod = "POST"

        do {
            let (data, other) = try await URLSession.shared.upload(for: request, from: encoded)

            let decodedOrder = try JSONDecoder().decode(Order.self, from: data)
            confirmationMessage = "Votre commande de \(decodedOrder.quantity)x cupcakes \(Order.types[decodedOrder.type].lowercased()) est en route !"
            showingConfirmation = true
        } catch {
            print("Échec de la commande : \(error.localizedDescription)")
        }
    }
```

## Sauvegarde des Données

Je connais 3 façons de sauvegarder des données dans Swift/UI :

- UserDefaults : Mieux utilisé pour sauvegarder de petites quantités de données. Par exemple, les paramètres de l'application.
- Écriture dans le répertoire des documents
- SwiftData

### Écriture et lecture dans UserDefaults

Nous avons besoin de quelques éléments :

1. Nos données doivent être `Codable`, afin que nous puissions créer `JSONEncoder` plus tard
2. UserDefaults pour sauvegarder et charger nos données
3. Un initialiseur personnalisé pour la classe de données, afin qu'elle charge automatiquement
4. Un `didSet` pour les données, afin que chaque fois que des données sont ajoutées ou modifiées, elles soient automatiquement sauvegardées.

Rendre les données `Codable` n'est souvent pas trop difficile : Tant que les composants sont `Codable`, toute la classe l'est aussi.

Voici à quoi peut ressembler la sauvegarde des données dans un `didSet` :

```swift
var items = [ExpenseItem]() {
    didSet {
        if let encoded = try? JSONEncoder().encode(items) {
            UserDefaults.standard.set(encoded, forKey: "Items")
        }
    }
}
```

Et voici à quoi pourrait ressembler un initialiseur qui charge les données :

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

### Écriture et lecture dans le répertoire des documents

Voici comment nous écrivons :

```swift
let data = Data("Message de test".utf8)
let url = URL.documentsDirectory.appending(path: "message.txt")

do {
    try data.write(to: url, options: [.atomic, .completeFileProtection])
}