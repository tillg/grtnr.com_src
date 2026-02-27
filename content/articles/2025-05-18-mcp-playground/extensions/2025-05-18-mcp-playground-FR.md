---
image: mcp.png
excerpt: Notes sur les découvertes et les _compréhensions_ autour de [Model Context Protocol alias _MCP](https://modelcontextprotocol.io/introduction).
title: MCP Playground
tags: Tech, IA
translation: fr
source_language: en
source_hash: 1c3aa9204681ea87c2ca715d9af8e740b8cb8c72ceb2b9f76e05481d19cc10f3
translator: gpt-4o-2024-08-06
translate_date: 2026-02-27T10:14:31.079862+00:00
generated_by: simplified-translation-system
---

Notes sur les découvertes et les _compréhensions_ autour de [Model Context Protocol alias \_MCP](https://modelcontextprotocol.io/introduction).

[TOC]

## Questions

Questions ouvertes que j'ai.

- Puis-je exécuter Claude avec différentes configurations de serveur MCP ? C'est-à-dire que j'ai une configuration par projet, disons une pour mon projet Python (incluant l'accès uniquement à mon répertoire de projet Python), une pour mon projet Swift/Xcode (avec un répertoire différent et des outils différents).
- Test : Expérimenter avec MCP Inspector et [Xcode Build MCP Server](https://github.com/cameroncooke/XcodeBuildMCP).

## Accéder à un serveur MCP

Lors de la recherche et de la découverte éventuelle d'un serveur MCP pour mon cas d'utilisation, je trouve utile de les expérimenter afin de _comprendre_ quels outils l'LLM obtient. Le moyen le plus simple de le faire est avec le [MCP Inspector](https://github.com/modelcontextprotocol/inspector).

Pour commencer :

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

### Serveur MCP Filesystem

- [Serveur MCP Filesystem](https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem)
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

### Accès au Système de Fichiers

### Construction Xcode

![Construction Xcode](xcode_build.png)

- Permet les actions de construction Xcode.
- https://github.com/cameroncooke/XcodeBuildMCP