---
title: MCP Spielplatz
image: mcp.png
summary: Notizen zu Erkenntnissen und _Verständnissen_ rund um das [Model Context Protocol aka _MCP](https://modelcontextprotocol.io/introduction).
tags: Technik, KI
Translation: de
Source-Language: en
Translator: gpt-4
Translate-Date: 2025-07-04T16:31:52.941932
Source-File: /Users/tgartner/git/grtnr.com_src/content/articles/2025-05-18-mcp-playground/2025-05-18-mcp-playground.md
Generated-By: automatic-translation-plugin
---

Notizen zu Erkenntnissen und _Verständnissen_ rund um das [Model Context Protocol aka _MCP](https://modelcontextprotocol.io/introduction).

[TOC]

## Fragen

Offene Fragen, die ich habe.

- Kann ich Claude mit verschiedenen MCP Server Konfigurationen betreiben? D.h., ich habe eine Konfiguration pro Projekt, sagen wir eine für mein Python-Projekt (mit Zugriff nur auf mein Python-Projektverzeichnis), eine für mein Swift/Xcode-Projekt (mit einem anderen Verzeichnis und anderen Tools).
- Test: Spielen Sie mit dem MCP Inspector und dem [Xcode Build MCP Server](https://github.com/cameroncooke/XcodeBuildMCP) herum.

## Zugriff auf einen MCP-Server

Bei der Suche und schließlich der Findung eines MCP-Servers für meinen Anwendungsfall finde ich es hilfreich, mit ihnen herumzuspielen, um zu _verstehen_, welche Werkzeuge das LLM erhält. Der einfachste Weg, dies zu tun, ist mit dem [MCP Inspector](https://github.com/modelcontextprotocol/inspector).

So geht's:

```bash
# Stellen Sie sicher, dass Sie eine aktuelle Version von nodeJs installiert haben (in meinem Fall mit nvm)
nvm use 24
npx @modelcontextprotocol/inspector node build/index.js

# Es lädt & startet den MCP UI Client und bedient ihn lokal.
```

**Konfiguration**

Der Inspector behält alles, was Sie in die Seitenleiste eingeben, im localStorage, aber für wiederholbare Setups können Sie eine kleine JSON-Datei speichern und die CLI darauf hinweisen:

```json
// mcp.json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/Users/IhrName/Projects", // Lesen/Schreiben
        "/Users/IhrName/Notes", // Lesen/Schreiben
        "/Users/IhrName/Code" // Nur lesen? Fügen Sie ',ro' hinzu, wenn Sie Docker verwenden
      ]
    }
  }
}
```

Führen Sie dann `npx @modelcontextprotocol/inspector --config ./mcp.json --server filesystem` aus

## MCP Server

MCP Server, die ich verwendet oder angesehen habe:

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
        "/Users/Benutzername/Desktop",
        "/pfad/zum/anderen/erlaubten/verzeichnis"
      ]
    }
  }
}
```

## MCP Server

MCP Server, die ich getestet habe oder plane zu testen.

### Dateisystemzugriff

### Xcode Build

![Xcode Build](xcode_build.png)

- Ermöglicht Xcode-Build-Aktionen.
- https://github.com/cameroncooke/XcodeBuildMCP