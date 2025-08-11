---
Tags: tech
Title: Aide-mémoire SwiftUI
Date: 2025-08-03
image: swiftui.png
summary: Mon aide-mémoire, créé en suivant [100 Days of SwiftUI](https://www.hackingwithswift.com/100/swiftui/).
translation: fr
source_language: en
source_hash: b2a2fd2590a98613ee14933ee2c3d3c6b963d3e1469976664a5cc7728fb11fb0
translator: gpt-4o-2024-08-06
translate_date: 2025-08-11T11:33:21.527352
generated_by: simplified-translation-system
---

En juin 2025, j'ai commencé à suivre [100 Days of SwiftUI](https://www.hackingwithswift.com/100/swiftui/). C'est un excellent cours, et je suis vraiment impressionné par la quantité de contenu de qualité et de cours que Paul Hudson propose - et maintient !! Paul, merci beaucoup pour cela ! 🙏🏼

Mais c'est beaucoup de contenu, alors voici mes notes - j'espère dans un format d'aide-mémoire facile à naviguer. J'ai une structure approximative en tête, mais je ne remplirai le contenu que lorsque j'en aurai besoin. Ne vous attendez donc pas à un aperçu complet !

[TOC]

## Swift

### Optionnels

- Les optionnels nous permettent de représenter l'absence de données, ce qui signifie que nous pouvons dire "cet entier n'a pas de valeur" – c'est différent d'un nombre fixe tel que 0.
  - Exemple : `var str:String?` peut contenir une chaîne ou nil
- En conséquence, tout ce qui n'est pas optionnel a définitivement une valeur à l'intérieur, même si ce n'est qu'une chaîne vide.
- Déballer un optionnel est le processus de regarder à l'intérieur d'une boîte pour voir ce qu'elle contient : s'il y a une valeur à l'intérieur, elle est renvoyée pour être utilisée, sinon il y aura nil à l'intérieur.
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

- [Interactful](https://apps.apple.com/de/app/interactful/id1528095640?l=en-GB)
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

`ForEach` est une vue, qui est composée des sous-vues créées à chaque instance de boucle.

Nous l'utilisons généralement pour créer des sous-vues basées sur un compteur ou un tableau.

`ForEach` avec un tableau :

```swift
import SwiftUI

struct ContentView: View {
  let items = ["Pomme", "Banane", "Cerise"]

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

Construire des tableaux de données défilants en utilisant `List`, en particulier comment il peut créer des lignes directement à partir de tableaux de données.

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

Lire des fichiers depuis notre bundle d'application en recherchant leur chemin en utilisant la classe `Bundle`, y compris le chargement de chaînes depuis celui-ci.

### Animations

Couvert dans [Jour 32-34](https://www.hackingwithswift.com/100/swiftui/32). TODO Je dois revoir les clips pour extraire mes notes/aide-mémoire.

- Créer des animations implicitement en utilisant le modificateur `animation()`.
- Personnaliser les animations avec des délais et des répétitions, et choisir entre des animations ease-in-ease-out et des animations à ressort.
- Attacher le modificateur animation() à des liaisons, afin que nous puissions animer les changements directement depuis les contrôles de l'interface utilisateur.
- Utiliser `withAnimation()` pour créer des animations explicites.
- Attacher plusieurs modificateurs `animation()` à une seule vue afin que nous puissions contrôler la pile d'animations.

### Autres sujets

- Apprentissage automatique
- Faire planter votre code avec `fatalError()`, et pourquoi cela pourrait en fait être une bonne chose.
- Comment vérifier si une chaîne est orthographiée correctement, en utilisant `UITextChecker` (c'est une bête compliquée).
- Utiliser `DragGesture()` pour permettre à l'utilisateur de déplacer des vues, puis les faire revenir à leur emplacement d'origine.
- Bundles : Comment mettre un fichier `whatever.txt` dans votre bundle, comment y accéder (c'est-à-dire le lire). Les noms de fichiers doivent être uniques dans tout un bundle.

## Questions

- Quelles sont les différences entre un `Form` et un `VStack` ?