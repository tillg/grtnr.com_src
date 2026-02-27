---
date: 2025-09-30
image: embedding.png
excerpt: Apple a introduit de nouveaux modèles d'intégration que je souhaite utiliser pour mesurer la proximité des textes. Voici mon parcours sur comment les créer et les rendre efficaces.
title: Intégrations en Swift sur Apple Silicon
tags: tech
translation: fr
source_language: en
source_hash: 99f94cce4e66af838911fcc4b2ab79dc8fc884f1793594d7b959118b261bcd38
translator: gpt-4o-2024-08-06
translate_date: 2026-02-27T10:30:06.182744+00:00
generated_by: simplified-translation-system
---

**Travail en cours !!**

Je suis en train d'apprendre le langage de programmation Swift. Je le fais en suivant le cours fantastique [100 Days of SwiftUI](https://www.hackingwithswift.com/100/swiftui/) de Paul Hudson. C'est un cours formidable, qui couvre d'abord les bases de Swift puis SwiftUI.

Lorsque j'essaie d'appliquer mon apprentissage à de petits projets, j'ai toujours beaucoup de questions qui surgissent, et la source la plus fiable pour chercher des réponses est le cours, c'est-à-dire ses pages. Donc, je dois faire des recherches sur le site de Paul Hudson, plus précisément dans les pages de son cours.

Comme je m'amuse aussi avec l'apprentissage automatique, j'ai prévu de créer une application que j'appellerais **AskPaul** : entrez votre question et obtenez des réponses construites par un système RAG (local !) : un système qui contient toutes les pages du cours, en Markdown, découpées et indexées avec leurs intégrations. Ensuite, recherchez les morceaux pertinents pour la question posée et passez-les au LLM avec la question. Et quand je dis LLM, je parle du LLM local sur votre appareil Apple 😜

Pour expérimenter avec les intégrations Swift, j'ai mis en place un dépôt [SwiftEmbeddings](https://github.com/tillg/SwiftEmbeddings). Il contient mon code et des [Playgrounds](https://github.com/tillg/SwiftEmbeddings/tree/main/SwiftEmbeddings/SwiftEmbeddings/Playgrounds).

## Ce qui doit être fait

Voici ce que je veux accomplir :

