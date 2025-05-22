---
title: MCP Playground
image: mcp.png
summary: Notes about findings and _understandings_ around [Model Context Protocol aka _MCP](https://modelcontextprotocol.io/introduction).
tags: Tech, AI
---

Notes about findings and _understandings_ around [Model Context Protocol aka _MCP](https://modelcontextprotocol.io/introduction).

[TOC]

## Questions

Open questions that I have.

* Can I run Claude with different MCP Server configurations? I.e. I have one configuration per project, say one for my Python project (including access only to my Python project directory), one for my Swift/Xcode project (with a different dir and different tools).
* Test: Play around with MCP Inspector and [Xcode Build MCP Server](https://github.com/cameroncooke/XcodeBuildMCP).

## Accessing a MCP server

When searching and eventually finding an MCP server for my use case, I find it helpful to play around with them, in order to _understand_ what tooling the LLM gets. The easiest way to do this is with the [MCP Inspector](https://github.com/modelcontextprotocol/inspector).

Get going:

```bash
# Make sure you have installed a recent version of nodeJs (in my case with nvm)
nvm use 24
npx @modelcontextprotocol/inspector node build/index.js

# It downloads & starts the MCP UI Client and serves it locally.
```

**Configuration**

The Inspector keeps whatever you type in the sidebar in localStorage, but for repeatable setups you can save a tiny JSON file and point the CLI to it:
```json
// mcp.json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/Users/yourname/Projects",      // read/write
        "/Users/yourname/Notes",         // read/write
        "/Users/yourname/Code",          // read-only? add ',ro' if you use Docker
      ]
    }
  }
}
```

Then run `npx @modelcontextprotocol/inspector --config ./mcp.json --server filesystem`

## MCP Servers

MCP Servers I used or looked at:

### Filesystem MCP Server

* [Filesystem MCP Server](https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem)
* One of the [Reference Servers](https://github.com/modelcontextprotocol/servers?tab=readme-ov-file#-reference-servers) 

Main config: 

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

## MCP Servers

MCP Servers I tested or plan to test.

### FileSystem Access

### Xcode Build

![Xcode Build](xcode_build.png)

* Enables Xcode build actions.
* https://github.com/cameroncooke/XcodeBuildMCP
 