---
date: 2025-03-24
image: https://img.transistor.fm/8oNIHMVZfJuWvHxD2UmRV8s-zz2ZDfXC-Sud2dJRo24/rs:fill:400:400:1/q:60/aHR0cHM6Ly9pbWct/dXBsb2FkLXByb2R1/Y3Rpb24udHJhbnNp/c3Rvci5mbS9lMjg4/Y2UwYzYzMjlmN2My/Y2U4MWE3ZmYwNDJk/YTZhZC5wbmc.webp
excerpt: "I heard an interesting podcast on how to structure different model types in Swift: Domain models that are my internal representation, Data Models (or DTOs) that are the external representation, and View Models that are the representation for the UI. But many aspects are still unclear to me."
---

I heard this really nice podcast yesterday on how to structure different model types in Swift: Domain models that are my internal representation, Data Models (or DTOs) that are the external representation, and View Models that are the representation for my UI:

[![Developer Podcast](https://img.transistor.fm/8oNIHMVZfJuWvHxD2UmRV8s-zz2ZDfXC-Sud2dJRo24/rs:fill:400:400:1/q:60/aHR0cHM6Ly9pbWct/dXBsb2FkLXByb2R1/Y3Rpb24udHJhbnNp/c3Rvci5mbS9lMjg4/Y2UwYzYzMjlmN2My/Y2U4MWE3ZmYwNDJk/YTZhZC5wbmc.webp)](https://podcasts.apple.com/de/podcast/developer-podcast/id1467065787?i=1000698509743)

This post basically is a question that I added to the [Discord that goes with the Podcast](https://discord.com/invite/j57uchzUa9).

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