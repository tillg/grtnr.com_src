---
date: 2025-03-24
image: developer_podcast.jpg
excerpt: "J'ai écouté un podcast intéressant sur la structuration de différents types de modèles en Swift : les modèles de domaine qui sont ma représentation interne, les modèles de données (ou DTOs) qui sont la représentation externe, et les modèles de vue qui sont la représentation pour l'interface utilisateur. Mais de nombreux aspects restent encore flous pour moi."
translation: fr
source_language: en
source_hash: e5f70dbd927f7137061d6c631f9bd7ef414c3992a3c494fd9f1f3ccce95df6a3
translator: gpt-4o-2024-08-06
translate_date: 2025-07-18T21:55:45.891504
generated_by: simplified-translation-system
---

[TOC]

J'ai écouté ce très bon podcast hier sur la structuration de différents types de modèles en Swift : les modèles de domaine qui sont ma représentation interne, les modèles de données (ou DTOs) qui sont la représentation externe, et les modèles de vue qui sont la représentation pour mon interface utilisateur :

[![Podcast Développeur](developer_podcast.jpg)](https://podcasts.apple.com/de/podcast/developer-podcast/id1467065787?i=1000698509743)

Ce post est essentiellement une question que j'ai ajoutée au [Discord associé au Podcast](https://discord.com/invite/j57uchzUa9).

# Question

Je suis débutant en Swift, et de nombreux aspects restent encore flous pour moi. Basé sur l'exemple que vous avez utilisé dans le podcast, je vais essayer de combler les lacunes dans ma compréhension.

## Modèles de Domaine, Modèles de Données et Mappers

L'exemple est une application de tâches et donc l'entité principale est la **Tâche**. J'aurais donc un modèle de domaine `Task` qui ressemble à ceci :

```swift
struct Task {
    let id: UUID
    let title: String
    let description: String
    let dueDate: Date
    let isCompleted: Bool
}
```

Comme je veux stocker mes tâches dans CloudKit, j'ai besoin d'un modèle de données compatible avec CloudKit. J'ai donc besoin d'objets `CKRecord` qui représentent les tâches. Selon ma compréhension, ils sont construits comme ceci :

```swift
func mapTaskToCKRecord(task: Task) -> CKRecord {
    let record = CKRecord(recordType: "task")
    record["id"] = task.id as CKRecordValue
    record["title"] = task.title as CKRecordValue
    record["description"] = task.description as CKRecordValue
    record["dueDate"] = task.dueDate as CKRecordValue
    record["isCompleted"] = task.isCompleted as CKRecordValue
    return record
}
```

Et j'aurais la fonction correspondante pour mapper un `CKRecord` de retour à une `Task` :

```swift
func mapCKRecordToTask(record: CKRecord) -> Task {
    let id = record["id"] as! UUID
    let title = record["title"] as! String
    let description = record["description"] as! String
    let dueDate = record["dueDate"] as! Date
    let isCompleted = record["isCompleted"] as! Bool
    return Task(id: id, title: title, description: description, dueDate: dueDate, isCompleted: isCompleted)
}
```

Questions :

- **Où** dois-je placer les fonctions de mappage ? Font-elles partie du modèle de domaine ou du modèle de données ? Je suppose qu'elles appartiennent plutôt au modèle de données.
- **Erreurs** : Comment gérer les erreurs ? Par exemple, si le `CKRecord` ne contient pas de valeur pour `id`, je rencontrerais un crash. Dois-je utiliser des optionnels ou lancer une erreur ?

## Référentiel

Ensuite, vous mentionnez le référentiel. Basé sur la discussion précédente sur Discord, je supposerais que le référentiel ne traite que des modèles de domaine. Il pourrait donc ressembler à ceci :

```swift
protocol TaskRepository {
    func getAllTasks() -> [Task]
    func getTaskById(id: UUID) -> Task?
    func getTasksByCompletionStatus(isCompleted: Bool) -> [Task]
    func addTask(task: Task)
    func updateTask(task: Task)
    func deleteTask(id: UUID)
}
```

Et basé sur ce protocole, je pourrais implémenter un `TaskRepositoryCloudKit` qui utilise les fonctions de mappage pour convertir entre les modèles de domaine et de données et reflète toutes les opérations CRUD effectuées sur le référentiel de tâches (en mémoire) dans la base de données CloudKit.

Prochaine question :

- **Fonctions du référentiel** : Typiquement, je construirais des fonctions à partir d'un référentiel qui vont au-delà du CRUD. Par exemple, une fonction `getTasksDateRange` qui retourne la date d'échéance la plus ancienne et la plus récente. Où devrais-je construire cela ? Je ne veux pas le mettre dans `TaskRepositoryCloudKit` car ce serait la même logique lors de l'utilisation d'un stockage différent (c'est-à-dire charger toutes les tâches en mémoire, les trier et retourner la première et la dernière). Comme je ne peux pas avoir de fonctions dans un protocole, où dois-je le mettre ?
- **Nommage** : Le nommage que j'ai suggéré est-il raisonnable ? Est-ce ainsi que vous le feriez en Swift ? J'ai choisi `TaskRepositoryCloudKit` pour qu'il soit listé à côté de `TaskRepository` dans le navigateur de fichiers Xcode. Si j'avais besoin d'autres modèles de données pour interfacer un système Xyz, je les appellerais `TaskRawXyz` - est-ce raisonnable ?

# Réponse

J'ai reçu une excellente [réponse](https://discord.com/channels/1028834407374655518/1028846930182291526/1353860001411760228) de [Cocoatype](https://pado.name) sur Discord. Et je suis très reconnaissant qu'il ait pris le temps de lire et de rédiger la réponse.

Voici la réponse de Cocoatype pour référence :

> **Où** dois-je placer les fonctions de mappage ? Font-elles partie du modèle de domaine ou du modèle de données ? Je suppose qu'elles appartiennent plutôt au modèle de données.
> Je mettrais ces fonctions dans le référentiel ou dans un type d'assistance pour le référentiel. Par exemple, dans mon application Barc, j'ai un protocole `BarcodeRepository`, et un `FileBarcodeRepository` qui utilise SwiftData. Voici un petit aperçu de ce à quoi cela ressemble :

```swift
public protocol BarcodeRepository {
    var codes: [Code] { get throws }
}

class FileBarcodeRepository: BarcodeRepository {
    private var models: [BarcodeModel] {
        get throws {
            let sort = SortDescriptor(\BarcodeModel.createdDate, order: .reverse)
            let descriptor = FetchDescriptor(sortBy: [sort])
            return try modelContainer.mainContext.fetch(descriptor)
        }
    }

    private let mapper = BarcodeModelMapper()
    var codes: [Code] {
        get throws {
            return try models.compactMap {
                do {
                    return try mapper.code(from: $0)
                } catch {
                    errorHandler.log(error, module: "Persistence", type: "FileBarcodeRepository")
                    return nil
                }
            }
        }
    }
}

struct BarcodeModelMapper {
    func code(from model: BarcodeModel) throws -> Code {
        let value = switch model.type {
            // elided for length; just a bunch of cases
        }

        guard let modelName = model.name else { throw BarcodeModelMapperError.noNameSet }
        let name = if modelName.isEmpty { Strings.BarcodeModelMapper.untitledCodeName } else { modelName }

        return Code(
            name: name,
            value: value,
            location: model.location.map(locationMapper.location(from:)),
            date: model.date
        )
    }
}
```

> **Erreurs** : Comment gérer les erreurs ? Par exemple, si le CKRecord ne contient pas de valeur pour id, je rencontrerais un crash. Dois-je utiliser des optionnels ou lancer une erreur ?

Personnellement, je lance des erreurs et je les gère au niveau où il est raisonnable de les gérer. Les optionnels sont bien si quelque chose est réellement optionnel, mais souvenez-vous que ce que vous essayez de faire ici est d'éviter d'avoir à gérer les contraintes de l'API dans votre code de vue. Donc, je ne rendrais pas quelque chose optionnel juste pour éviter des erreurs.

> **Fonctions du référentiel** : Typiquement, je construirais des fonctions à partir d'un référentiel qui vont au-delà du CRUD. Par exemple, une fonction getTasksDateRange qui retourne la date d'échéance la plus ancienne et la plus récente. Où devrais-je construire cela ? Je ne veux pas le mettre dans TaskRepositoryCloudKit car ce serait la même logique lors de l'utilisation d'un stockage différent (c'est-à-dire charger toutes les tâches en mémoire, les trier et retourner la première et la dernière). Comme je ne peux pas avoir de fonctions dans un protocole, où dois-je le mettre ?

Si vous voulez avoir quelque chose à travers plusieurs implémentations, utilisez une extension de protocole. Par exemple :

```swift
extension TaskRepository {
    func getTasks(dateRange: Range<Date>) -> [Task] {
        return getAllTasks().filter { task in
            dateRange.contains(task.dueDate)
        }
    }
}
```

Parce que vous savez que toutes les implémentations de TaskRepository ont un `getAllTasks()`, vous pouvez l'utiliser dans l'extension comme cela.

> **Nommage** : Le nommage que j'ai suggéré est-il raisonnable ? Est-ce ainsi que vous le feriez en Swift ? J'ai choisi TaskRepositoryCloudKit pour qu'il soit listé à côté de TaskRepository dans le navigateur de fichiers Xcode. Si j'avais besoin d'autres modèles de données pour interfacer un système Xyz, je les appellerais TaskRawXyz - est-ce raisonnable

Personnellement, je mets la partie la plus spécifique en premier (BarcodeRepository devient FileBarcodeRepository et PreviewBarcodeRepository et StubBarcodeRepository), mais à la fin, c'est bien aussi. Rien d'étrange dans un sens ou dans l'autre.