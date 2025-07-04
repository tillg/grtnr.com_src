---
Translation: de
Source-Language: en
Translator: gpt-4
Translate-Date: 2025-07-04T17:04:05.134300
Source-File: /Users/tgartner/git/grtnr.com_src/content/articles/2025-02-11-solid-comments-in-static-website/2025-02-11-solid-comments-in-static-website.md
Generated-By: automatic-translation-plugin
---

```markdown
---
date: 2025-02-11
image: screenshot_comment.jpg
excerpt: Ich habe Kommentare zu meiner statischen Website hinzugefügt. Hier ist, wie ich es gemacht habe.
---

**TL;DR:** Ich habe Kommentare zu meiner statischen Website hinzugefügt. Hier ist, wie ich es gemacht habe - einschließlich einiger technischer Details. Ich habe verschiedene mögliche Lösungen recherchiert, um die solideste zu finden, sie für alle Beiträge integriert und einen Zähler für die Anzahl der Kommentare auf der Beitragsübersichtsseite hinzugefügt.

**2025-05-23 Update** Da ich von Jekyll zu [Pelican](https://getpelican.com) gewechselt bin, habe ich einige Details aktualisiert.

## Auswahl einer Lösung

Da ich vorhatte, mit dem neuen [Deep Research Model von OpenAI](https://openai.com/index/introducing-deep-research/) zu experimentieren, habe ich es mit diesem Thema ausprobiert: [lesen Sie hier gerne weiter](https://chatgpt.com/share/67a8aea4-9bc8-8009-917b-8855ebdd4776). Insgesamt war die Recherche hilfreich und ich habe mich letztendlich für [Giscus](https://giscus.app/) für die Kommentare entschieden. Teilweise, weil es sich am robustesten und zuverlässigsten anfühlte, teilweise, weil ich vor einigen Jahren wirklich schlechte Erfahrungen mit Disqus gemacht habe.

Die Wahl basierte auf den Kriterien, die ich dem Modell gegeben habe. Hier sind die wichtigsten:

- Kein selbstgehosteter Server – Ich möchte keinen Server verwalten (und bezahlen 😉).
- Datenportabilität – Die Kommentare können exportiert werden.
- Datenschutzfreundlich – keine zusätzlichen Tracker oder Anzeigen über das hinaus, was ich bereits verwende (z.B. Google Analytics).
- Markdown-Unterstützung – ermöglicht reichhaltige Formatierung (Code-Blöcke usw.) für technische Diskussionen.
- Spam-Schutz – verfügt über Maßnahmen zur Reduzierung von Spam, insbesondere wenn anonyme oder nicht authentifizierte Kommentare erlaubt sind.

Die Tools, die Deep Research _analysiert_ hat, waren:

- Giscus
- Utterances
- Staticman
- Commento
- Hyvor Talk
- Disqus
- Einige _selbstgemachte_ Lösungen

## Integration von Giscus

Im Anschluss an die Recherche habe ich das Modell gebeten, mir eine Schritt-für-Schritt-Anleitung zur Integration der Lösung zu geben. Dies war weit weniger zuverlässig als die erste Recherche, aber dennoch hilfreich.

Hier ist die Zusammenfassung der Schritte (die Details finden Sie im [Chat, den ich mit der KI hatte](https://chatgpt.com/share/67a8aea4-9bc8-8009-917b-8855ebdd4776)):

- Schritt 1: Aktivieren Sie GitHub Discussions für Ihr Repository. Das bedeutet das Repo, in das die statische Seite generiert wird (was manchmal nicht dasselbe wie die Quelle ist).
  - Gehen Sie zu Ihrem GitHub-Repository
  - Navigieren Sie zu Einstellungen > Allgemein.
  - Scrollen Sie nach unten zum Abschnitt Discussions und aktivieren Sie ihn.
- Zwischenschritt, den die KI nicht erwähnt hat: Installieren Sie Giscus für alle oder einige Ihrer Repos. [Hier](https://github.com/apps/giscus/installations/select_target)
  ![alt text](image.png)
- Schritt 2: Installieren und Konfigurieren Sie Giscus
  - Besuchen Sie die Giscus-Setup-Seite: https://giscus.app/.
  - Unter "Repository" geben Sie Ihren Repo-Namen ein. Sie sollten nun das grüne Häkchen sehen, dass Ihr Repo alle Kriterien für die Verwendung von Giscus erfüllt.
  - Die Option „Page discussion mapping“ legt eine Beziehung zwischen Ihren Seiten, z.B. einem Artikel, und einer GitHub-Diskussion fest. Ich habe den Pfadnamen ausgewählt.
  - Für die Diskussionskategorie habe ich „general“ ausgewählt.
    Setzen Sie das Thema auf "Match OS" oder definieren Sie manuell den hellen und dunklen Modus.
    Klicken Sie auf "Code kopieren", sobald Sie das <script>-Tag generiert haben.

![Giscus Features](giscus-features.png)

- Schritt 3: Fügen Sie Giscus zu Ihrer Jekyll-Postvorlage hinzu (oder Pelican 😀). - - Schritt 4: Stylen Sie Giscus, um zum Lanyon-Thema zu passen. Diesen Schritt habe ich übersprungen, da das Styling für mich _nackt_ ziemlich gut aussah.
- Schritt 5: Anzeigen der Kommentaranzahl in Beitragszusammenfassungen (siehe unten)
- Schritt 6: Änderungen committen und pushen - Na klar...
- Schritt 7: Testen Sie Ihr Setup

## Hinzufügen des Kommentarzählers

Nachdem ich ein wenig herumgebastelt und die Kanten geglättet hatte, funktionierte alles einwandfrei. Aber es gab eine Funktion, die ich vermisste: Ich wollte die Anzahl der Kommentare, die ein Blogbeitrag hat, auf der Beitragsübersichtsseite sehen.

![Kommentarzähler](screenshot_comment_counter.jpg){: style="box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);"}

Also habe ich ChatGPT erneut gestartet und ein weiteres [Rechercheergebnis](https://chatgpt.com/share/67ab5f69-4ddc-8009-8471-a35e00cb6a43) erhalten. Die groben Schritte sind:

- Schritt 1: Fügen Sie einen Platzhalter für die Kommentaranzahl hinzu. In meinem [`post_preview.html`](https://github.com/tillg/grtnr.com_2024/blob/main/_includes/post_preview.html) habe ich ein `<span>` hinzugefügt, das tatsächlich ein wenig anders sein musste als das, was die KI vorgeschlagen hat:

  ```html
  <span class="comment-count" data-giscus-comments="{{ post.url }}">
    <span class="comment-num">Kommentare zählen...</span>
  </span>
  ```

- Schritt 2: Fügen Sie JavaScript hinzu, um die Kommentaranzahl abzurufen. Ich habe ein Skript hinzugefügt, das die Kommentaranzahl von der GitHub Discussions API abruft und die Kommentaranzahl aktualisiert. Das vorgeschlagene Skript benötigte einige Korrekturen und endete in diesem [Event Listener](https://github.com/tillg/grtnr.com_2024/blob/main/assets/js/giscus-comments.js). Seien Sie nicht überrascht von den zwei Zeilen mit Bindestrichen (---) oben, ich werde sie unten erklären... Bemerkenswert hier sind
  - Umgang mit dem `accessToken` (unten erklärt)
  - Dieses Argument der grahQL-Abfrage: `categoryId: "DIC_kwDONYRp_c4Cm0cH"`. Dies ist die ID der Kategorie, die die Diskussionen des Repositories enthält.
  - Hinweis: Was mir beim Debuggen und Beheben dieser Funktion geholfen hat, ist der [Github GraphQL Explorer](https://docs.github.com/en/graphql/overview/explorer).
- Schritt 3: Fügen Sie das JavaScript in Ihre Jekyll-Site ein. In meinem Fall habe ich diesen Skriptverweis am Ende der [`default.html` Layout-Datei](https://github.com/tillg/grtnr.com_2024/blob/main/_layouts/default.html) hinzugefügt.
- Schritt 4: Testen Sie die Kommentaranzahl. Nach einigen Tests und Korrekturen funktionierte es schließlich lokal.

Die folgenden Aspekte haben mich ein oder zwei Stunden beschäftigt:

- Das `accessToken`, wo und wie man es bekommt
- Wie man das Zugriffstoken auf Github veröffentlicht, ohne dass der Token-Scanner und -Schutz eingreift
```