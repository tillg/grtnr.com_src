---
title: Terrain de jeu MCP
image: mcp.png
summary: Notes sur les découvertes et les _compréhensions_ autour du [Protocole de Contexte de Modèle alias _MCP](https://modelcontextprotocol.io/introduction).
tags: Tech, IA
Translation: fr
Source-Language: en
Translator: gpt-4o
Translate-Date: 2025-07-09T07:28:01.172427
Source-File: /Users/tgartner/git/grtnr.com_src/content/articles/2025-05-18-mcp-playground/2025-05-18-mcp-playground.md
Generated-By: automatic-translation-plugin
---

Notes sur les découvertes et les _compréhensions_ autour du [Protocole de Contexte de Modèle alias _MCP](https://modelcontextprotocol.io/introduction).

[TOC]

## Questions

Questions ouvertes que j'ai.

- Puis-je exécuter Claude avec différentes configurations de serveur MCP ? C'est-à-dire que j'ai une configuration par projet, disons une pour mon projet Python (y compris l'accès uniquement à mon répertoire de projet Python), une pour mon projet Swift/Xcode (avec un répertoire différent et des outils différents).
- Test : Jouez avec l'Inspecteur MCP et le [Serveur MCP de Construction Xcode](https://github.com/cameroncooke/XcodeBuildMCP).

## Accéder à un serveur MCP

Lors de la recherche et finalement de la découverte d'un serveur MCP pour mon cas d'utilisation, je trouve utile de jouer avec eux, afin de _comprendre_ quels outils le LLM obtient. La façon la plus simple de faire cela est avec l'[Inspecteur MCP](https://github.com/modelcontextprotocol/inspector).

Pour commencer :

```bash
# Assurez-vous d'avoir installé une version récente de nodeJs (dans mon cas avec nvm)
nvm use 24
npx @modelcontextprotocol/inspector node build/index.js

# Il télécharge & démarre le Client UI MCP et le sert localement.
```

**Configuration**

L'Inspecteur conserve tout ce que vous tapez dans la barre latérale dans le localStorage, mais pour des configurations répétables, vous pouvez sauvegarder un petit fichier JSON et pointer le CLI vers celui-ci :

```json
// mcp.json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/Users/votre_nom/Projects", // lecture/écriture
        "/Users/votre_nom/Notes", // lecture/écriture
        "/Users/votre_nom/Code" // lecture seule ? ajoutez ',ro' si vous utilisez Docker
      ]
    }
  }
}
```

Ensuite, exécutez `npx @modelcontextprotocol/inspector --config ./mcp.json --server filesystem`

## Serveurs MCP

Serveurs MCP que j'ai utilisés ou examinés :

### Serveur MCP de Système de Fichiers

- [Serveur MCP de Système de Fichiers](https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem)
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
        "/Users/nom_utilisateur/Bureau",
        "/chemin/vers/autre/répertoire/autorisé"
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