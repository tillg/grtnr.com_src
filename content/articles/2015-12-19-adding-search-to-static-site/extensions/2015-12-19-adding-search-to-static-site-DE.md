---
title: Hinzufügen von Suchfunktionen zu einer statischen Website
date: 2015-12-19
tag: tech
image: search.jpg
translation: de
source_language: en
source_hash: bb933a9c5df8d9686c53b4eb84eca0b768e16afe8e564efcca1875d3bf1e8e5f
translator: gpt-4o-2024-08-06
translate_date: 2025-07-18T22:20:42.848307
generated_by: simplified-translation-system
---

Jetzt habe ich also eine statische Website, die von jBake generiert wird. Bis jetzt, so gut. Aber was ist eine Website ohne Suche? Eine Suche ist ein Muss. Wie fügen wir also einer statischen Website eine Suchfunktion hinzu? Ganz einfach: Wir nutzen die Custom Search-Funktionalität der Suchgiganten ;)

Dies sind die Schritte, die ich unternommen habe, um dorthin zu gelangen:

## Erstellen der benutzerdefinierten Suchmaschine

Nichts leichter als das: Gehen Sie einfach zur [Google CSE-Seite](http://www.google.com/cse) und erstellen Sie sie. Der Prozess ist selbsterklärend: Sie benötigen einen Namen für Ihre Suchmaschine und geben an, welche Inhalte verfügbar gemacht werden sollen. In meinem Fall wäre dies alles von [tillgartner.com](https://tillgartner.com) und das war's im Wesentlichen. Am Ende kehren wir zu dieser Seite zurück, um das Aussehen und das Gefühl der Ergebnisse zu optimieren.

![Google CSE-Verwaltung](Custom_Search_-_Basic.jpg)

Das Einzige, was wir von hier benötigen, ist der Code, um die Suche einzubetten. Sie erhalten diesen Code, indem Sie auf den Button "**Code abrufen**" klicken.

## Hinzufügen des Suchfeldes

Als nächstes benötigen wir ein Suchfeld auf unseren Seiten. Ich möchte ein Suchfeld oben rechts auf jeder Seite der gesamten Website. Also füge ich es zur Freemarker-Vorlage hinzu, die das Menü erstellt.

In meinem Fall sieht das `menu.ftl` ungefähr so aus:

```javascript
    <!-- Feste Navigationsleiste -->
    <nav class="navbar navbar-default navbar-fixed-top" role="navigation">
      <div class="container-fluid">
        <div class="navbar-header">
            <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
                <span class="sr-only">Navigation umschalten</span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
            </button>
          <a class="navbar-brand" href="/">tillgartner.com</a>
        </div>
        <div class="navbar-collapse collapse">
          <ul class="nav navbar-nav">
            <li><a href="/recipe/recipe.html">Rezepte</a></li>
            <li><a href="/about.html">Über</a></li>
          </ul>
          <div class="col-sm-3 col-md-3 pull-right">
              <form class="navbar-form" role="search" action="/search.html">
            <div class="input-group">
                <input type="text" class="form-control" placeholder="Suche" name="q">
                <div class="input-group-btn">
                    <button class="btn btn-default" type="submit">
                        <i class="glyphicon glyphicon-search"></i>
                    </button>
                </div>
            </div>
         </form>
         </div>
        </div><!--/.nav-collapse -->
      </div>
    </nav>
    <div class="container">
```

_Hinweis:_ Ich habe den Code auf meiner Website und im obigen Code am 29.12.2015 korrigiert. Der Code für den Button, der erscheint, wenn die Breite des Bildschirms das Menü zusammenklappen lässt, fehlte. Nur für den Fall, dass Sie dies früher gelesen haben und sich fragen, warum es jetzt anders ist...

Ich fand, dass der Teil des Menüs und wie es zusammenklappt, nicht trivial war. Die beste Erklärung, die ich fand, war [dieses Video](https://bootstrapbay.com/blog/bootstrap-tutorial-navbar/).

Es ist das Standard-Bootstrap-Menü-Gewackel. Was in unserem Fall besonders ist, ist das `action`-Attribut im Formular, das auf die Suchergebnisseite verweist (in meinem Fall `search.html` genannt).

Das Ergebnis ist ein kleines, ordentliches Suchfeld in der oberen rechten Ecke:

![Suchfeld](search_box.jpg)

## Suchergebnisseite

Zu guter Letzt benötigen wir die Suchergebnisseite. Diese Seite wird vom Suchformular, das wir gerade erstellt haben, aufgerufen (d.h. verlinkt). Ihre URL wird etwa so aussehen:

```url
http://tillgartner.com/search.html?q=huhu
```

In meinem Fall wird die Suchergebnisseite **nur** das Suchergebnis enthalten. Falls der Benutzer seine Suche ändern möchte, hat er immer noch das allgegenwärtige Suchfeld in der oberen rechten Ecke.
Die Suchergebnisseite wird den Code enthalten, den wir beim Konfigurieren der benutzerdefinierten Suchmaschine kopiert haben. In meinem Fall sieht die gesamte Markdown-Datei so aus:

```javascript
title=Suche
type=page
date=2015-12-17
status=published
~~~~~~

<script>
  (function() {
    var cx = 'XXX_Your_code:goes_here_XXX';
    var gcse = document.createElement('script');
    gcse.type = 'text/javascript';
    gcse.async = true;
    gcse.src = (document.location.protocol == 'https:' ? 'https:' : 'http:') +
        '//www.google.com/cse/cse.js?cx=' + cx;
    var s = document.getElementsByTagName('script')[0];
    s.parentNode.insertBefore(gcse, s);
  })();
</script>
<div markdown = "0"><gcse:searchresults-only>Suchergebnisse...</gcse:searchresults-only></div>
```

Es hat eine Weile gedauert, bis ich herausgefunden habe, wie man Markdown mitteilt, dass dies reines HTML ist und es als solches ohne Transformation oder Zitierung akzeptieren sollte. Die Lösung war das `<div markdown="0">`-Tag.

## Ressourcen

Einige Lektüren, die mir geholfen haben, meinen Weg zu finden:

- [Erstellen Sie Ihre eigene Suchmaschine](http://www.google.com/cse)
- [Wie man ein Google Custom Search Popup in eine Bootstrap-Navigationsleiste integriert](http://www.cambiaresearch.com/articles/84/how-to-integrate-a-google-custom-search-popup-in-a-bootstrap-navbar)
- [Implementierung des Suchfeldes, von Google](https://developers.google.com/custom-search/docs/tutorial/implementingsearchbox)