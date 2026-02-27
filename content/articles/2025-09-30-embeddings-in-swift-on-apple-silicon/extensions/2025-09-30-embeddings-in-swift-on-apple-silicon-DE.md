---
date: 2025-09-30
image: embedding.png
excerpt: Apple hat neue Embedding-Modelle eingeführt, die ich nutzen möchte, um die Nähe von Texten zu messen. Dies ist mein Weg, wie ich sie erstelle und effizient nutze.
title: Embeddings in Swift auf Apple Silicon
tags: tech
translation: de
source_language: en
source_hash: 99f94cce4e66af838911fcc4b2ab79dc8fc884f1793594d7b959118b261bcd38
translator: gpt-4o-2024-08-06
translate_date: 2026-02-27T10:30:08.544266+00:00
generated_by: simplified-translation-system
---

**In Arbeit!!**

Ich lerne gerade die Programmiersprache Swift. Dabei folge ich dem fantastischen Kurs [100 Days of SwiftUI](https://www.hackingwithswift.com/100/swiftui/) von Paul Hudson. Es ist ein großartiger Kurs, der zuerst grundlegendes Swift und dann SwiftUI behandelt.

Wenn ich versuche, mein Wissen auf kleine Projekte anzuwenden, tauchen immer viele Fragen auf, und die verlässlichste Quelle, um Antworten zu finden, ist der Kurs, also seine Seiten. Daher muss ich auf Paul Hudsons Seite suchen, genauer gesagt in den Seiten seines Kurses.

Da ich auch mit Machine Learning herumspiele, habe ich geplant, eine App zu entwickeln, die ich **AskPaul** nennen würde: Gib deine Frage ein und erhalte Antworten, die von einem (lokalen!) RAG-System erstellt wurden: Ein System, das alle Seiten des Kurses in Markdown enthält, in Stücke zerlegt und mit ihren Embeddings indexiert. Dann suche die relevanten Stücke für die aktuelle Frage und übergebe sie zusammen mit der Frage an das LLM. Und wenn ich LLM sage, meine ich das lokale LLM auf deinem Apple-Gerät 😜

Um mit den Swift Embeddings zu experimentieren, habe ich ein Repo [SwiftEmbeddings](https://github.com/tillg/SwiftEmbeddings) eingerichtet. Es enthält meinen Code & [Playgrounds](https://github.com/tillg/SwiftEmbeddings/tree/main/SwiftEmbeddings/SwiftEmbeddings/Playgrounds).

## Was getan werden muss

Hier ist, was ich erreichen möchte:

Angenommen, es gibt eine Reihe von Webseiten als Markdown, zerteile sie in handliche Portionen und erstelle ihre Embeddings: Ein Vektor (d.h. eine Serie von 512 Double-Werten), der _ihren Inhalt_ auf mathematische Weise darstellt.

Angenommen, es gibt eine Frage (denke an etwas wie `In Swift, wie kann ich ein Protokoll erweitern?`), sollte das System die Stücke mit relevantem Inhalt finden, indem es den Embedding-Vektor dieser Frage berechnet und dann mit allen Vektoren der Stücke vergleicht, um das nächste zu finden. Diese Stücke werden dann zusammen mit der Frage an das LLM übergeben.

Im _alten_ Apple Embedding-System, das im [Natural Language framework](https://developer.apple.com/documentation/NaturalLanguage) zu finden ist, sind die Funktionen, um dies zu erreichen, leicht zugänglich und sehr gut im Artikel [Finding similarities between pieces of text](https://developer.apple.com/documentation/naturallanguage/finding-similarities-between-pieces-of-text) erklärt.

## Das Problem

Aber es gibt einen neuen Akteur: [NLContextualEmbedding](https://developer.apple.com/documentation/naturallanguage/nlcontextualembedding). Es wurde in iOS 17/macOS 14 eingeführt und in iOS 18/macOS 15 erweitert.

Hier ist, warum ich das neue `NLContextualEmbedding` verwenden möchte:

- Erfasst Kontext: Es würde den Unterschied zwischen „river bank“ und „investment bank“ machen. Das ältere `NLEmbedding` machte diesen Unterschied nicht.
- Ist mehrsprachig und sprachübergreifend: Durch das gleichzeitige Training auf mehreren Sprachen richtet das Modell semantische Räume über Sprachen hinweg aus, sodass „chien“ und „dog“ nahe beieinander eingebettet sind.
- Unterstützt mehr Sprachen
- Läuft vollständig auf dem Gerät: Das Modell respektiert die Privatsphäre der Nutzer und funktioniert offline. Nur kleine Modelfiles werden bei Bedarf heruntergeladen und systemweit zwischengespeichert.
- Bietet robuste API-Steuerungen: Entwickler können Modelleigenschaften inspizieren, Assets verwalten und Embeddings in ihre eigenen ML-Pipelines integrieren.

Was fehlt, sind

- das Äquivalent zu `NLEmbedding`'s `vector(for:)`: Einen Vektor für einen Satz oder ein Stück erhalten
- das Äquivalent zu `distanceBetweenString:andString:distanceType:`: Ein Maß für die Distanz zwischen 2 Sätzen erhalten.

Was `NLContextualEmbedding` bietet, ist eine Funktion `embeddingResult(for: String, language: NLLanguage?) throws -> NLContextualEmbeddingResult`. Aber wenn du in die Struktur des `NLContextualEmbeddingResult` schaust, siehst du, dass es einen Vektor für jedes Token erstellt, also einen Vektor von Vektoren. Außerdem werden diese Vektoren mit einem Iterator abgerufen: `enumerateTokenVectors(in: Range<String.Index>, using: ([Double], Range<String.Index>) -> Bool)` - was für mich einiges an Überlegungen und Lernen erforderte...

Also habe ich mich daran gemacht, ein einfach zu verwendendes Tooling zu entwickeln, das auf dem neuen `NLContextualEmbedding` basiert, ähnlich dem, was wir in `NLEmbedding` haben.

Beachte, dass ein entscheidender Aspekt die Leistung ist, da es viele Vergleiche erfordert, um die am besten passenden Stücke/Vektoren in einem größeren Satz zu finden - und meine ersten Versuche dauerten viele Minuten, um zu suchen...

## Testdaten

Da ich mit der Idee begann, ein On-Device RAG-System für Paul Hudsons SwiftUI-Kurs zu bauen, habe ich Folgendes getan:

- Die Hauptseiten des SwiftUI-Kurses in Markdown scrapen
- Sie in Stücke zerteilen
- Sie alle in eine JSON-Datei schreiben, die ich in mein Swift-Projekt kopieren kann

Um dies zu erledigen, habe ich einige Skripte in [site2chunks](https://github.com/tillg/site2chunks) zusammengesteckt. Ein Beispiel-JSON befindet sich in meinem AskPaul-Projekt: [merged_chunks](https://github.com/tillg/SwiftEmbeddings/blob/main/SwiftEmbeddings/SwiftEmbeddings/merged_chunks.json)

Basierend darauf habe ich in meinem Swift-Code

- Eine `struct Chunk`. Wenn du neugierig bist, sieh dir den [Code](https://github.com/tillg/AskPaul/blob/main/AskPaul/AskPaul/Chunk.swift) an, der ein Stück darstellt
- Eine `Bundle Extension`, die die Stücke aus der JSON-Datei liest ([Code]()). Hinweis: Dies ist natürlich inspiriert von [Paul Hudsons Kurs](https://www.hackingwithswift.com/example-code/system/how-to-decode-json-from-your-app-bundle-the-easy-way) 😜

**Hinweis**: Ich beginne nur mit den _Hauptseiten_: der Einstiegsseite jeder der 100 Lektionen. Ich mache dies, damit der Datensatz leicht zu handhaben ist und meine Experimente schnell durchführbar sind. Diese 100 Seiten sind in 722 Stücke zerteilt. Sobald ich mit den Experimenten fertig bin, werde ich den Datensatz auf alle Seiten von hackingwithswift.com erweitern.

## Der Ausgangspunkt: `NLEmbedding`

Mit diesen Testdaten an Ort und Stelle, lass uns mit dem _alten_ `NLEmbedding` herumspielen. Du kannst den Code in [Playgrounds/01-NLEmbedding.swift](https://github.com/tillg/SwiftEmbeddings/blob/main/SwiftEmbeddings/SwiftEmbeddings/Playgrounds/01-NLEmbedding.swift) nachschlagen

Die grobe Struktur des Codes sieht so aus:

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

Hier ist, worum es in diesem Code geht:

- Wir initialisieren unsere Variablen `question` und `potentialAnswer`
- Wir erstellen unser `NLEmbedding`-Objekt - das theoretisch fehlschlagen könnte. Wenn es das tut, können wir nichts anderes tun, als alles zu beenden.
- Dann berechnen wir die [Entfernung](<https://developer.apple.com/documentation/naturallanguage/nlembedding/distance(between:and:distancetype:)>) zwischen der Frage und drucken sie aus.

Als nächstes schauen wir, wie lange es dauert, die Embedding-Vektoren für alle 722 Stücke aus unseren Testdaten zu berechnen. Auf meinem MacBook Pro dauert es 35'966 ms ~ 35 Sekunden oder ~ 49 ms / Vektor.

Der andere Test ist das Berechnen von Entfernungen zwischen Satzpaaren:

```swift
let distance = sentenceEmbedding.distance(between: chunk1.content, and: chunk2.content)
```

Wie erwartet dauert dies etwa doppelt so lange, da für jede Distanzberechnung 2 Embedding-Vektoren berechnet werden müssen: `⏱️ [Calculating distances with NLEmbedding] count=1  total=72.558420s  avg=72.558420s`

Beachte, dass wenn ich die Schleife ausführe, die immer die Entfernung zum gleichen Text berechnet, es fast genau so lange dauert wie nur das Berechnen eines Vektors. Mit anderen Worten, diese Schleife:

```swift
for chunk in chunks {
    let distance = sentenceEmbedding.distance(between: chunk.content, and: "This is a simple text")
}
```

dauert etwa 36 Sekunden. Dies würde darauf hindeuten, dass das Berechnen der Entfernung zwischen 2 Vektoren sehr wenig Zeit in Anspruch nimmt...

Das letzte, was ich tun möchte, ist, die `k` nächsten Stücke zu einer gegebenen Frage zu finden. Meine Methode, dies zu tun, besteht darin, das Array der Stücke nach ihrer Entfernung zu unserer Frage zu sortieren:

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

Das Finden der nächsten Stücke zu einer gegebenen Frage (was dem Sortieren des Arrays entspricht) dauert ziemlich lange: 1'554'280 ms ~ 1'554 Sekunden ~ 25 MINUTEN

Beachte, dass wir 11'290 Vergleiche benötigen. Da ich davon ausgehe, dass Apple den Vektor des einen Satzes, der in jedem Vergleich verwendet wird, zwischenspeichert, bedeutet das, dass es die Zeit für 11'290 x (Vektor berechnen + Vektordistanz berechnen) verwendet hat. Seltsamerweise ergibt das ~ 137 ms / (Vektor berechnen + Distanz berechnen)...

Ein Versuch, unsere Ergebnisse in einer Übersicht darzustellen:

| Datensatz: 722 Stücke | Vektoren berechnen | Distanzen berechnen | Array sortieren | ms / Vektor |
| --------------------- | ------------------ | ------------------- | --------------- | ----------- |
| NLEmbedding           | 35 sec             | 70 sec              | 1'554 sec       | 49 ms       |

## Zeit messen

Da wir viel Verarbeitungszeit messen werden, die durch unsere Berechnungen verbraucht wird, habe ich ein kleines Zeitverfolgungssystem gebaut. So wird es aufgerufen:

```swift
timerTrack("Timer name") {
    // Some code that I want to time here
}
timerReport("Timer name") // Prints out my timer stats
```

Mein `timerTrack` gibt auch das Ergebnis seines Blocks zurück und funktioniert asynchron. So können wir Dinge wie folgt tun:

```swift
let result = try timerTrack("Embedding") {
    try embeddingResult(for: sentence, language: language)
}
```

## Einen Embedding-Vektor basierend auf `NLContextualEmbedding` auf naive Weise berechnen

Wenn wir nun versuchen, etwas Ähnliches mit `NLContextualEmbedding` zu tun, müssen wir zuerst einige grundlegende Codierungen durchführen: Apples Contextual Embedding generiert eine Liste von Vektoren, insbesondere einen pro Token.

Also müssen wir sie zu nur einem Vektor zusammenfassen. Eine Standardmethode, dies zu erreichen, ist das Vektor-Pooling:

[Die gebräuchlichste Methode ist das Mittelwert-Pooling, bei dem die Embeddings aller Tokens (ohne Padding) gemittelt werden.](https://milvus.io/ai-quick-reference/how-do-sentence-transformers-create-fixedlength-sentence-embeddings-from-transformer-models-like-bert-or-roberta)

Stell dir vor, du hast 2 3-dimensionale Vektoren `v1` und `v2` und möchtest ihren Mittelwertvektor `v3` berechnen:

```swift
v3.x = (v1.x + v2.x) / 2;
v3.y = (v1.y + v2.y) / 2;
v3.z = (v1.z + v2.z) / 2;
```

Es wäre eine einfache Schleife durch die Dimensionen, und für jede Dimension berechnest du den Durchschnitt aller Komponenten der Vektoren. Nun stehen wir vor einer kleinen technischen Herausforderung: `NLContextualEmbedding` liefert uns die Vektoren, eingepackt in ein `NLContextualEmbeddingResult`. Wenn du die [Dokumentation](https://developer.apple.com/documentation/naturallanguage/nlcontextualembeddingresult) nachschlägst, hier ist, was sie sagen:

```swift
func enumerateTokenVectors(in: Range<String.Index>, using: ([Double], Range<String.Index>) -> Bool)
# Iterates over the embedding vectors for the range you specify.
```

Es hat einige Zeit gedauert, dies zu verdauen, aber darauf läuft es hinaus:

Du gibst ihm einen `Range<String.Index>`, um anzugeben, von wo bis wo du die Vektoren auflisten möchtest. Warum haben sie nicht einfach etwas wie `0...10` verwendet? Das Geheimnis ist, dass der `Range<String.Index>` nicht einfach durch den Text geht wie `T`, `h`, `ì`, `s`, `_`, `i`, `s`... sondern durch die **Tokens**.

Lass uns untersuchen, wie die Tokens tatsächlich aussehen:

```swift
result.enumerateTokenVectors(in: result.string.startIndex..<result.string.endIndex) { vector, range in
    let token = result.string[range]
    print("Vector for token [\(token)]")
    return true // Return true to keep enumerating, false to stop early
}
```

Das ist, was wir bekommen:

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

Wenn man das sieht, macht es Sinn, dass der Index nicht einfach von 1 bis zur `string.count` zählt, sondern ein etwas komplexeres Biest ist.

Du hast bereits gesehen, wie man das zweite Argument unserer `enumerateTokenVectors`-Funktion verwendet: Die `using`-Closure mit einer Signatur von `([Double], Range<String.Index>) -> Bool`. Das bedeutet im Grunde, dass du ihm ein Array von `Double` gibst (ja, das ist endlich unser Vektor 😜) und einen String-Index und ein `Bool` zurückgibst: `true`, wenn du möchtest, dass es fortfährt, `false`, wenn du möchtest, dass es aufhört.

Mit diesem Wissen, lass uns eine Funktion schreiben, die den Durchschnitt unserer Vektoren berechnet, die sich in einem `NLContextualResult` befinden:

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

    // Check that we are not facing an empty arry of vectors - avoid div by 0
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

Hier ist, was im Code passiert:

- Wir setzen unseren `sumVector` und `count` (dies wird die Anzahl der Vektoren sein, die wir addiert haben).
- Dann rufen wir die `enumerateTokenVectors` mit einer Closure auf, die den Wert jedes Vektors zum `sumVector` hinzufügt und `count` um +1 für jeden Vektor erhöht. Wir starten die Schleife mit einem `sumVector`, der `nil` ist, und setzen ihn auf den Wert des ersten Vektors, der hereinkommt.
- Dann teilen wir jede Komponente des `sumVector` durch die Anzahl der Vektoren, die wir ursprünglich hatten,
- ...und wir umgeben dies mit einigen Guards, um eine Division durch Null zu vermeiden.

Beachte, dass ich dies in meiner Codebasis als [Erweiterungen für `NLContextualEmbeddingResult`](https://github.com/tillg/SwiftEmbeddings/blob/main/SwiftEmbeddings/SwiftEmbeddings/NLContextualEmbeddingExtension.swift) verpackt habe.

Bevor wir die Zeitmessung unseres naiven Mittelwert-Poolings messen, schauen wir, wie lange es dauert, nur die Embedding-Vektoren mit `NLContextualEmbedding` zu berechnen:

Das Berechnen von 722 Embeddings mit `NLContextualEmbedding` (ohne sie zu ihrem Mittelwert zu kompilieren) dauert 5245 ms ~ 5,2 Sekunden.

Um es in Relation zu setzen, fügen wir dies unserer Übersichtstabelle hinzu:

| Datensatz: 722 Stücke                       | Vektoren berechnen | Distanzen berechnen | Array sortieren | ms / Vektor |
| ------------------------------------------- | ------------------ | ----------------