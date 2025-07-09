---
title: MCP Spielplatz
image: mcp.png
summary: Notizen über Erkenntnisse und _Verständnisse_ rund um [Model Context Protocol aka _MCP](https://modelcontextprotocol.io/introduction).
tags: Technik, KI
Translation: de
Source-Language: en
Translator: gpt-4o
Translate-Date: 2025-07-09T07:57:28.836077
Source-File: /Users/tgartner/git/grtnr.com_src/content/articles/2025-05-18-mcp-playground/2025-05-18-mcp-playground.md
Generated-By: automatic-translation-plugin
---

Notizen über Erkenntnisse und _Verständnisse_ rund um [Model Context Protocol aka _MCP](https://modelcontextprotocol.io/introduction).

[TOC]

## Fragen

Offene Fragen, die ich habe.

- Kann ich Claude mit verschiedenen MCP Server Konfigurationen betreiben? D.h. ich habe eine Konfiguration pro Projekt, sagen wir eine für mein Python-Projekt (mit Zugriff nur auf mein Python-Projektverzeichnis), eine für mein Swift/Xcode-Projekt (mit einem anderen Verzeichnis und anderen Tools).
- Test: Spielen Sie mit dem MCP Inspector und [Xcode Build MCP Server](https://github.com/cameroncooke/XcodeBuildMCP) herum.

## Zugriff auf einen MCP-Server

Bei der Suche und schließlich dem Finden eines MCP-Servers für meinen Anwendungsfall finde ich es hilfreich, mit ihnen herumzuspielen, um zu _verstehen_, welche Werkzeuge das LLM erhält. Der einfachste Weg, dies zu tun, ist mit dem [MCP Inspector](https://github.com/modelcontextprotocol/inspector).

So geht's:

```bash
# Stellen Sie sicher, dass Sie eine aktuelle Version von nodeJs installiert haben (in meinem Fall mit nvm)
nvm use 24
npx @modelcontextprotocol/inspector node build/index.js

# Es lädt & startet den MCP UI Client und stellt ihn lokal zur Verfügung.
```

**Konfiguration**

Der Inspector behält alles, was Sie in die Seitenleiste eingeben, im localStorage, aber für wiederholbare Setups können Sie eine winzige JSON-Datei speichern und die CLI darauf hinweisen:

```json
// mcp.json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/Users/IhrName/Projects", // lesen/schreiben
        "/Users/IhrName/Notes", // lesen/schreiben
        "/Users/IhrName/Code" // nur lesen? fügen Sie ',ro' hinzu, wenn Sie Docker verwenden
      ]
    }
  }
}
```

Führen Sie dann `npx @modelcontextprotocol/inspector --config ./mcp.json --server filesystem` aus

## MCP-Server

MCP-Server, die ich verwendet oder angesehen habe:

### Dateisystem MCP Server

- [Dateisystem MCP Server](https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem)
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
        "/Users/Benutzername/Desktop",
        "/pfad/zum/anderen/erlaubten/verzeichnis"
      ]
    }
  }
}
```

## MCP-Server

MCP-Server, die ich getestet habe oder plane zu testen.

### Dateisystemzugriff

### Xcode Build

![Xcode Build](xcode_build.png)

- Ermöglicht Xcode Build-Aktionen.
- https://github.com/cameroncooke/XcodeBuildMCP