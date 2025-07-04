## Multilingual site

- Articles are translated automatically already
- Now a multilingual site structure should be created.
- The user should be able on every page to switch between German, English and French
- Once he selected a language, he should stay in this language when following links inside our website.

### Architecture

The translated articles, pages etc. should be transformed & copied into the target web structure during the build process.

### File organization

We have following directory structure in our sources:

```text
content/
    articles/
        2025-07-03-something-interesting/
            2025-07-03-something-interesting.md
            extensions/
                2025-07-03-something-interesting-DE.md
                2025-07-03-something-interesting-FR.md
```

Architecture question: What is the ideal directory & file structure we want to have in our output?
