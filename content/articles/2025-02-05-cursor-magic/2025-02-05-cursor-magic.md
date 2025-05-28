---
date: 2025-02-05
image: david_cursor_magic.png
excerpt: I found this video of a dev with LOTS of helpful tips on how to use Cursor - here are my take aways.
---

[TOC]

Last week end I discovered this video from David Ondrej: [I spent 400+ hours in Cursor, here’s what I learned](https://youtu.be/gYLNxUxVomY?si=1Q2x2UWgqy1RHvLt). The title is not super attractive, but the content was very helpful for me. So here are my notes so I can use all his tips and have the different prompts and snippets at hand to use them when coding.

<iframe width="560" height="315" src="https://www.youtube.com/embed/gYLNxUxVomY?si=xQAMyMvQCsSwWztk" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

## Prompt Structure

The overall prompt structure that Deavid suggests:

1.  what we are doing
2.  tag relevant files
3.  how to execute // what not to do
4.  context dump
5.  repeat core instruction
6.  output format

## Cursorrules

`.cursorrules.md` is a file you put in your project top level directory that gives the AI more context about your project. Here is the structure of the file that David suggests:

```markdown
# PROJECT OVERVIEW

# PERSONALITY

# TECH STACK

- choose a tech stack with super popular languages

# ERROR FIXING PROCESS

step 1: explain the error in simple terms
step 2: explain the solution in simple terms
step 3: show how to fix the error

# BUILDING PROCESS

# Our - env variables

backend/.env
frontend/. env

# CURRENT FILE STRUCTURE

Here you past the content of this command, so that Cursor knows about your project structure:
tree -L 4 -a -I 'node*modules | -git|\_pycache*|.DS\_$

# GITHUB PUSH PROCESS

# IMPORTANT

- Repeat the most important instructions.
```

He also strongly suggests to have a `.cursorignore` in which you list your `.env` files. This hinders chat and Composer to write in those files accidentally.

## AI Rules in Cursor Settings

AI Rules are to be set in the cursor settings. They should not contain anything project specific, just coding principles that you would always want to apply. That's the difference to the `.cursorrules` that also contain project specific details.

An example:

```markdown
# Fundamental Principles

- Write clean, simple, readable code
- Implement features in the simplest possible way
- Keep files small and focused (<200 lines)
- Test after every meaningful change
- Focus on core functionality before optimization
- Use clear, consistent naming
- Think thoroughly before coding. Write 2-3 reasoning paragraphs.
- ALWAYS write simple, clean and modular code.
- use clear and easy-to-understand language. write in short sentences.

# Error Fixing

- DO NOT JUMP TO CONCLUSIONS! Consider multiple possible causes before deciding.
- Explain the problem in plain English
- Make minimal necessary changes, changing as few lines of code as possible
- in case of strange errors, ask the user to perform a Perplexity web search in order to get the latest up-to-date information

# Building Process

- ﻿﻿Verify each new feature works by telling the user how to test it
- ﻿﻿DO NOT write complicated and confusing code. Opt for the simple & modular approach.
- ﻿﻿when not sure what to do, tell the user to perform a web search

# Comments

- ALWAYS try to add more helpful and explanatory comments into our code.
- NEVER delete old comments - unless they are obviously wrong / obsolete.
- Include LOTS of explanatory comments in your code. ALWAYS write well documented code.
- Document all changes and their reasoning IN THE COMMENTS YOU WRITE
- when writing comments, use clear and easy-to-understand language. write short sentences.
```

## Helpful small prompts

David provides a list of helpful small prompts or prompt snippets. I copied some of them here for copy&paste usage:

```text
Proceed like a Senior Developer with a focus on clear architecture.

The fewer lines of code the better.

Start by writing 3 reasoning paragraphs analyzing what the error might be. DO NOT JUMP TO CONCLUSIONS.

DO NOT STOP WORKING until…

Answer in short

DO NET DELETE COMMENTS

You should start the reasoning paragraph with lots of uncertainty, and slowly gain confidence as you think about the item more.
```

## Larger prompts

### Summary of current state

Used to summarize a compose flow and move over to a fresh compose dialoge.

```text
Before we proceed, I need you to give me a summary of the current state of the project.

Format this as 3 concise paragraphs, where you describe what we just did, what did not work, which files were updated/created, what mistakes to avoid, any key insights/lessons we’ve learned, what problems/errors we are facing,… and anything else a programmer might need to work productively on this project.

Write in a conversational yet informative tone, something like README file on GitHub that is super information dense and without any fluff or noise. DO NOT include any assumptions or theories, just the facts.

I expect to see three concise paragraphs, written as if you were giving instructions to another programmer and this was ALL you could tell him.
```

### Unbiased 50/50

```text
BEFORE YOU ANSWER, i want you to write two detailed paragraphs, one arguing for each of these solutions - do not jump to conclusions, seriously consider both approaches

then, after you finish, tell me whether one of these solutions is obviously better than the other, and why.
```

### one-paragraph search query

```text
let's perform a web search. your task is to write a one-paragraph search query, as if you were telling a human researcher that to find, including all the relevant context. format the paragraph as clear instructions, commanding a researcher to find what we're looking for. ask for code snippets or technical details when relevant
```

## Instructions

David suggests to have a directory `instructions` that contains md files with tips for the AI. This way you can reference these files from the Composer prompt. He also preferers this kind of instrauction files over refreencing @Docs in cursor, which seems not to work too good yet.

Instruction files that he mentioned:

- `supabase.md`: A file that describes the structure of his database, so cursor knows about tables, fields, mandatoryness etc.
- `roadmap.md`: An explanation of the roadmap of your project.

## Other tools

Besides Cursor David uses many other tools. Some of what he mentioned:

- [ChatGPT](https://chatgpt.com)
- [Claude](https://claude.ai) for side discussions with an advanced AI.
- [Perplexity](https://www.perplexity.ai) for smart web searches.
- [WisprFlow](https://wisprflow.ai) to speak rather than typing
- [v0](https://v0.dev) a tool to create Web Apps in the browser by chatting withj an AI.
- [Lovable](https://lovable.dev) for building backends, especially with [Supabase](https://supabase.com)
- [Bolt](https://bolt.new) to build web sites.
