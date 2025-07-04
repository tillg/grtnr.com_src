---
Tags: tech, AI
Title: Más allá de la codificación por vibración - Rediseñando Filmz
Date: 2025-05-21
image: filmz.png
summary: Hace algún tiempo construí una pequeña aplicación iOS llamada Filmz con _codificación por vibración_. Resulta que eso es agradable hasta que terminas con _depuración por vibración_. Así que ahora hago un nuevo intento, comenzando de una manera más estructurada.
Translation: es
Source-Language: en
Translator: gpt-4
Translate-Date: 2025-07-04T16:39:27.383122
Source-File: /Users/tgartner/git/grtnr.com_src/content/articles/2025-05-21-beyond-vibe-coding/2025-05-21-beyond-vibe-coding.md
Generated-By: automatic-translation-plugin
---

<img src="filmz.png" alt="Filmz" width="300">

Hace algún tiempo construí una pequeña aplicación iOS llamada Filmz: mantén un registro de las películas y programas que quieres ver o que ya has visto. Conserva información adicional personal como "¿me gustó?" (es decir, mi calificación personal), "¿A qué público lo recomendaría?" (Adultos, niños, familia) "¿Cuándo y dónde lo vi?" etc. Y luego viene el compartir: pasar recomendaciones de películas a amigos, ya sea una película a la vez o listas.

Como no sabía nada de Swift en aquel entonces, la construí en un estilo de _codificación por vibración_, totalmente respaldado por IA (en aquel entonces principalmente Cursor.ai). Esto me dio un inicio rápido, pero me perdí una vez que quise agregar características más complejas que requerían una base de código bien estructurada. Y como no sabía mucho sobre Swift, tampoco pude hacerlo. La depuración por vibración no funciona - todavía…

Así que aquí empiezo de nuevo, y con un enfoque diferente: intentaré trabajar de manera similar a como lo haría con un desarrollador junior pero inteligente. El enfoque estará en un enfoque paso a paso, seguido de una documentación adecuada: Descripciones de la tarea en cuestión, descripción de los cambios de arquitectura, de las opciones que se inspeccionaron / pensaron y qué se eligió por qué...

[Trabajé con mi amigo AI ChatGPT](https://chatgpt.com/share/68371708-8a44-8009-b424-059b920feec9), y planeo comenzar con una estructura como la descrita a continuación.

```text
README.md                        # Descripción general del proyecto e instrucciones de configuración
docs/                     # Todo lo que *no* es código fuente vive aquí
├── index.md              # Descripción funcional de alto nivel (centrada en el usuario)
├── architecture.md       # Tecnología de alto nivel
├── glossary.md           # Vocabulario del dominio
├── features/             # Un subdirectorio *por* característica ⬇
│   ├── dark-mode/
│   │   ├── 01-intent.md          # "Historia de usuario" o declaración del problema
│   │   ├── 02-ui-flow.md         # Flujo de cableado, capturas de pantalla, diagramas → mantener PNG/Drawio *en la misma carpeta*
│   │   ├── 03-design.md          # Diseño técnico y pseudocódigo
│   │   ├── 04-test-plan.md       # Lista de aceptación y casos límite
│   │   └── dark-mode.drawio.png  # El diagrama se encuentra junto al texto que lo referencia
│   ├── profile-refactor/
│   │   └── …
│   └── _TEMPLATE/               # Esqueleto vacío que copias al agregar una característica
├── data-structure/            # Estructuras de entidad o ERDs, notas de migración
│   ├── schema-overview.mmd
│   └── schema.md
├── adr/                  # Registros de decisiones de arquitectura
│   ├── ADR-001-use-themex.md
│   └── ADR-002-db-index.md
└── changelog.md          # Historial al estilo "Keep a Changelog"
```

2025-05-28: Tomo esto como punto de partida, trabajo y veo qué falta. Y agrego los bits que faltan en el camino.