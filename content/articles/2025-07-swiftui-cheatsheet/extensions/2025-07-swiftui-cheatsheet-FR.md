---
Tags: tech
Title: Aide-mémoire SwiftUI
Date: 2025-08-03
image: swiftui.png
summary: Mon aide-mémoire, créé en suivant [100 Days of SwiftUI](https://www.hackingwithswift.com/100/swiftui/).
translation: fr
source_language: en
source_hash: b2137725a3734ebc8aab07a0407f106d8a722e6d32ecc800701dbcd523ba90b7
translator: gpt-4o-2024-08-06
translate_date: 2025-08-03T08:56:12.820293
generated_by: simplified-translation-system
---

En juin 2025, j'ai commencé à suivre [100 Days of SwiftUI](https://www.hackingwithswift.com/100/swiftui/). C'est un excellent cours, et je suis vraiment impressionné par la quantité de contenu de qualité et de cours que Paul Hudson propose - et maintient !! Paul, merci beaucoup pour cela ! 🙏🏼

Mais c'est beaucoup de contenu, donc voici mes notes - j'espère dans un format d'aide-mémoire facile à naviguer. J'ai une structure approximative en tête, mais je ne remplirai le contenu que lorsque j'en aurai besoin. Ne vous attendez donc pas à un aperçu complet !

## Swift

### Optionnels

- Les optionnels nous permettent de représenter l'absence de données, ce qui signifie que nous pouvons dire "cet entier n'a pas de valeur" – c'est différent d'un nombre fixe tel que 0.
  - Exemple : `var str:String?` peut contenir une chaîne ou nil
- En conséquence, tout ce qui n'est pas optionnel a définitivement une valeur à l'intérieur, même si ce n'est qu'une chaîne vide.
- Déballer un optionnel est le processus de regarder à l'intérieur d'une boîte pour voir ce qu'elle contient : s'il y a une valeur à l'intérieur, elle est renvoyée pour être utilisée, sinon il y aura nil à l'intérieur.
- Nous pouvons utiliser if let pour exécuter du code si l'optionnel a une valeur, ou guard let pour exécuter du code si l'optionnel n'a pas de valeur – mais avec guard, nous devons toujours quitter la fonction ensuite.
- L'opérateur de coalescence nil, ??, déballe et renvoie la valeur d'un optionnel, ou utilise une valeur par défaut à la place.
- Le chaînage optionnel nous permet de lire un optionnel à l'intérieur d'un autre optionnel avec une syntaxe pratique.
- Si une fonction peut générer des erreurs, vous pouvez la convertir en optionnel en utilisant try? – vous obtiendrez soit la valeur de retour de la fonction, soit nil si une erreur est générée.

### Dates

`Date`, `DateComponents`, et `DateFormatter`

## SwiftUI

### Vues

- Tout est une vue dans SwiftUI 😜
- Exécution de code lorsqu'une vue est affichée, en utilisant `onAppear()`.

### Saisie de données

- `Stepper` pour les nombres
- `DatePicker` pour les Dates. Utilisation du paramètre `displayedComponents` pour contrôler les dates ou les heures.

### Listes

Construction de tableaux de données défilants en utilisant `List`, en particulier comment il peut créer des lignes directement à partir de tableaux de données.

### Bundle

Lecture de fichiers depuis notre bundle d'application en recherchant leur chemin à l'aide de la classe `Bundle`, y compris le chargement de chaînes de caractères à partir de là.

### Animations

Couvert dans [Jour 32-34](https://www.hackingwithswift.com/100/swiftui/32). TODO Je dois revoir les clips pour extraire mes notes/aide-mémoire.

- Création d'animations implicitement en utilisant le modificateur `animation()`.
- Personnalisation des animations avec des délais et des répétitions, et choix entre animations ease-in-ease-out et animations à ressort.
- Attachement du modificateur animation() aux liaisons, afin que nous puissions animer les changements directement depuis les contrôles de l'interface utilisateur.
- Utilisation de `withAnimation()` pour créer des animations explicites.
- Attachement de plusieurs modificateurs `animation()` à une seule vue afin que nous puissions contrôler la pile d'animations.

### Autres sujets

- Apprentissage automatique
- Faire planter votre code avec `fatalError()`, et pourquoi cela pourrait en fait être une bonne chose.
- Comment vérifier si une chaîne est orthographiée correctement, en utilisant `UITextChecker` (c'est une bête compliquée).
- Utilisation de `DragGesture()` pour permettre à l'utilisateur de déplacer les vues, puis les faire revenir à leur emplacement d'origine.