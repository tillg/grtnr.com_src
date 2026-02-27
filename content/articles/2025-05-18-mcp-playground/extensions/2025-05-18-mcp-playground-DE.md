---
image: mcp.png
excerpt: Notizen zu Erkenntnissen und _Verständnissen_ rund um [Model Context Protocol aka _MCP](https://modelcontextprotocol.io/introduction).
title: MCP Playground
tags: Tech, AI
translation: de
source_language: en
source_hash: 1c3aa9204681ea87c2ca715d9af8e740b8cb8c72ceb2b9f76e05481d19cc10f3
translator: gpt-4o-2024-08-06
translate_date: 2026-02-27T10:29:28.764418+00:00
generated_by: simplified-translation-system
---

Notizen zu Erkenntnissen und _Verständnissen_ rund um [Model Context Protocol aka \_MCP](https://modelcontextprotocol.io/introduction).

[TOC]

## Fragen

Offene Fragen, die ich habe.

- Kann ich Claude mit verschiedenen MCP Server-Konfigurationen ausführen? D.h. ich habe eine Konfiguration pro Projekt, sagen wir eine für mein Python-Projekt (einschließlich Zugriff nur auf mein Python-Projektverzeichnis), eine für mein Swift/Xcode-Projekt (mit einem anderen Verzeichnis und anderen Tools).
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

Der Inspector speichert alles, was du in die Seitenleiste eingibst, in localStorage, aber für wiederholbare Setups kannst du eine kleine JSON-Datei speichern und die CLI darauf verweisen:

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

Dann führe `npx @modelcontextprotocol/inspector --config ./mcp.json --server filesystem` aus

## MCP-Server

MCP-Server, die ich verwendet oder angeschaut habe:

### Filesystem MCP Server

- [Filesystem MCP Server](https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem)
- Einer der [Referenz-Server](https://github.com/modelcontextprotocol/servers?tab=readme-ov-file#-reference-servers)

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