---
Tags: tech
Title: Aide-mémoire SwiftUI
Date: 2025-08-03
image: swiftui.png
summary: Mon aide-mémoire, construit en suivant [100 Days of SwiftUI](https://www.hackingwithswift.com/100/swiftui/).
translation: fr
source_language: en
source_hash: 4ea71b7272600a018826a75cc835c7685e5512de376cbab0a168f774188aec16
translator: gpt-4o-2024-08-06
translate_date: 2025-08-05T08:16:27.865559
generated_by: simplified-translation-system
---

En juin 2025, j'ai commencé à suivre [100 Days of SwiftUI](https://www.hackingwithswift.com/100/swiftui/). C'est un excellent cours, et je suis vraiment impressionné par la qualité et la quantité de contenu et de cours que Paul Hudson propose - et maintient !! Paul, merci beaucoup pour cela ! 🙏🏼

Mais c'est beaucoup de contenu, alors voici mes notes - j'espère dans un format d'aide-mémoire facile à naviguer. J'ai une structure approximative en tête, mais je ne remplirai le contenu que lorsque j'en aurai besoin. Ne vous attendez donc pas à un aperçu complet !

## Swift

### Chaînes de caractères

- Elles sont spéciales, et il y a beaucoup à savoir...
- Cela ne fonctionne pas :

```swift
let name = "Paul"
let firstLetter = name[0]
```

### Optionnels

- Les optionnels nous permettent de représenter l'absence de données, ce qui signifie que nous pouvons dire « cet entier n'a pas de valeur » – c'est différent d'un nombre fixe tel que 0.
  - Exemple : `var str:String?` peut contenir une chaîne de caractères ou nil
- En conséquence, tout ce qui n'est pas optionnel a définitivement une valeur à l'intérieur, même si ce n'est qu'une chaîne vide.
- Déballer un optionnel est le processus consistant à regarder à l'intérieur d'une boîte pour voir ce qu'elle contient : s'il y a une valeur à l'intérieur, elle est renvoyée pour être utilisée, sinon il y aura nil à l'intérieur.
- Nous pouvons utiliser if let pour exécuter du code si l'optionnel a une valeur, ou guard let pour exécuter du code si l'optionnel n'a pas de valeur – mais avec guard, nous devons toujours quitter la fonction par la suite.
- L'opérateur de coalescence nil, ??, déballe et renvoie la valeur d'un optionnel, ou utilise une valeur par défaut à la place.
- Le chaînage optionnel nous permet de lire un optionnel à l'intérieur d'un autre optionnel avec une syntaxe pratique.
- Si une fonction peut générer des erreurs, vous pouvez la convertir en optionnel en utilisant try? – vous obtiendrez soit la valeur de retour de la fonction, soit nil si une erreur est générée.

### Dates

`Date`, `DateComponents`, et `DateFormatter`

## SwiftUI

- [Interactful](https://apps.apple.com/de/app/interactful/id1528095640?l=en-GB)
- [Guide d'interface humaine](https://developer.apple.com/design/human-interface-guidelines/components)

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

### Saisie de données

#### `Stepper`

![Stepper](stepper.png)
Un stepper est un contrôle à deux segments que les utilisateurs utilisent pour augmenter ou diminuer une valeur incrémentale.

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

### Bundle

Lire des fichiers depuis notre bundle d'application en recherchant leur chemin à l'aide de la classe `Bundle`, y compris le chargement de chaînes de caractères à partir de là.

### Animations

Couvert dans [Jour 32-34](https://www.hackingwithswift.com/100/swiftui/32). TODO Je dois revoir les clips pour extraire mes notes/aide-mémoire.

- Créer des animations implicitement en utilisant le modificateur `animation()`.
- Personnaliser les animations avec des délais et des répétitions, et choisir entre des animations ease-in-ease-out et des animations à ressort.
- Attacher le modificateur animation() aux liaisons, afin que nous puissions animer les changements directement depuis les contrôles de l'interface utilisateur.
- Utiliser `withAnimation()` pour créer des animations explicites.
- Attacher plusieurs modificateurs `animation()` à une seule vue afin que nous puissions contrôler la pile d'animations.

### Autres sujets

- Apprentissage automatique
- Faire planter votre code avec `fatalError()`, et pourquoi cela pourrait en fait être une bonne chose.
- Comment vérifier si une chaîne de caractères est orthographiée correctement, en utilisant `UITextChecker` (c'est une bête compliquée).
- Utiliser `DragGesture()` pour permettre à l'utilisateur de déplacer des vues, puis les ramener à leur position d'origine.
- Bundles : Comment mettre un fichier `whatever.txt` dans votre bundle, comment y accéder (c'est-à-dire le lire). Les noms de fichiers doivent être uniques dans un bundle.

## Questions

- Quelles sont les différences entre un `Form` et un `VStack` ?