Étant donné un ensemble de pages web disponibles en Markdown, les découper en portions de taille pratique et créer leurs intégrations : un vecteur (c'est-à-dire une série de 512 valeurs Double) qui _représente leur contenu_ d'une manière mathématique.

Étant donné une question (pensez à quelque chose comme `En Swift, comment puis-je étendre un protocole ?`), le système devrait trouver les morceaux avec un contenu pertinent en calculant le vecteur d'intégration de cette question, puis le comparer à tous les vecteurs des morceaux pour trouver le plus proche. Ces morceaux sont ensuite passés au LLM avec la question.

Dans l'ancien système d'intégration d'Apple situé dans le [cadre Natural Language](https://developer.apple.com/documentation/NaturalLanguage), les fonctions pour y parvenir sont facilement accessibles et très bien expliquées dans l'article [Trouver des similitudes entre des morceaux de texte](https://developer.apple.com/documentation/naturallanguage/finding-similarities-between-pieces-of-text).

## Le problème

Mais il y a un nouveau venu : [NLContextualEmbedding](https://developer.apple.com/documentation/naturallanguage/nlcontextualembedding). Il a été introduit dans iOS 17/macOS 14 et étendu dans iOS 18/macOS 15.

Voici pourquoi je veux utiliser le nouveau `NLContextualEmbedding` :

- Capture le contexte : Il ferait la différence entre « river bank » et « investment bank ». L'ancien `NLEmbedding` ne faisait pas cette différence.
- Est multilingue et interlingue : En s'entraînant sur plusieurs langues simultanément, le modèle aligne les espaces sémantiques entre les langues, de sorte que « chien » et « dog » sont intégrés à proximité.
- Prend en charge plus de langues
- Fonctionne entièrement sur l'appareil : Le modèle respecte la confidentialité de l'utilisateur et fonctionne hors ligne. Seuls de petits fichiers de modèle sont téléchargés lorsque nécessaire, et ceux-ci sont mis en cache à l'échelle du système.
- Offre des contrôles d'API robustes : Les développeurs peuvent inspecter les propriétés du modèle, gérer les actifs et intégrer les intégrations dans leurs propres pipelines ML.

Ce qui manque, ce sont

- l'équivalent de `NLEmbedding`'s `vector(for:)` : Obtenir un vecteur pour une phrase ou un morceau
- l'équivalent de `distanceBetweenString:andString:distanceType:` : Obtenir une mesure de la distance entre 2 phrases.

Ce que `NLContextualEmbedding` fournit est une fonction `embeddingResult(for: String, language: NLLanguage?) throws -> NLContextualEmbeddingResult`. Mais si vous regardez dans la structure du `NLContextualEmbeddingResult`, vous voyez qu'il crée un vecteur pour chaque jeton, donc un vecteur de vecteurs. De plus, ces vecteurs sont accessibles avec un itérateur : `enumerateTokenVectors(in: Range<String.Index>, using: ([Double], Range<String.Index>) -> Bool)` - ce qui m'a demandé un peu de réflexion et d'apprentissage...

J'ai donc décidé de créer un outil simple à utiliser basé sur le nouveau `NLContextualEmbedding`, similaire à ce que nous avons dans `NLEmbedding`.

Notez qu'un aspect crucial est la performance, car pour trouver les meilleurs morceaux / vecteurs correspondants dans un ensemble plus large, il faut de nombreuses comparaisons - et mes premières tentatives ont pris de nombreuses minutes pour rechercher...

## Données de test

Comme j'ai commencé avec l'idée de construire un système RAG sur l'appareil pour le cours SwiftUI de Paul Hudson, voici ce que j'ai fait :

- Récupérer les pages principales du cours SwiftUI en Markdown
- Les découper
- Les écrire toutes dans un fichier JSON que je peux copier dans mon projet Swift

Pour ce faire, j'ai assemblé quelques scripts dans [site2chunks](https://github.com/tillg/site2chunks). Un exemple de JSON est dans mon projet AskPaul : [merged_chunks](https://github.com/tillg/SwiftEmbeddings/blob/main/SwiftEmbeddings/SwiftEmbeddings/merged_chunks.json)

Sur cette base, j'ai dans mon code Swift

- Une `struct Chunk`. Si vous êtes curieux, allez voir le [code](https://github.com/tillg/AskPaul/blob/main/AskPaul/AskPaul/Chunk.swift) qui représente un morceau
- Une `Extension de Bundle` qui lit les morceaux à partir du fichier JSON ([Code]()). Note : Cela est bien sûr inspiré du [cours de Paul Hudson](https://www.hackingwithswift.com/example-code/system/how-to-decode-json-from-your-app-bundle-the-easy-way) 😜

**Note** : Je commence juste avec les _pages principales_ : la page d'entrée de chacune des 100 leçons. Je fais cela pour que l'ensemble de données soit facile à manipuler et que mes expériences soient rapides à exécuter. Ces 100 pages sont découpées en 722 morceaux. Une fois que j'aurai terminé les expériences, j'augmenterai l'ensemble de données à toutes les pages de hackingwithswift.com.

## Le point de départ : `NLEmbedding`

Avec ces données de test en place, jouons avec l'ancien `NLEmbedding`. Vous pouvez consulter le code dans [Playgrounds/01-NLEmbedding.swift](https://github.com/tillg/SwiftEmbeddings/blob/main/SwiftEmbeddings/SwiftEmbeddings/Playgrounds/01-NLEmbedding.swift)

La structure générale du code ressemble à ceci :

```swift
#Playground("Basic embedding & distance")
{
    let question = "What is a protocol?"
    let potentialAnswer = """
    A protocol defines a blueprint of methods, properties, ... blabla
    """
    guard let sentenceEmbedding = NLEmbedding.sentenceEmbedding(for: .english) else {
        fatalError("Cannot create Embedding")
    }
    guard let vector = sentenceEmbedding.vector(for: question) else {
        fatalError("Cannot create vector")
    }
    let distance = sentenceEmbedding.distance(between: question, and: potentialAnswer)
    print("Distance: \(distance.description)")
}

```

Voici de quoi parle ce code :

- Nous initialisons nos variables `question` et `potentialAnswer`
- Nous créons notre objet `NLEmbedding` - qui pourrait (théoriquement) échouer. Si c'est le cas, il n'y a rien que nous puissions faire à part tout échouer.
- Ensuite, nous calculons la [distance](<https://developer.apple.com/documentation/naturallanguage/nlembedding/distance(between:and:distancetype:)>) entre la question et l'imprimons.

Ensuite, voyons combien de temps il faut pour calculer les vecteurs d'intégration pour les 722 morceaux de nos données de test. Sur mon MacBook Pro, cela prend 35'966 ms ~ 35 secondes ou ~ 49 ms / Vecteur.

L'autre test consiste à calculer les distances entre paires de phrases :

```swift
let distance = sentenceEmbedding.distance(between: chunk1.content, and: chunk2.content)
```

Comme prévu, cela prend environ deux fois plus de temps, car pour chaque calcul de distance, 2 vecteurs d'intégration doivent être calculés : `⏱️ [Calculating distances with NLEmbedding] count=1  total=72.558420s  avg=72.558420s`

Notez que si je fais tourner la boucle en calculant toujours la distance par rapport au même texte, cela prend presque exactement le même temps que de calculer un seul vecteur. En d'autres termes, cette boucle :

```swift
for chunk in chunks {
    let distance = sentenceEmbedding.distance(between: chunk.content, and: "This is a simple text")
}
```

prend environ 36 secondes. Cela indiquerait que le calcul de la distance entre 2 vecteurs prend très peu de temps...

La dernière chose que je voudrais faire est d'obtenir les `k` morceaux les plus proches d'une question donnée. Ma façon de faire cela est de trier le tableau de morceaux par leur distance à notre question :

```swift
func findClosest<T: Embeddable>(to question: String, in chunks: [T], k: Int = 3) -> [T] {
        guard let sentenceEmbedding = NLEmbedding.sentenceEmbedding(for: .english) else {
            // Fallback if embedding is unavailable
            return Array(chunks.prefix(k))
        }
        let sorted = chunks.sorted { lhs, rhs in
            let dl = sentenceEmbedding.distance(between: question, and: lhs.content)
            let dr = sentenceEmbedding.distance(between: question, and: rhs.content)
            return dl < dr
        }
        return Array(sorted.prefix(k))
    }
```

Trouver les morceaux les plus proches d'une question donnée (ce qui équivaut à trier le tableau) prend assez longtemps : 1'554'280 ms ~ 1'554 sec ~ 25 MINUTES

Notez que nous avons besoin de 11'290 comparaisons. Comme je suppose qu'Apple met en cache le vecteur de la phrase unique utilisée dans chaque comparaison, cela signifie qu'il a utilisé le temps pour 11'290 x (calculer le vecteur + calculer la distance des vecteurs). Étonnamment, cela fait ~ 137ms / (calcul du vecteur + calcul de la distance)...

Une tentative de mettre nos résultats dans un aperçu :

| Ensemble de données : 722 morceaux | Calculer vecteurs | Calculer distances | Trier tableau | ms / Vecteur |
| ---------------------------------- | ----------------- | ------------------ | ------------- | ------------ |
| NLEmbedding                        | 35 sec            | 70 sec             | 1'554 sec     | 49 ms        |

## Mesurer le temps

Comme nous allons mesurer beaucoup de temps de traitement consommé par nos calculs, j'ai construit un petit système de suivi du temps. Voici comment l'appeler :

```swift
timerTrack("Nom du minuteur") {
    // Du code que je veux chronométrer ici
}
timerReport("Nom du minuteur") // Imprime les statistiques de mon minuteur
```

Mon `timerTrack` retourne également le résultat de son bloc et fonctionne de manière asynchrone. Nous pouvons donc faire des choses comme ceci :

```swift
let result = try timerTrack("Embedding") {
    try embeddingResult(for: sentence, language: language)
}
```

## Calculer un vecteur d'intégration basé sur `NLContextualEmbedding` de manière naïve

Maintenant, si nous essayons de faire quelque chose de similaire en utilisant `NLContextualEmbedding`, nous devons d'abord faire un peu de codage de base : l'intégration contextuelle d'Apple génère une liste de vecteurs, spécifiquement un par jeton.

Nous devons donc les compiler en un seul vecteur. Une méthode standard pour y parvenir est le regroupement de vecteurs :

[La méthode la plus courante est le regroupement moyen, où les intégrations de tous les jetons (à l'exclusion du remplissage) sont moyennées.](https://milvus.io/ai-quick-reference/how-do-sentence-transformers-create-fixedlength-sentence-embeddings-from-transformer-models-like-bert-or-roberta)

Imaginez que vous avez 2 vecteurs tridimensionnels `v1` et `v2`, et que vous voulez calculer leur vecteur moyen `v3` :

```swift
v3.x = (v1.x + v2.x) / 2;
v3.y = (v1.y + v2.y) / 2;
v3.z = (v1.z + v2.z) / 2;
```

Ce serait une boucle facile à travers les dimensions, et pour chaque dimension, calculer la moyenne de tous les composants des vecteurs. Maintenant, nous faisons face à une petite technicité : `NLContextualEmbedding` nous livre les vecteurs, enveloppés dans un `NLContextualEmbeddingResult`. Si vous consultez les [docs](https://developer.apple.com/documentation/naturallanguage/nlcontextualembeddingresult), voici ce qu'ils disent :

```swift
func enumerateTokenVectors(in: Range<String.Index>, using: ([Double], Range<String.Index>) -> Bool)
# Itère sur les vecteurs d'intégration pour la plage que vous spécifiez.
```

Il m'a fallu un certain temps pour digérer cela, mais voici ce à quoi cela se résume :

Vous lui donnez un `Range<String.Index>` pour indiquer d'où à où vous voulez que les vecteurs soient listés. Pourquoi n'ont-ils pas simplement utilisé quelque chose comme `0...10` ? Le secret est que le `Range<String.Index>` ne parcourt pas le texte comme `T`, `h`, `ì`, `s`, `_`, `i`, `s`... mais à travers les **jetons**.

Voyons à quoi ressemblent réellement les jetons :

```swift
result.enumerateTokenVectors(in: result.string.startIndex..<result.string.endIndex) { vector, range in
    let token = result.string[range]
    print("Vector for token [\(token)]")
    return true // Return true to keep enumerating, false to stop early
}
```

Voici ce que nous obtenons :

```text
Vector for token []
Vector for token []
Vector for token [This]
Vector for token [is]
Vector for token [a]
Vector for token [sentenc]
Vector for token [e]
Vector for token [.]
```

En voyant cela, il est logique que l'index ne se contente pas de compter de 1 à `string.count`, mais soit un peu plus complexe.

Vous avez déjà vu comment utiliser le deuxième argument de notre fonction `enumerateTokenVectors` : la fermeture `using` avec une signature de `([Double], Range<String.Index>) -> Bool`. Cela signifie essentiellement que vous lui donnez un tableau de `Double` (oui, c'est enfin notre vecteur 😜) et un index de chaîne et renvoyez un `Bool` : `true` si vous voulez qu'il continue, `false` si vous voulez qu'il s'arrête.

Avec cela à l'esprit, écrivons une fonction qui calcule la moyenne de nos vecteurs qui sont à l'intérieur d'un `NLContextualResult` :

```swift
func meanVectorNaive(result: NLContextualEmbeddingResult) -> [Double]? {
    var sumVector: [Double]? = nil
    var count = 0
    result.enumerateTokenVectors(in: result.string.startIndex..<result.string.endIndex) { vector, _ in
        if sumVector == nil {
            sumVector = vector
        } else {
            precondition(sumVector!.count == vector.count, "All vectors must have the same length")
            for i in 0..<sumVector!.count {
                sumVector![i] += vector[i]
            }
        }
        count += 1
        return true
    }

    // Vérifiez que nous ne faisons pas face à un tableau vide de vecteurs - évitez la division par 0
    guard var sumVector = sumVector, count > 0 else {
        print("meanVectorNaive: No token vectors to average")
        return nil
    }

    let divisor = Double(count)
    for i in 0..<sumVector.count {
        sumVector[i] /= divisor
    }
    return sumVector
}
```

Voici ce qui se passe dans le code :

- Nous définissons notre `sumVector` et `count` (ce sera le nombre de vecteurs que nous avons additionnés).
- Ensuite, nous appelons le `enumerateTokenVectors` avec une fermeture qui ajoute la valeur de chaque vecteur au `sumVector` et augmente `count` de +1 pour chaque vecteur. Nous commençons la boucle avec un `sumVector` étant `nil` et le définissons sur la valeur du premier vecteur qui entre.
- Ensuite, nous divisons chaque composant du `sumVector` par le nombre de vecteurs que nous avions initialement,
- ...et nous entourons cela de quelques gardes pour éviter la division par zéro.

Notez que dans ma base de code, j'ai enveloppé cela en tant qu'[extensions à `NLContextualEmbeddingResult`](https://github.com/tillg/SwiftEmbeddings/blob/main/SwiftEmbeddings/SwiftEmbeddings/NLContextualEmbeddingExtension.swift).

Avant de mesurer le temps de notre regroupement moyen naïf, voyons combien de temps il faut pour simplement calculer les vecteurs d'intégration avec `NLContextualEmbedding` :

Calculer 722 intégrations avec `NLContextualEmbedding` (sans les compiler en leur moyenne) prend 5245 ms ~ 5,2 secondes.

Pour le mettre en relation, ajoutons cela à notre tableau d'aperçu :

| Ensemble de données : 722 morceaux                       | Calculer vecteurs | Calculer distances | Trier tableau | ms / Vecteur |
| -------------------------------------------------------- | ----------------- | ------------------ | ------------- | ------------ |
| NLEmbedding                                              | 35 sec            | 70 sec             | 1554 sec      | 49 ms        |
| NLContextualEmbedding (Juste l'intégration)              | 5 sec             |                    |               | 7,26 ms      |