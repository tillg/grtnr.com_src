---
date: 2025-02-11
image: screenshot_comment.jpg
excerpt: Ich habe Kommentare zu meiner statischen Website hinzugefügt. So habe ich es gemacht.
translation: de
source_language: en
source_hash: 2874836d1997d93f99163c8d5920e3aa86f8eb8e596cd57752d40a8b3f87c875
translator: gpt-4o-2024-08-06
translate_date: 2025-07-18T21:56:25.404633
generated_by: simplified-translation-system
---

**Kurzfassung:** Ich habe Kommentare zu meiner statischen Website hinzugefügt. So habe ich es gemacht - einschließlich einiger technischer Details. Ich habe verschiedene mögliche Lösungen recherchiert, um die solideste zu finden, sie für alle Beiträge integriert und einen Zähler für die Anzahl der Kommentare in der Beitragsübersichtsseite hinzugefügt.

**Aktualisierung vom 2025-05-23** Da ich von Jekyll zu [Pelican](https://getpelican.com) gewechselt bin, habe ich einige Details aktualisiert.

## Auswahl einer Lösung

Da ich vorhatte, mit dem neuen [Deep Research Model von OpenAI](https://openai.com/index/introducing-deep-research/) zu experimentieren, habe ich es zu diesem Thema ausprobiert: [lesen Sie hier gerne weiter](https://chatgpt.com/share/67a8aea4-9bc8-8009-917b-8855ebdd4776). Insgesamt war die Recherche hilfreich und ich habe mich letztendlich für [Giscus](https://giscus.app/) für die Kommentare entschieden. Teilweise, weil es sich am robustesten und zuverlässigsten anfühlte, teilweise, weil ich vor einigen Jahren wirklich schlechte Erfahrungen mit Disqus gemacht habe.

Die Wahl basierte auf den Kriterien, die ich dem Modell gegeben habe. Hier sind die wichtigsten:

- Kein selbst gehosteter Server – Ich möchte keinen Server verwalten (und bezahlen 😉).
- Datenportabilität – die Kommentare können exportiert werden.
- Datenschutzfreundlich – keine zusätzlichen Tracker oder Werbung über das hinaus, was ich bereits verwende (z. B. Google Analytics).
- Markdown-Unterstützung – ermöglicht reichhaltige Formatierung (Codeblöcke usw.), die für technische Diskussionen geeignet ist.
- Spamschutz – verfügt über Maßnahmen zur Reduzierung von Spam, insbesondere wenn anonyme oder nicht authentifizierte Kommentare zugelassen werden.

Die Werkzeuge, die Deep Research _analysiert_ hat, waren

- Giscus
- Utterances
- Staticman
- Commento
- Hyvor Talk
- Disqus
- Einige _selbstgemachte_ Lösungen

## Integration von Giscus

Im Anschluss an die Recherche habe ich das Modell gebeten, mir eine Schritt-für-Schritt-Anleitung zur Integration der Lösung zu geben. Diese war weit weniger zuverlässig als die erste Recherche, aber dennoch hilfreich.

Hier ist die Zusammenfassung (die Details finden Sie im [Chat, den ich mit der KI hatte](https://chatgpt.com/share/67a8aea4-9bc8-8009-917b-8855ebdd4776)):

- Schritt 1: Aktivieren Sie GitHub Discussions für Ihr Repository. Das bedeutet das Repo, in das die statische Seite generiert wird (was manchmal nicht dasselbe ist wie die Quelle).
  - Gehen Sie zu Ihrem GitHub-Repository
  - Navigieren Sie zu Einstellungen > Allgemein.
  - Scrollen Sie nach unten zum Abschnitt Diskussionen und aktivieren Sie ihn.
- Zwischenschritt, den die KI nicht erwähnt hat: Installieren Sie Giscus für alle oder einige Ihrer Repos. [Hier](https://github.com/apps/giscus/installations/select_target)
  ![alt text](image.png)
- Schritt 2: Installieren Sie Giscus und konfigurieren Sie es
  - Besuchen Sie die Giscus-Setup-Seite: https://giscus.app/.
  - Unter "Repository" geben Sie Ihren Repo-Namen ein. Sie sollten jetzt das grüne Häkchen sehen, dass Ihr Repo alle Kriterien für die Verwendung von Giscus erfüllt.
  - Die Option „Page discussion mapping“ bestimmt eine Beziehung zwischen Ihren Seiten, z. B. einem Artikel, und einer GitHub-Diskussion. Ich habe den Pfadnamen ausgewählt.
  - Für die Diskussionskategorie habe ich „allgemein“ ausgewählt.
    Stellen Sie das Thema auf "Match OS" oder definieren Sie manuell den hellen und dunklen Modus.
    Klicken Sie auf "Code kopieren", sobald Sie das <script>-Tag generiert haben.

![Giscus Features](giscus-features.png)

- Schritt 3: Fügen Sie Giscus zu Ihrer Jekyll-Post-Vorlage hinzu (oder Pelican 😀). - - Schritt 4: Stylen Sie Giscus, um zum Lanyon-Theme zu passen. Diesen Schritt habe ich übersprungen, da das Styling für mich _nackt_ ziemlich gut aussah.
- Schritt 5: Anzeigen der Kommentaranzahl in Beitragszusammenfassungen (siehe unten)
- Schritt 6: Änderungen committen und pushen - Na klar...
- Schritt 7: Testen Sie Ihr Setup

## Hinzufügen des Kommentarzählers

Nachdem ich ein wenig herumprobiert und die Kanten geglättet hatte, funktionierte alles einwandfrei. Aber es gab ein Feature, das ich vermisste: Ich wollte die Anzahl der Kommentare sehen, die ein Blogbeitrag auf der Beitragsübersichtsseite hat.

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
- Schritt 3: Binden Sie das JavaScript in Ihre Jekyll-Site ein. In meinem Fall habe ich diesen Skriptverweis am Ende der [`default.html` Layout-Datei](https://github.com/tillg/grtnr.com_2024/blob/main/_layouts/default.html) hinzugefügt.
- Schritt 4: Testen Sie die Kommentaranzahl. Nach einigen Tests und Korrekturen funktionierte es schließlich lokal.

Die folgenden Aspekte haben mich ein oder zwei Stunden beschäftigt:

- Das `accessToken`, wo und wie man es bekommt
- Wie man das Zugriffstoken auf Github veröffentlicht, ohne dass der Token-Scanner und -Schutz eingreift