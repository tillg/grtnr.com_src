---
Tags: tech
Title: SwiftUI Cheatsheet
Date: 2025-08-03
image: swiftui.png
summary: Mon aide-mémoire, créé en suivant [100 Days of SwiftUI](https://www.hackingwithswift.com/100/swiftui/).
translation: fr
source_language: en
source_hash: 06b297ad1e3c40d5dc0c07363f90bf4f7d37817e86210dac2a17df220350ad77
translator: gpt-4o-2024-08-06
translate_date: 2025-08-17T10:27:03.141565
generated_by: simplified-translation-system
---

En juin 2025, j'ai commencé à travailler sur [100 Days of SwiftUI](https://www.hackingwithswift.com/100/swiftui/). C'est un excellent cours, et je suis vraiment impressionné par la quantité de contenu de qualité et de cours que Paul Hudson propose - et maintient !! Paul, merci beaucoup pour cela ! 🙏🏼

Mais c'est beaucoup de contenu, alors voici mes notes - j'espère dans un format d'aide-mémoire facile à naviguer. J'ai une structure générale en tête, mais je ne remplirai le contenu que lorsque j'en aurai besoin. Ne vous attendez donc pas à une vue d'ensemble complète !

[TOC]

## Swift

Pour une vue d'ensemble complète, voir [Learn essential Swift in one hour](https://www.hackingwithswift.com/articles/242/learn-essential-swift-in-one-hour).

Dans le chapitre suivant, j'ai juste ajouté les parties que j'avais besoin de vérifier au moins une fois.

### `struct` et propriétés calculées

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

- Les optionnels nous permettent de représenter l'absence de données, ce qui signifie que nous pouvons dire "cet entier n'a pas de valeur" – c'est différent d'un nombre fixe comme 0.
  - Exemple : `var str:String?` peut contenir une chaîne ou nil
- En conséquence, tout ce qui n'est pas optionnel a définitivement une valeur à l'intérieur, même si ce n'est qu'une chaîne vide.
- Déballer un optionnel est le processus consistant à regarder à l'intérieur d'une boîte pour voir ce qu'elle contient : s'il y a une valeur à l'intérieur, elle est renvoyée pour être utilisée, sinon il y aura nil à l'intérieur.
- Nous pouvons utiliser `if let` pour exécuter du code si l'optionnel a une valeur, ou `guard let` pour exécuter du code si l'optionnel n'a pas de valeur – mais avec guard, nous devons toujours quitter la fonction par la suite.

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

### Tableaux et tri

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

1. Ajouter la conformité `Comparable` à la définition de User.
2. Ajouter une méthode appelée `<` qui prend deux utilisateurs et renvoie vrai si le premier doit être trié avant le second.

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

- Elles sont spéciales, et il y a beaucoup à savoir...
- Cela ne fonctionne pas :

```swift
let name = "Paul"
let firstLetter = name[0]
```

### Dates

`Date`, `DateComponents`, et `DateFormatter`

## SwiftUI

- [Interactful](https://apps.apple.com/de/app/interactful/id1528095640?l=en-GB) est un outil pratique pour naviguer et explorer les différentes vues et composants.
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

### Saisie de données

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
-

### Listes

Construction de tableaux de données défilants en utilisant `List`, en particulier comment il peut créer des lignes directement à partir de tableaux de données.

```swift
List {
    Section {
        Label("Soleil", systemImage: "sun.max")
        Label("Nuage", systemImage: "cloud")
        Label("Pluie", systemImage: "cloud.rain")
    }
}
```

Boutons dans les listes : Lorsque vous placez un bouton dans une liste, l'ENTIÈRE élément de liste devient cliquable ! S'il y a plus d'un bouton dans une liste, où que vous cliquiez sur l'élément de liste, cela clique sur TOUS les boutons l'un après l'autre !

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

Lecture de fichiers à partir de notre bundle d'application en recherchant leur chemin à l'aide de la classe `Bundle`, y compris le chargement de chaînes à partir de là.

### Animations

Couvert dans [Jour 32-34](https://www.hackingwithswift.com/100/swiftui/32). TODO Je dois revoir les clips pour extraire mes notes/aide-mémoire.

- Création d'animations implicitement en utilisant le modificateur `animation()`.
- Personnalisation des animations avec des délais et des répétitions, et choix entre les animations ease-in-ease-out et les animations à ressort.
- Attachement du modificateur animation() aux liaisons, afin que nous puissions animer les changements directement à partir des contrôles de l'interface utilisateur.
- Utilisation de `withAnimation()` pour créer des animations explicites.
- Attachement de plusieurs modificateurs `animation()` à une seule vue afin que nous puissions contrôler la pile d'animations.

### Chargement de données

Si c'est synchrone :

```swift
View...
    .onAppear(loadIt)
```

?? Comment cela se fait-il lorsque `loadIt` est asynchrone ??

## Réseautage

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

## SwiftData

?? Quelle est la relation entre Model, ModelContext et ModelContainer ??

Créez d'abord un modèle :

```swift
@Model
class Book {  // Les modèles DOIVENT ÊTRE des classes !
    var title: String
    var author: String
    var genre: String
    var review: String
    var rating: Int
}
```

Ajoutez le `modelContainer` au niveau de l'application

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

Utilisez les données dans votre vue :

```swift
struct ContentView: View {
    @Environment(\.modelContext) var modelContext
    @Query(sort: [
        SortDescriptor(\Book.title),
        SortDescriptor(\Book.author)
    ]) var books: [Book]
    ...
```

Passez un objet SwiftData à une vue en aval :

```swift
struct DetailView: View {
    @Environment(\.modelContext) var modelContext

    let book: Book
    ...
```

Ajoutez un objet SwiftData :

```swift

struct AddBookView: View {
    @Environment(\.modelContext) var modelContext
    var body: some View {
        NavigationStack {
            Form {
                // Saisie de données ici
                Section {
                    Button("Enregistrer") {
                        let newBook = Book(title: title, author: author, genre: genre, review: review, rating: rating)
                        modelContext.insert(newBook)
                        dismiss()
                    }
                }
            }
            .navigationTitle("Ajouter un livre")
        }
    }
}
```

Supprimez un objet SwiftData :

```swift
    func deleteBook() {
        modelContext.delete(book)
        dismiss()
    }
```

Ajout d'un contexte et de données d'exemple pour `#Preview` :

```swift
#Preview {
    do {
        let config = ModelConfiguration(isStoredInMemoryOnly: true)
        let container = try ModelContainer(for: Book.self, configurations: config)
        let example = Book(title: "Test Book", author: "Test Author", genre: "Fantasy", review: "C'était un excellent livre ; je l'ai vraiment apprécié.", rating: 4)

        return DetailView(book: example)
            .modelContainer(container)
    } catch {
        return Text("Échec de la création de l'aperçu : \(error.localizedDescription)")
    }
}
```

## Autres sujets

- Apprentissage automatique
- Faire planter votre code avec `fatalError()`, et pourquoi cela pourrait en fait être une bonne chose.
- Comment vérifier si une chaîne est correctement orthographiée, en utilisant `UITextChecker` (c'est une bête compliquée).
- Utilisation de `DragGesture()` pour permettre à l'utilisateur de déplacer des vues, puis les ramener à leur position d'origine.
- Bundles : Comment mettre un fichier `whatever.txt` dans votre bundle, comment y accéder (c'est-à-dire le lire). Les noms de fichiers doivent être uniques dans tout un bundle.

## Questions et tâches

- Quelles sont les différences entre un `Form` et un `VStack` ?
- Configurations multi-écrans : `Sheet` et `NavigationStack`, et comment se déplacer
  - `NavigationStack(path)`
- Liaison : `@State`, `@Bindable`, `@Binding`
- Comment passer des données dans des configurations multi-écrans