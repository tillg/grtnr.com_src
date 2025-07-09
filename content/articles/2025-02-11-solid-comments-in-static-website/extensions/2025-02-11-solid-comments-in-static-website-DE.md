---
date: 2025-02-11
image: screenshot_comment.jpg
excerpt: Ich habe Kommentare zu meiner statischen Website hinzugefügt. So habe ich es gemacht.
translation: de
source_language: en
translator: gpt-4o
translate_date: 2025-07-09T14:55:34.028924
source_file: /Users/tgartner/git/grtnr.com_src/content/articles/2025-02-11-solid-comments-in-static-website/2025-02-11-solid-comments-in-static-website.md
generated_by: automatic-translation-plugin
---

**TL;DR:** Ich habe Kommentare zu meiner statischen Website hinzugefügt. So habe ich es gemacht – inklusive einiger technischer Details. Ich habe verschiedene mögliche Lösungen recherchiert, um die solideste zu finden, sie für alle Beiträge integriert und einen Zähler für die Anzahl der Kommentare in der Beitragsübersichtsseite hinzugefügt.

**2025-05-23 Update** Da ich von Jekyll zu [Pelican](https://getpelican.com) gewechselt bin, habe ich einige Details aktualisiert.

## Auswahl einer Lösung

Da ich vorhatte, mit dem neuen [Deep Research Model von OpenAI](https://openai.com/index/introducing-deep-research/) zu experimentieren, habe ich es zu diesem Thema ausprobiert: [lesen Sie hier gerne weiter](https://chatgpt.com/share/67a8aea4-9bc8-8009-917b-8855ebdd4776). Insgesamt war die Recherche hilfreich und ich habe mich letztendlich für [Giscus](https://giscus.app/) für die Kommentare entschieden. Teilweise, weil es am robustesten und zuverlässigsten erschien, teilweise, weil ich vor einigen Jahren wirklich schlechte Erfahrungen mit Disqus gemacht habe.

Die Wahl basierte auf den Kriterien, die ich dem Modell gegeben habe. Hier sind die wichtigsten:

- Kein selbst gehosteter Server – Ich möchte keinen Server verwalten (und bezahlen 😉).
- Datenportabilität – Die Kommentare können exportiert werden.
- Datenschutzfreundlich – Keine zusätzlichen Tracker oder Anzeigen über das hinaus, was ich bereits verwende (z.B. Google Analytics).
- Markdown-Unterstützung – Erlaubt reichhaltige Formatierung (Codeblöcke, etc.) geeignet für technische Diskussionen.
- Spamschutz – Hat Maßnahmen zur Reduzierung von Spam, insbesondere wenn anonyme oder nicht authentifizierte Kommentare erlaubt sind.

Die Werkzeuge, die Deep Research _analysiert_ hat, waren

- Giscus
- Utterances
- Staticman
- Commento
- Hyvor Talk
- Disqus
- Einige _selbstgemachte_ Lösungen

## Integration von Giscus

Im Anschluss an die Recherche bat ich das Modell, mir eine Schritt-für-Schritt-Anleitung zur Integration der Lösung zu geben. Dies war weitaus weniger zuverlässig als die erste Recherche, aber dennoch hilfreich.

Hier ist die Zusammenfassung (die Details sind im [Chat, den ich mit der KI hatte](https://chatgpt.com/share/67a8aea4-9bc8-8009-917b-8855ebdd4776)):

- Schritt 1: Aktivieren Sie GitHub Discussions für Ihr Repository. Das bedeutet das Repo, in das die statische Seite generiert wird (was manchmal nicht dasselbe ist wie die Quelle).
  - Gehen Sie zu Ihrem GitHub-Repository
  - Navigieren Sie zu Einstellungen > Allgemein.
  - Scrollen Sie nach unten zum Abschnitt Discussions und aktivieren Sie ihn.
- Zwischenschritt, den die KI nicht erwähnt hat: Installieren Sie Giscus für alle oder einige Ihrer Repos. [Hier](https://github.com/apps/giscus/installations/select_target)
  ![alt text](image.png)
- Schritt 2: Installieren und Konfigurieren Sie Giscus
  - Besuchen Sie die Giscus-Einrichtungsseite: https://giscus.app/.
  - Unter "Repository" geben Sie Ihren Reponamen ein. Sie sollten nun das grüne Häkchen sehen, dass Ihr Repo alle Kriterien für die Verwendung von Giscus erfüllt.
  - Die Option „Page discussion mapping“ bestimmt eine Beziehung zwischen Ihren Seiten, z.B. einem Artikel, und einer GitHub-Diskussion. Ich habe den Pfadnamen ausgewählt.
  - Für die Diskussionskategorie habe ich „general“ ausgewählt.
    Setzen Sie das Thema auf "Match OS" oder definieren Sie manuell den hellen und dunklen Modus.
    Klicken Sie auf "Copy Code", sobald Sie das <script>-Tag generiert haben.

![Giscus Features](giscus-features.png)

- Schritt 3: Fügen Sie Giscus zu Ihrer Jekyll-Postvorlage (oder Pelican 😀) hinzu. - - Schritt 4: Stylen Sie Giscus, um zum Lanyon-Theme zu passen. Diesen Schritt habe ich übersprungen, da das Styling für mich _nackt_ ziemlich gut aussah.
- Schritt 5: Zeigen Sie die Kommentaranzahl in Beitragszusammenfassungen an (siehe unten)
- Schritt 6: Änderungen committen und pushen - Klar...
- Schritt 7: Testen Sie Ihre Einrichtung

## Hinzufügen des Kommentarzählers

Nach einigem Herumprobieren und Glätten der Kanten funktionierte alles einwandfrei. Aber es gab ein Feature, das ich vermisste: Ich wollte die Anzahl der Kommentare eines Blogbeitrags auf der Beitragsübersichtsseite sehen.

![Kommentarzähler](screenshot_comment_counter.jpg){: style="box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);"}

Also habe ich ChatGPT erneut gestartet und ein weiteres [Rechercheergebnis](https://chatgpt.com/share/67ab5f69-4ddc-8009-8471-a35e00cb6a43) erhalten. Die groben Schritte sind:

- Schritt 1: Fügen Sie einen Platzhalter für die Kommentaranzahl hinzu. In meinem [`post_preview.html`](https://github.com/tillg/grtnr.com_2024/blob/main/_includes/post_preview.html) habe ich ein `<span>` hinzugefügt, das tatsächlich etwas anders sein musste als von der KI vorgeschlagen:

  ```html
  <span class="comment-count" data-giscus-comments="{{ post.url }}">
    <span class="comment-num">Kommentare zählen...</span>
  </span>
  ```

- Schritt 2: Fügen Sie JavaScript hinzu, um die Kommentaranzahl abzurufen. Ich habe ein Skript hinzugefügt, das die Kommentaranzahl von der GitHub Discussions API abruft und die Kommentaranzahl aktualisiert. Das vorgeschlagene Skript benötigte einige Korrekturen und endete in diesem [Event Listener](https://github.com/tillg/grtnr.com_2024/blob/main/assets/js/giscus-comments.js). Seien Sie nicht überrascht von den zwei Zeilen mit Bindestrichen (---) oben, ich werde sie unten erklären... Bemerkenswert hier sind
  - Umgang mit dem `accessToken` (unten erklärt)
  - Dieses Argument der grahQL-Abfrage: `categoryId: "DIC_kwDONYRp_c4Cm0cH"`. Dies ist die ID der Kategorie, die die Diskussionen des Repositories enthält.
  - Hinweis: Was mir beim Debuggen & Fixieren dieser Funktion geholfen hat, ist der [Github GraphQL Explorer](https://docs.github.com/en/graphql/overview/explorer).
- Schritt 3: Integrieren Sie das JavaScript in Ihre Jekyll-Site. In meinem Fall habe ich diesen Skriptverweis am Ende der [`default.html` Layout-Datei](https://github.com/tillg/grtnr.com_2024/blob/main/_layouts/default.html) hinzugefügt.
- Schritt 4: Testen Sie die Kommentaranzahl. Nach einigen Tests und Korrekturen funktionierte es schließlich lokal.

Die folgenden Aspekte haben mich ein oder zwei Stunden beschäftigt:

- Das `accessToken`, wo und wie man es bekommt
- Wie man den Zugriffstoken auf Github veröffentlicht, ohne dass der Token-Scanner und -Schutz eingreift