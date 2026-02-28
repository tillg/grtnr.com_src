---
date: 2025-05-18
image: mcp.png
excerpt: Notizen über Erkenntnisse und _Verständnisse_ rund um das Model Context Protocol, auch bekannt als MCP.
title: MCP Playground
tags: Tech, AI
translation: de
source_language: en
source_hash: 5b6a2f789f63743b4bd4c86550d220561bd96627e391e09ab952c23229592dd5
translator: gpt-4o-2024-08-06
translate_date: 2026-02-28T09:40:37.397487+00:00
generated_by: simplified-translation-system
---

Notizen über Erkenntnisse und _Verständnisse_ rund um das [Model Context Protocol aka \_MCP](https://modelcontextprotocol.io/introduction).

[TOC]

## Fragen

Offene Fragen, die ich habe.

- Kann ich Claude mit verschiedenen MCP-Serverkonfigurationen ausführen? D.h. ich habe eine Konfiguration pro Projekt, sagen wir eine für mein Python-Projekt (einschließlich Zugriff nur auf mein Python-Projektverzeichnis), eine für mein Swift/Xcode-Projekt (mit einem anderen Verzeichnis und anderen Tools).
- Test: Mit dem MCP Inspector und [Xcode Build MCP Server](https://github.com/cameroncooke/XcodeBuildMCP) herumspielen.

## Zugriff auf einen MCP-Server

Wenn ich nach einem MCP-Server für meinen Anwendungsfall suche und schließlich einen finde, finde ich es hilfreich, mit ihnen herumzuspielen, um zu _verstehen_, welche Tools das LLM erhält. Der einfachste Weg, dies zu tun, ist mit dem [MCP Inspector](https://github.com/modelcontextprotocol/inspector).

Loslegen:

```bash
# Stelle sicher, dass du eine aktuelle Version von nodeJs installiert hast (in meinem Fall mit nvm)
nvm use 24
npx @modelcontextprotocol/inspector node build/index.js

# Es lädt & startet den MCP UI Client und stellt ihn lokal bereit.
```

**Konfiguration**

Der Inspector speichert alles, was du in die Seitenleiste eingibst, in localStorage, aber für wiederholbare Setups kannst du eine kleine JSON-Datei speichern und das CLI darauf verweisen:

```json
// mcp.json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/Users/yourname/Projects", // lesen/schreiben
        "/Users/yourname/Notes", // lesen/schreiben
        "/Users/yourname/Code" // nur lesen? füge ',ro' hinzu, wenn du Docker verwendest
      ]
    }
  }
}
```

Dann führe `npx @modelcontextprotocol/inspector --config ./mcp.json --server filesystem` aus.

## MCP-Server

MCP-Server, die ich verwendet oder angesehen habe:

### Filesystem MCP Server

- [Filesystem MCP Server](https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem)
- Einer der [Referenzserver](https://github.com/modelcontextprotocol/servers?tab=readme-ov-file#-reference-servers)

Hauptkonfiguration:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/Users/username/Desktop",
        "/path/to/other/allowed/dir"
      ]
    }
  }
}
```

## MCP-Server

MCP-Server, die ich getestet habe oder testen möchte.

### Dateisystemzugriff

### Xcode Build

![Xcode Build](xcode_build.png)

- Ermöglicht Xcode-Build-Aktionen.
- https://github.com/cameroncooke/XcodeBuildMCP