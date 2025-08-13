---
Tags: tech
Title: Aide-mémoire SwiftUI
Date: 2025-08-03
image: swiftui.png
summary: Mon aide-mémoire, créé en suivant [100 Days of SwiftUI](https://www.hackingwithswift.com/100/swiftui/).
translation: fr
source_language: en
source_hash: 6eef7758d78403186edcaf2dad6921fdb12a1642e62e25ca022e92067b2c8a39
translator: gpt-4o-2024-08-06
translate_date: 2025-08-12T09:04:35.057796
generated_by: simplified-translation-system
---

En juin 2025, j'ai commencé à suivre [100 Days of SwiftUI](https://www.hackingwithswift.com/100/swiftui/). C'est un excellent cours, et je suis vraiment impressionné par la quantité de contenu de qualité et de cours que Paul Hudson propose - et maintient !! Paul, merci beaucoup pour cela ! 🙏🏼

Mais c'est beaucoup de contenu, alors voici mes notes - j'espère dans un format d'aide-mémoire facile à naviguer. J'ai une structure approximative en tête, mais je ne remplirai le contenu que lorsque j'en aurai besoin. Ne vous attendez donc pas à un aperçu complet !

[TOC]

## Swift

Pour un aperçu complet, voir [Apprenez l'essentiel de Swift en une heure](https://www.hackingwithswift.com/articles/242/learn-essential-swift-in-one-hour).

Dans le chapitre suivant, j'ai juste ajouté les parties que j'avais besoin de vérifier au moins une fois.

### Optionnels

- Les optionnels nous permettent de représenter l'absence de données, ce qui signifie que nous pouvons dire "cet entier n'a pas de valeur" – c'est différent d'un nombre fixe tel que 0.
  - Exemple : `var str:String?` peut contenir une chaîne ou nil
- En conséquence, tout ce qui n'est pas optionnel a définitivement une valeur à l'intérieur, même si ce n'est qu'une chaîne vide.
- Déballer un optionnel est le processus consistant à regarder à l'intérieur d'une boîte pour voir ce qu'elle contient : s'il y a une valeur à l'intérieur, elle est renvoyée pour être utilisée, sinon il y aura nil à l'intérieur.
- Nous pouvons utiliser if let pour exécuter du code si l'optionnel a une valeur, ou guard let pour exécuter du code si l'optionnel n'a pas de valeur – mais avec guard, nous devons toujours quitter la fonction ensuite.
- L'opérateur de coalescence de nil, ??, déballe et renvoie la valeur d'un optionnel, ou utilise une valeur par défaut à la place.
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

Si vous avez des structures plus complexes, vous devez transmettre la comparaison :

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

- [Interactful](https://apps.apple.com/de/app/interactful/id1528095640?l=en-GB) est un outil sympa pour naviguer et jouer avec les différentes vues et composants.
- [Human Interfaces Guideline](https://developer.apple.com/design/human-interface-guidelines/components)

### Vues

- Tout est une vue dans SwiftUI 😜
- Exécuter du code lorsqu'une vue est affichée, en utilisant `onAppear()`.

Même `ForEach` est une vue, c'est pourquoi nous pouvons écrire

```swift
ForEach(0..<5) {
    Text("Row \($0)")
}
```

Remarque : Nous ne pouvons pas écrire `ForEach(0..<5)`, car `ForEach` attend un `Range<Int>`, pas un `ClosedRange<Int>` !

#### Vue `ForEach`

`ForEach` est une vue, qui est composée des sous-vues créées à chaque instance de boucle.

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

Construction de tableaux de données défilants en utilisant `List`, en particulier comment elle peut créer des lignes directement à partir de tableaux de données.

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
- Personnalisation des animations avec des délais et des répétitions, et choix entre les animations ease-in-ease-out et spring.
- Attachement du modificateur animation() aux liaisons, afin que nous puissions animer les changements directement à partir des contrôles de l'interface utilisateur.
- Utilisation de `withAnimation()` pour créer des animations explicites.
- Attachement de plusieurs modificateurs `animation()` à une seule vue afin que nous puissions contrôler la pile d'animations.

### Autres sujets

- Apprentissage automatique
- Faire planter votre code avec `fatalError()`, et pourquoi cela pourrait en fait être une bonne chose.
- Comment vérifier si une chaîne est orthographiée correctement, en utilisant `UITextChecker` (c'est une bête compliquée).
- Utilisation de `DragGesture()` pour permettre à l'utilisateur de déplacer des vues, puis les faire revenir à leur position d'origine.
- Bundles : Comment mettre un fichier `whatever.txt` dans votre bundle, comment y accéder (c'est-à-dire le lire). Les noms de fichiers doivent être uniques dans un bundle.

## Questions

- Quelles sont les différences entre un `Form` et un `VStack` ?