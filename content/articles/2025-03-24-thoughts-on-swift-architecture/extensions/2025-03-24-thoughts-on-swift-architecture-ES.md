---
date: 2025-03-24
image: developer_podcast.jpg
excerpt: "Escuché un podcast interesante sobre cómo estructurar diferentes tipos de modelos en Swift: Modelos de dominio que son mi representación interna, Modelos de datos (o DTOs) que son la representación externa, y Modelos de vista que son la representación para la UI. Pero muchos aspectos aún no me quedan claros."
Translation: es
Source-Language: en
Translator: gpt-4
Translate-Date: 2025-07-04T16:50:00.344564
Source-File: /Users/tgartner/git/grtnr.com_src/content/articles/2025-03-24-thoughts-on-swift-architecture/2025-03-24-thoughts-on-swift-architecture.md
Generated-By: automatic-translation-plugin
---

[TOC]

Escuché este podcast realmente agradable ayer sobre cómo estructurar diferentes tipos de modelos en Swift: Modelos de dominio que son mi representación interna, Modelos de datos (o DTOs) que son la representación externa, y Modelos de vista que son la representación para mi UI:

[![Podcast de Desarrollador](developer_podcast.jpg)](https://podcasts.apple.com/de/podcast/developer-podcast/id1467065787?i=1000698509743)

Esta publicación básicamente es una pregunta que agregué al [Discord que acompaña al Podcast](https://discord.com/invite/j57uchzUa9).

# Pregunta

Soy un novato en Swift, y muchos aspectos aún no me quedan claros. Basándome en el ejemplo que ustedes usaron en el podcast, intentaré llenar los vacíos en mi comprensión.

## Modelos de Dominio, Modelos de Datos y Mapeadores

El ejemplo es una aplicación ToDo y por lo tanto la entidad principal es la **Tarea**. Entonces tendría un modelo de dominio `Task` que se ve así:

```swift
struct Task {
    let id: UUID
    let title: String
    let description: String
    let dueDate: Date
    let isCompleted: Bool
}
```

Como quiero almacenar mis tareas en CloudKit, necesito un Modelo de Datos que sea compatible con CloudKit. Entonces necesito objetos `CKRecord` que representen tareas. Según mi entendimiento, se construyen así:

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

Y tendría la función correspondiente para mapear un `CKRecord` de vuelta a una `Task`:

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

Preguntas:

- **¿Dónde** coloco las funciones de mapeo? ¿Son parte del Modelo de Dominio o del Modelo de Datos? Supongo que pertenecen más al Modelo de Datos.
- **Errores**: ¿Cómo lidiar con los errores? Por ejemplo, si el `CKRecord` no contiene un valor para `id`, obtendría un fallo. ¿Debería usar opcionales o lanzar un error?

## Repositorio

Luego mencionas el repositorio. Basándome en la discusión anterior en Discord, asumiría que el repositorio solo trata con modelos de dominio. Entonces podría verse así:

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

Y basándome en este protocolo podría implementar un `TaskRepositoryCloudKit` que usa las funciones de mapeo para convertir entre Modelos de Dominio y Modelos de Datos y refleja todas las operaciones CRUD que se realizan en el repositorio de tareas (en memoria) en la base de datos de CloudKit.

Próxima pregunta:

- **Funciones del repositorio**: Normalmente construiría funciones de un repositorio que van más allá de CRUD. Por ejemplo, un `getTasksDateRange` que devuelve la fecha de vencimiento más antigua y más reciente. ¿Dónde construiría esto? No quiero ponerlo en `TaskRepositoryCloudKit` ya que sería la misma lógica al usar un almacenamiento diferente (es decir, cargar todas las tareas en memoria, ordenarlas y devolver la primera y la última). Como no puedo tener funciones en un protocolo, ¿dónde lo pongo?
- **Nomenclatura**: ¿Es razonable la nomenclatura que sugerí? ¿Es así como lo harías en Swift? Elegí `TaskRepositoryCloudKit` para que se liste junto al `TaskRepository` en el explorador de archivos de Xcode. Si necesitara otros Modelos de Datos para interfaz con un sistema Xyz, los llamaría `TaskRawXyz` - ¿es eso razonable?

# Respuesta

Obtuve una gran [respuesta](https://discord.com/channels/1028834407374655518/1028846930182291526/1353860001411760228) de [Cocoatype](https://pado.name) en discord. Y estoy muy agradecido de que se tomó el tiempo para leer y escribir la respuesta.

Aquí está la respuesta de Cocoatype para referencia:

> **¿Dónde** coloco las funciones de mapeo? ¿Son parte del Modelo de Dominio o del Modelo de Datos? Supongo que pertenecen más al Modelo de Datos.
> Yo las pondría en el repositorio o en un tipo de ayuda para el repositorio. Por ejemplo, en mi aplicación Barc, tengo un protocolo `BarcodeRepository`, y un `FileBarcodeRepository` que utiliza SwiftData. Aquí hay una pequeña visión general de cómo se ve eso:

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
            // omitido por longitud; solo un montón de casos
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

> **Errores**: ¿Cómo lidiar con los errores? Por ejemplo, si el CKRecord no contiene un valor para id, obtendría un fallo. ¿Debería usar opcionales o lanzar un error?

Personalmente, lanzo errores y los manejo en el nivel en el que es razonable manejarlos. Los opcionales están bien si algo es realmente opcional, pero recuerda que lo que estás tratando de hacer aquí es evitar tener que lidiar con las restricciones de la API en tu código de vista. Así que no haría algo opcional solo para evitar errores.

> **Funciones del repositorio**: Normalmente construiría funciones de un repositorio que van más allá de CRUD. Por ejemplo, un getTasksDateRange que devuelve la fecha de vencimiento más antigua y más reciente. ¿Dónde construiría esto? No quiero ponerlo en TaskRepositoryCloudKit ya que sería la misma lógica al usar un almacenamiento diferente (es decir, cargar todas las tareas en memoria, ordenarlas y devolver la primera y la última). Como no puedo tener funciones en un protocolo, ¿dónde lo pongo?

Si quieres tener algo en múltiples implementaciones, usa una extensión de protocolo. Por ejemplo:

```swift
extension TaskRepository {
    func getTasks(dateRange: Range<Date>) -> [Task] {
        return getAllTasks().filter { task in
            dateRange.contains(task.dueDate)
        }
    }
}
```

Porque sabes que todas las implementaciones de TaskRepository tienen un `getAllTasks()`, puedes usarlo en la extensión de esa manera.

> **Nomenclatura**: ¿Es razonable la nomenclatura que sugerí? ¿Es así como lo harías en Swift? Elegí TaskRepositoryCloudKit para que se liste junto al TaskRepository en el explorador de archivos de Xcode. Si necesitara otros Modelos de Datos para interfaz con un sistema Xyz, los llamaría TaskRawXyz - ¿es eso razonable?

Personalmente, pongo la parte más específica primero (BarcodeRepository se convierte en FileBarcodeRepository y PreviewBarcodeRepository y StubBarcodeRepository), pero al final también está bien. No hay nada extraño de ninguna manera.