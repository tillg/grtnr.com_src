---
source-language: de
target-language: fr
last-created: 2025-07-03 17:23:23
hash-on-last-created: 6f5f3859413aa8ee235065659ab80dc33db60f32d1c181831639b1989c52de3e
translation-type: automatic
---

[de→fr] <div class="toc">
<ul>
<li><a href="#prompt-structure">Prompt Structure</a></li>
<li><a href="#cursorrules">Cursorrules</a></li>
<li><a href="#ai-rules-in-cursor-settings"><span class="caps">AI</span> Rules in Cursor Settings</a></li>
<li><a href="#helpful-small-prompts">Helpful small prompts</a></li>
<li><a href="#larger-prompts">Larger prompts</a><ul>
<li><a href="#summary-of-current-state">Summary of current state</a></li>
<li><a href="#unbiased-5050">Unbiased 50/50</a></li>
<li><a href="#one-paragraph-search-query">one-paragraph search query</a></li>
</ul>
</li>
<li><a href="#instructions">Instructions</a></li>
<li><a href="#other-tools">Other tools</a></li>
</ul>
</div>
<p>Last week end I discovered this video from David Ondrej: <a href="https://youtu.be/gYLNxUxVomY?si=1Q2x2UWgqy1RHvLt" rel="noopener noreferrer" target="_blank">I spent 400+ hours in Cursor, here’s what I learned</a>. The title is not super attractive, but the content was very helpful for me. So here are my notes so I can use all his tips and have the different prompts and snippets at hand to use them when coding.</p>
<iframe allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen="" frameborder="0" height="315" referrerpolicy="strict-origin-when-cross-origin" src="https://www.youtube.com/embed/gYLNxUxVomY?si=xQAMyMvQCsSwWztk" title="YouTube video player" width="560"></iframe>
<h2 id="prompt-structure">Prompt Structure</h2>
<p>The overall prompt structure that Deavid suggests:</p>
<ol>
<li>what we are doing</li>
<li>tag relevant files</li>
<li>how to execute // what not to do</li>
<li>context dump</li>
<li>repeat core instruction</li>
<li>output format</li>
</ol>
<h2 id="cursorrules">Cursorrules</h2>
<p><code>.cursorrules.md</code> is a file you put in your project top level directory that gives the <span class="caps">AI</span> more context about your project. Here is the structure of the file that David suggests:</p>
<div class="highlight"><pre><span></span><code><span class="gh"># PROJECT OVERVIEW</span>

<span class="gh"># PERSONALITY</span>

<span class="gh"># TECH STACK</span>

<span class="k">-</span><span class="w"> </span>choose a tech stack with super popular languages

<span class="gh"># ERROR FIXING PROCESS</span>

step 1: explain the error in simple terms
step 2: explain the solution in simple terms
step 3: show how to fix the error

<span class="gh"># BUILDING PROCESS</span>

<span class="gh"># Our - env variables</span>

backend/.env
frontend/. env

<span class="gh"># CURRENT FILE STRUCTURE</span>

Here you past the content of this command, so that Cursor knows about your project structure:
tree -L 4 -a -I 'node*modules | -git|\_pycache*|.DS\_$

<span class="gh"># GITHUB PUSH PROCESS</span>

<span class="gh"># IMPORTANT</span>

<span class="k">-</span><span class="w"> </span>Repeat the most important instructions.
</code></pre></div>
<p>He also strongly suggests to have a <code>.cursorignore</code> in which you list your <code>.env</code> files. This hinders chat and Composer to write in those files accidentally.</p>
<h2 id="ai-rules-in-cursor-settings"><span class="caps">AI</span> Rules in Cursor Settings</h2>
<p><span class="caps">AI</span> Rules are to be set in the cursor settings. They should not contain anything project specific, just coding principles that you would always want to apply. That’s the difference to the <code>.cursorrules</code> that also contain project specific details.</p>
<p>An example:</p>
<div class="highlight"><pre><span></span><code><span class="gh"># Fundamental Principles</span>

<span class="k">-</span><span class="w"> </span>Write clean, simple, readable code
<span class="k">-</span><span class="w"> </span>Implement features in the simplest possible way
<span class="k">-</span><span class="w"> </span>Keep files small and focused (&lt;200 lines)
<span class="k">-</span><span class="w"> </span>Test after every meaningful change
<span class="k">-</span><span class="w"> </span>Focus on core functionality before optimization
<span class="k">-</span><span class="w"> </span>Use clear, consistent naming
<span class="k">-</span><span class="w"> </span>Think thoroughly before coding. Write 2-3 reasoning paragraphs.
<span class="k">-</span><span class="w"> </span>ALWAYS write simple, clean and modular code.
<span class="k">-</span><span class="w"> </span>use clear and easy-to-understand language. write in short sentences.

<span class="gh"># Error Fixing</span>

<span class="k">-</span><span class="w"> </span>DO NOT JUMP TO CONCLUSIONS! Consider multiple possible causes before deciding.
<span class="k">-</span><span class="w"> </span>Explain the problem in plain English
<span class="k">-</span><span class="w"> </span>Make minimal necessary changes, changing as few lines of code as possible
<span class="k">-</span><span class="w"> </span>in case of strange errors, ask the user to perform a Perplexity web search in order to get the latest up-to-date information

