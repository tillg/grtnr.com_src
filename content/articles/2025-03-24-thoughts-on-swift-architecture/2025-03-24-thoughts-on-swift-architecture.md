---
date: 2025-03-24
image: developer_podcast.jpg
excerpt: "I heard an interesting podcast on how to structure different model types in Swift: Domain models that are my internal representation, Data Models (or DTOs) that are the external representation, and View Models that are the representation for the UI. But many aspects are still unclear to me."
---

[TOC]

I heard this really nice podcast yesterday on how to structure different model types in Swift: Domain models that are my internal representation, Data Models (or DTOs) that are the external representation, and View Models that are the representation for my UI:

[![Developer Podcast](developer_podcast.jpg)](https://podcasts.apple.com/de/podcast/developer-podcast/id1467065787?i=1000698509743)

This post basically is a question that I added to the [Discord that goes with the Podcast](https://discord.com/invite/j57uchzUa9).

# Question

I'm a Swift Rookie, and many aspects are still unclear to me. Based on the example you guys used in the podcast, I will try to fill out the gaps in my understanding.

## Domain Models, Data Models, and Mappers

The example is a ToDo app and so the main entity is the **Task**. So I would have a Domain model `Task` that looks like this:

```swift
struct Task {
    let id: UUID
    let title: String
    let description: String
    let dueDate: Date
    let isCompleted: Bool
}
```

As I want to store my tasks in CloudKit, I need a Data Model that is compatible with CloudKit. So I need `CKRecord` objects that represent tasks. According to my understanding, they are built like this:

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

And I would have the corresponding function to map a `CKRecord` back to a `Task`:

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

Questions:

* **Where** do I put the mapping functions? Are they part on the Domain Model or the Data Model? I guess they rather belong to the the Data Model.
* **Errors**: How to deal with errors? For example, if the `CKRecord` does not contain a value for `id`, I would get a crash. Should I use optionals or throw an error?

## Repository

Then you mention the repository. Based on the earlier discussion on Discord, I would assume the repository only deals with Domain models. So it might look like this:

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

And based on this protocol I could implement a `TaskRepositoryCloudKit` that uses the mapping functions to convert between Domain and Data Models and reflects all the CRUD operations that are made to the (in memory) TaskRepostory to the CloudKit database.

Next question:

* **Repository functions**: Typically I would build functions from a repository that are beyond CRUD. For example a `getTasksDateRange` that returns the oldest and most recent due date. Where would I build this? I don't want to put it in `TaskRepositoryCloudKit` as it would be the same logic when using a different storage (i.e. load all the tasks in memory, sort them, and return the first and last). As I can't have functions in a protocol, wher do I put it?
* **Naming**: Is the naming I suggested reasonable? Is it how you would do it in Swift? I chose `TaskRepositoryCloudKit` so it is listed next to the `TaskRepository` in the Xcode file browser. If I would need other Data Models to interface a system Xyz I would call them `TaskRawXyz` - is that reasonable?

# Answer

I got a great [answer](https://discord.com/channels/1028834407374655518/1028846930182291526/1353860001411760228) from [Cocoatype](https://pado.name) on discord. And I am very grateful that he took the time to read and type the answer.

Here is Cocoatype's answer for reference:

> **Where** do I put the mapping functions? Are they part on the Domain Model or the Data Model? I guess they rather belong to the the Data Model.
I would put these in the repository or in a helper type for the repository. For instance, in my app Barc, I have a `BarcodeRepository` protocol, and a `FileBarcodeRepository` that uses SwiftData. Here's a small overview of what that looks like:

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

> **Errors**: How to deal with errors? For example, if the CKRecord does not contain a value for id, I would get a crash. Should I use optionals or throw an error?

I personally throw errors and deal with them at the level it's reasonable to deal with them in. Optionals are fine if something is actually optional, but remember that what you're trying to do here is avoid having to deal with API constraints in your view code. So I wouldn't make something optional just to avoid errors.

> **Repository functions**: Typically I would build functions from a repository that are beyond CRUD. For example a getTasksDateRange that returns the oldest and most recent due date. Where would I build this? I don't want to put it in TaskRepositoryCloudKit as it would be the same logic when using a different storage (i.e. load all the tasks in memory, sort them, and return the first and last). As I can't have functions in a protocol, wher do I put it?

If you want to have something across multiple implementations, use a protocol extension. For instance:

```swift
extension TaskRepository {
    func getTasks(dateRange: Range<Date>) -> [Task] {
        return getAllTasks().filter { task in
            dateRange.contains(task.dueDate)
        }
    }
}
````

Because you know all TaskRepository implementations have a `getAllTasks()`, you can use it in the extension like that.

> **Naming**: Is the naming I suggested reasonable? Is it how you would do it in Swift? I chose TaskRepositoryCloudKit so it is listed next to the TaskRepository in the Xcode file browser. If I would need other Data Models to interface a system Xyz I would call them TaskRawXyz - is that reasonable

I personally put the most specific part first (BarcodeRepository becomes FileBarcodeRepository and PreviewBarcodeRepository and StubBarcodeRepository), but at the end is fine, too. Nothing strange about it either way.
