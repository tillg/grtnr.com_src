---
date: 2025-05-18
image: mcp.png
excerpt: Notes sur les découvertes et les _compréhensions_ autour du Model Context Protocol alias MCP.
title: Terrain de jeu MCP
tags: Tech, IA
translation: fr
source_language: en
source_hash: 5b6a2f789f63743b4bd4c86550d220561bd96627e391e09ab952c23229592dd5
translator: gpt-4o-2024-08-06
translate_date: 2026-02-28T09:40:39.531105+00:00
generated_by: simplified-translation-system
---

Notes sur les découvertes et les _compréhensions_ autour du [Model Context Protocol alias \_MCP](https://modelcontextprotocol.io/introduction).

[TOC]

## Questions

Questions ouvertes que j'ai.

- Puis-je exécuter Claude avec différentes configurations de serveur MCP ? C'est-à-dire que j'ai une configuration par projet, disons une pour mon projet Python (incluant uniquement l'accès à mon répertoire de projet Python), une pour mon projet Swift/Xcode (avec un répertoire et des outils différents).
- Test : Expérimenter avec MCP Inspector et [Xcode Build MCP Server](https://github.com/cameroncooke/XcodeBuildMCP).

## Accéder à un serveur MCP

Lors de la recherche et de la découverte éventuelle d'un serveur MCP pour mon cas d'utilisation, je trouve utile de les manipuler pour _comprendre_ quels outils le LLM obtient. Le moyen le plus simple de le faire est avec le [MCP Inspector](https://github.com/modelcontextprotocol/inspector).

Commencez :

```bash
# Assurez-vous d'avoir installé une version récente de nodeJs (dans mon cas avec nvm)
nvm use 24
npx @modelcontextprotocol/inspector node build/index.js

# Il télécharge et démarre le client MCP UI et le sert localement.
```

**Configuration**

L'Inspector conserve tout ce que vous tapez dans la barre latérale dans le localStorage, mais pour des configurations répétables, vous pouvez enregistrer un petit fichier JSON et le pointer avec le CLI :

```json
// mcp.json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/Users/yourname/Projects", // lecture/écriture
        "/Users/yourname/Notes", // lecture/écriture
        "/Users/yourname/Code" // lecture seule ? ajoutez ',ro' si vous utilisez Docker
      ]
    }
  }
}
```

Ensuite, exécutez `npx @modelcontextprotocol/inspector --config ./mcp.json --server filesystem`

## Serveurs MCP

Serveurs MCP que j'ai utilisés ou examinés :

### Serveur MCP de système de fichiers

- [Serveur MCP de système de fichiers](https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem)
- L'un des [Serveurs de Référence](https://github.com/modelcontextprotocol/servers?tab=readme-ov-file#-reference-servers)

Configuration principale :

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

## Serveurs MCP

Serveurs MCP que j'ai testés ou que je prévois de tester.

### Accès au système de fichiers

### Construction Xcode

![Construction Xcode](xcode_build.png)

- Active les actions de construction Xcode.
- https://github.com/cameroncooke/XcodeBuildMCP