<span class="gh"># Building Process</span>

<span class="k">-</span><span class="w"> </span>﻿﻿Verify each new feature works by telling the user how to test it
<span class="k">-</span><span class="w"> </span>﻿﻿DO NOT write complicated and confusing code. Opt for the simple &amp; modular approach.
<span class="k">-</span><span class="w"> </span>﻿﻿when not sure what to do, tell the user to perform a web search

<span class="gh"># Comments</span>

<span class="k">-</span><span class="w"> </span>ALWAYS try to add more helpful and explanatory comments into our code.
<span class="k">-</span><span class="w"> </span>NEVER delete old comments - unless they are obviously wrong / obsolete.
<span class="k">-</span><span class="w"> </span>Include LOTS of explanatory comments in your code. ALWAYS write well documented code.
<span class="k">-</span><span class="w"> </span>Document all changes and their reasoning IN THE COMMENTS YOU WRITE
<span class="k">-</span><span class="w"> </span>when writing comments, use clear and easy-to-understand language. write short sentences.
</code></pre></div>
<h2 id="helpful-small-prompts">Helpful small prompts</h2>
<p>David provides a list of helpful small prompts or prompt snippets. I copied some of them here for copy&amp;paste usage:</p>
<div class="highlight"><pre><span></span><code>Proceed like a Senior Developer with a focus on clear architecture.

The fewer lines of code the better.

Start by writing 3 reasoning paragraphs analyzing what the error might be. DO NOT JUMP TO CONCLUSIONS.

DO NOT STOP WORKING until…

Answer in short

DO NET DELETE COMMENTS

You should start the reasoning paragraph with lots of uncertainty, and slowly gain confidence as you think about the item more.
</code></pre></div>
<h2 id="larger-prompts">Larger prompts</h2>
<h3 id="summary-of-current-state">Summary of current state</h3>
<p>Used to summarize a compose flow and move over to a fresh compose dialoge.</p>
<div class="highlight"><pre><span></span><code>Before we proceed, I need you to give me a summary of the current state of the project.

Format this as 3 concise paragraphs, where you describe what we just did, what did not work, which files were updated/created, what mistakes to avoid, any key insights/lessons we’ve learned, what problems/errors we are facing,… and anything else a programmer might need to work productively on this project.

Write in a conversational yet informative tone, something like README file on GitHub that is super information dense and without any fluff or noise. DO NOT include any assumptions or theories, just the facts.

I expect to see three concise paragraphs, written as if you were giving instructions to another programmer and this was ALL you could tell him.
</code></pre></div>
<h3 id="unbiased-5050">Unbiased 50/50</h3>
<div class="highlight"><pre><span></span><code>BEFORE YOU ANSWER, i want you to write two detailed paragraphs, one arguing for each of these solutions - do not jump to conclusions, seriously consider both approaches

then, after you finish, tell me whether one of these solutions is obviously better than the other, and why.
</code></pre></div>
<h3 id="one-paragraph-search-query">one-paragraph search query</h3>
<div class="highlight"><pre><span></span><code>let's perform a web search. your task is to write a one-paragraph search query, as if you were telling a human researcher that to find, including all the relevant context. format the paragraph as clear instructions, commanding a researcher to find what we're looking for. ask for code snippets or technical details when relevant
</code></pre></div>
<h2 id="instructions">Instructions</h2>
<p>David suggests to have a directory <code>instructions</code> that contains md files with tips for the <span class="caps">AI</span>. This way you can reference these files from the Composer prompt. He also preferers this kind of instrauction files over refreencing @Docs in cursor, which seems not to work too good yet.</p>
<p>Instruction files that he mentioned:</p>
<ul>
<li><code>supabase.md</code>: A file that describes the structure of his database, so cursor knows about tables, fields, mandatoryness etc.</li>
<li><code>roadmap.md</code>: An explanation of the roadmap of your project.</li>
</ul>
<h2 id="other-tools">Other tools</h2>
<p>Besides Cursor David uses many other tools. Some of what he mentioned:</p>
<ul>
<li><a href="https://chatgpt.com" rel="noopener noreferrer" target="_blank">ChatGPT</a></li>
<li><a href="https://claude.ai" rel="noopener noreferrer" target="_blank">Claude</a> for side discussions with an advanced <span class="caps">AI</span>.</li>
<li><a href="https://www.perplexity.ai" rel="noopener noreferrer" target="_blank">Perplexity</a> for smart web searches.</li>
<li><a href="https://wisprflow.ai" rel="noopener noreferrer" target="_blank">WisprFlow</a> to speak rather than typing</li>
<li><a href="https://v0.dev" rel="noopener noreferrer" target="_blank">v0</a> a tool to create Web Apps in the browser by chatting withj an <span class="caps">AI</span>.</li>
<li><a href="https://lovable.dev" rel="noopener noreferrer" target="_blank">Lovable</a> for building backends, especially with <a href="https://supabase.com" rel="noopener noreferrer" target="_blank">Supabase</a></li>
<li><a href="https://bolt.new" rel="noopener noreferrer" target="_blank">Bolt</a> to build web sites.</li>
</ul>