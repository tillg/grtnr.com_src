---
title: Patio de juegos MCP
image: mcp.png
summary: Notas sobre hallazgos y _comprensiones_ en torno al [Protocolo de Contexto de Modelo también conocido como _MCP](https://modelcontextprotocol.io/introduction).
tags: Tecnología, IA
Translation: es
Source-Language: en
Translator: gpt-4
Translate-Date: 2025-07-04T15:28:56.943508
Source-File: /Users/tgartner/git/grtnr.com_src/content/articles/2025-05-18-mcp-playground/2025-05-18-mcp-playground.md
Generated-By: automatic-translation-plugin
---

Notas sobre hallazgos y _comprensiones_ en torno al [Protocolo de Contexto de Modelo también conocido como _MCP](https://modelcontextprotocol.io/introduction).

[TOC]

## Preguntas

Preguntas abiertas que tengo.

- ¿Puedo ejecutar Claude con diferentes configuraciones de Servidor MCP? Es decir, tengo una configuración por proyecto, digamos una para mi proyecto Python (incluyendo acceso solo a mi directorio de proyecto Python), una para mi proyecto Swift/Xcode (con un directorio diferente y diferentes herramientas).
- Prueba: Juega con MCP Inspector y [Xcode Build MCP Server](https://github.com/cameroncooke/XcodeBuildMCP).

## Accediendo a un servidor MCP

Al buscar y finalmente encontrar un servidor MCP para mi caso de uso, encuentro útil jugar con ellos, para _comprender_ qué herramientas obtiene el LLM. La forma más fácil de hacer esto es con el [MCP Inspector](https://github.com/modelcontextprotocol/inspector).

Para comenzar:

```bash
# Asegúrate de tener instalada una versión reciente de nodeJs (en mi caso con nvm)
nvm use 24
npx @modelcontextprotocol/inspector node build/index.js

# Descarga e inicia el Cliente de la UI de MCP y lo sirve localmente.
```

**Configuración**

El Inspector guarda lo que escribes en la barra lateral en localStorage, pero para configuraciones repetibles puedes guardar un pequeño archivo JSON y apuntar la CLI a él:

```json
// mcp.json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/Users/tunombre/Projects", // leer/escribir
        "/Users/tunombre/Notes", // leer/escribir
        "/Users/tunombre/Code" // ¿solo lectura? añade ',ro' si usas Docker
      ]
    }
  }
}
```

Luego ejecuta `npx @modelcontextprotocol/inspector --config ./mcp.json --server filesystem`

## Servidores MCP

Servidores MCP que utilicé o examiné:

### Servidor MCP de Sistema de Archivos

- [Servidor MCP de Sistema de Archivos](https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem)
- Uno de los [Servidores de Referencia](https://github.com/modelcontextprotocol/servers?tab=readme-ov-file#-reference-servers)

Configuración principal:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/Users/nombredeusuario/Desktop",
        "/path/to/other/allowed/dir"
      ]
    }
  }
}
```

## Servidores MCP

Servidores MCP que probé o planeo probar.

### Acceso al Sistema de Archivos

### Construcción Xcode

![Construcción Xcode](xcode_build.png)

- Habilita acciones de construcción de Xcode.
- https://github.com/cameroncooke/XcodeBuildMCP