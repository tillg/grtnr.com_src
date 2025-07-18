---
date: 2025-03-24
image: developer_podcast.jpg
excerpt: "Ich habe einen interessanten Podcast darüber gehört, wie man verschiedene Modelltypen in Swift strukturiert: Domain-Modelle, die meine interne Darstellung sind, Datenmodelle (oder DTOs), die die externe Darstellung sind, und View-Modelle, die die Darstellung für die Benutzeroberfläche sind. Aber viele Aspekte sind mir noch unklar."
translation: de
source_language: en
source_hash: e5f70dbd927f7137061d6c631f9bd7ef414c3992a3c494fd9f1f3ccce95df6a3
translator: gpt-4o-2024-08-06
translate_date: 2025-07-18T21:55:20.918187
generated_by: simplified-translation-system
---

[TOC]

Ich habe gestern einen wirklich netten Podcast darüber gehört, wie man verschiedene Modelltypen in Swift strukturiert: Domain-Modelle, die meine interne Darstellung sind, Datenmodelle (oder DTOs), die die externe Darstellung sind, und View-Modelle, die die Darstellung für meine Benutzeroberfläche sind:

[![Entwickler-Podcast](developer_podcast.jpg)](https://podcasts.apple.com/de/podcast/developer-podcast/id1467065787?i=1000698509743)

Dieser Beitrag ist im Grunde eine Frage, die ich dem [Discord, das zum Podcast gehört](https://discord.com/invite/j57uchzUa9), hinzugefügt habe.

# Frage

Ich bin ein Swift-Anfänger, und viele Aspekte sind mir noch unklar. Basierend auf dem Beispiel, das Sie im Podcast verwendet haben, werde ich versuchen, die Lücken in meinem Verständnis zu füllen.

## Domain-Modelle, Datenmodelle und Mapper

Das Beispiel ist eine ToDo-App und somit ist die Haupteinheit die **Aufgabe**. Also hätte ich ein Domain-Modell `Task`, das so aussieht:

```swift
struct Task {
    let id: UUID
    let title: String
    let description: String
    let dueDate: Date
    let isCompleted: Bool
}
```

Da ich meine Aufgaben in CloudKit speichern möchte, benötige ich ein Datenmodell, das mit CloudKit kompatibel ist. Daher benötige ich `CKRecord`-Objekte, die Aufgaben darstellen. Meinem Verständnis nach werden sie so aufgebaut:

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

Und ich hätte die entsprechende Funktion, um ein `CKRecord` zurück zu einer `Task` zu konvertieren:

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

Fragen:

- **Wo** platziere ich die Mapping-Funktionen? Gehören sie zum Domain-Modell oder zum Datenmodell? Ich vermute, sie gehören eher zum Datenmodell.
- **Fehler**: Wie gehe ich mit Fehlern um? Zum Beispiel, wenn das `CKRecord` keinen Wert für `id` enthält, würde ich einen Absturz bekommen. Sollte ich Optionals verwenden oder einen Fehler werfen?

## Repository

Dann erwähnen Sie das Repository. Basierend auf der früheren Diskussion auf Discord würde ich annehmen, dass das Repository nur mit Domain-Modellen arbeitet. Es könnte also so aussehen:

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

Und basierend auf diesem Protokoll könnte ich ein `TaskRepositoryCloudKit` implementieren, das die Mapping-Funktionen nutzt, um zwischen Domain- und Datenmodellen zu konvertieren und alle CRUD-Operationen, die im (im Speicher) TaskRepository durchgeführt werden, in der CloudKit-Datenbank widerspiegelt.

Nächste Frage:

- **Repository-Funktionen**: Typischerweise würde ich Funktionen aus einem Repository erstellen, die über CRUD hinausgehen. Zum Beispiel ein `getTasksDateRange`, das das älteste und das neueste Fälligkeitsdatum zurückgibt. Wo würde ich das erstellen? Ich möchte es nicht in `TaskRepositoryCloudKit` setzen, da es die gleiche Logik wäre, wenn ein anderer Speicher verwendet wird (d.h. alle Aufgaben in den Speicher laden, sie sortieren und die erste und letzte zurückgeben). Da ich keine Funktionen in einem Protokoll haben kann, wo platziere ich es?
- **Benennung**: Ist die von mir vorgeschlagene Benennung sinnvoll? Ist es so, wie Sie es in Swift machen würden? Ich habe `TaskRepositoryCloudKit` gewählt, damit es neben dem `TaskRepository` im Xcode-Dateibrowser aufgelistet wird. Wenn ich andere Datenmodelle benötigen würde, um ein System Xyz zu integrieren, würde ich sie `TaskRawXyz` nennen - ist das sinnvoll?

# Antwort

Ich habe eine großartige [Antwort](https://discord.com/channels/1028834407374655518/1028846930182291526/1353860001411760228) von [Cocoatype](https://pado.name) auf Discord erhalten. Und ich bin sehr dankbar, dass er sich die Zeit genommen hat, die Antwort zu lesen und zu tippen.

Hier ist Cocoatypes Antwort zur Referenz:

> **Wo** platziere ich die Mapping-Funktionen? Gehören sie zum Domain-Modell oder zum Datenmodell? Ich vermute, sie gehören eher zum Datenmodell.
> Ich würde diese im Repository oder in einem Hilfstyp für das Repository platzieren. Zum Beispiel habe ich in meiner App Barc ein `BarcodeRepository`-Protokoll und ein `FileBarcodeRepository`, das SwiftData verwendet. Hier ist ein kleiner Überblick, wie das aussieht:

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

> **Fehler**: Wie gehe ich mit Fehlern um? Zum Beispiel, wenn das CKRecord keinen Wert für id enthält, würde ich einen Absturz bekommen. Sollte ich Optionals verwenden oder einen Fehler werfen?

Ich persönlich werfe Fehler und gehe auf der Ebene damit um, auf der es sinnvoll ist, damit umzugehen. Optionals sind in Ordnung, wenn etwas tatsächlich optional ist, aber denken Sie daran, dass Sie hier versuchen, zu vermeiden, dass Sie mit API-Einschränkungen in Ihrem View-Code umgehen müssen. Ich würde also nichts optional machen, nur um Fehler zu vermeiden.

> **Repository-Funktionen**: Typischerweise würde ich Funktionen aus einem Repository erstellen, die über CRUD hinausgehen. Zum Beispiel ein getTasksDateRange, das das älteste und das neueste Fälligkeitsdatum zurückgibt. Wo würde ich das erstellen? Ich möchte es nicht in TaskRepositoryCloudKit setzen, da es die gleiche Logik wäre, wenn ein anderer Speicher verwendet wird (d.h. alle Aufgaben in den Speicher laden, sie sortieren und die erste und letzte zurückgeben). Da ich keine Funktionen in einem Protokoll haben kann, wo platziere ich es?

Wenn Sie etwas über mehrere Implementierungen hinweg haben möchten, verwenden Sie eine Protokollerweiterung. Zum Beispiel:

```swift
extension TaskRepository {
    func getTasks(dateRange: Range<Date>) -> [Task] {
        return getAllTasks().filter { task in
            dateRange.contains(task.dueDate)
        }
    }
}
```

Da Sie wissen, dass alle TaskRepository-Implementierungen ein `getAllTasks()` haben, können Sie es in der Erweiterung so verwenden.

> **Benennung**: Ist die von mir vorgeschlagene Benennung sinnvoll? Ist es so, wie Sie es in Swift machen würden? Ich habe TaskRepositoryCloudKit gewählt, damit es neben dem TaskRepository im Xcode-Dateibrowser aufgelistet wird. Wenn ich andere Datenmodelle benötigen würde, um ein System Xyz zu integrieren, würde ich sie TaskRawXyz nennen - ist das sinnvoll

Ich persönlich setze den spezifischsten Teil zuerst (BarcodeRepository wird zu FileBarcodeRepository und PreviewBarcodeRepository und StubBarcodeRepository), aber am Ende ist auch in Ordnung. Daran ist nichts Ungewöhnliches.