---
date: 2015-12-19
image: search.jpg
excerpt: Wie man eine Suchfunktion zu einer statischen Website mit der Google Custom Search Engine und einer Bootstrap-Navigationsleiste hinzufügt.
title: Suche zu einer statischen Website hinzufügen
translation: de
source_language: en
source_hash: b726deb5e0431efb8a963f41c4db8668a942537dbd3e3ded4ee4eb154965b74b
translator: gpt-4o-2024-08-06
translate_date: 2026-02-28T14:26:10.073367+00:00
generated_by: simplified-translation-system
---

Jetzt habe ich also eine statische Website, die von jBake generiert wird. Bisher so gut. Aber was ist eine Website ohne Suche? Suche ist ein Muss. Also, wie fügen wir einer statischen Website eine Suchfunktion hinzu? Ganz einfach: Wir nutzen die Custom Search-Funktionalität der Suchgiganten ;)

Dies sind die Schritte, die ich unternommen habe, um dorthin zu gelangen:

## Erstelle die Custom Search Engine

Nichts einfacher als das: Geh einfach zur [Google CSE-Seite](http://www.google.com/cse) und erstelle sie. Der Prozess ist selbsterklärend: Du brauchst einen Namen für deine Suchmaschine und gibst an, welche Inhalte verfügbar gemacht werden sollen. In meinem Fall wäre das alles von [tillgartner.com](https://tillgartner.com) [Seite existiert nicht mehr] und das war's im Grunde. Wir werden am Ende zu dieser Seite zurückkehren, um das Aussehen und die Bedienung der Ergebnisse fein abzustimmen.

![Google CSE-Verwaltung](Custom_Search_-_Basic.jpg)

Das Einzige, was wir hier benötigen, ist der Code, um die Suche einzubetten. Diesen Code erhältst du, indem du auf den Button "**Get Code**" klickst.

## Suchfeld hinzufügen

Als Nächstes brauchen wir ein Suchfeld auf unseren Seiten. Ich möchte ein Suchfeld oben rechts auf jeder Seite der gesamten Website. Also füge ich es zur Freemarker-Vorlage hinzu, die das Menü erstellt.

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

_Hinweis:_ Ich habe den Code auf meiner Seite und im obigen Code am 29.12.2015 korrigiert. Der Code für den Button, der erscheint, wenn die Breite des Bildschirms das Menü zusammenklappen lässt, fehlte. Nur für den Fall, dass du dies früher gelesen hast und dich fragst, warum es jetzt anders ist...

Ich fand, dass der Teil des Menüs und wie es sich zusammenklappt, nicht trivial war. Die beste Erklärung, die ich gefunden habe, war [dieses Video](https://bootstrapbay.com/blog/bootstrap-tutorial-navbar/).

Es ist das Standard-Bootstrap-Menü-Gewusel. Was in unserem Fall besonders ist, ist das `action`-Attribut im Formular, das auf die Suchergebnisseite verweist (in meinem Fall `search.html` genannt).

Das Ergebnis ist ein schickes kleines Suchfeld in der oberen rechten Ecke:

![Suchfeld](search_box.jpg)

## Suchergebnisseite

Zu guter Letzt brauchen wir die Suchergebnisseite. Diese Seite wird vom Suchformular, das wir gerade erstellt haben, aufgerufen (d.h. verlinkt). Ihre URL wird etwa so aussehen:

```url
http://tillgartner.com/search.html?q=huhu
```

In meinem Fall wird die Suchergebnisseite **nur** das Suchergebnis enthalten. Falls der Benutzer seine Suche ändern möchte, hat er immer noch das allgegenwärtige Suchfeld in der oberen rechten Ecke.
Die Suchergebnisseite wird den Code enthalten, den wir beim Konfigurieren der Custom Search Engine kopiert haben. In meinem Fall sieht die gesamte Markdown-Datei so aus:

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

Es hat eine Weile gedauert, bis ich herausgefunden habe, wie man Markdown sagt, dass dies reines HTML ist und es als solches genommen werden sollte, ohne es zu transformieren oder zu zitieren. Die Lösung war das `<div markdown="0">`-Tag.

## Ressourcen

Einige Lektüre, die mir geholfen hat, meinen Weg zu finden:

- [Erstelle deine eigene Suchmaschine](http://www.google.com/cse)
- [Wie man ein Google Custom Search Popup in eine Bootstrap-Navigationsleiste integriert](http://www.cambiaresearch.com/articles/84/how-to-integrate-a-google-custom-search-popup-in-a-bootstrap-navbar)
- [Implementierung des Suchfelds, von Google](https://developers.google.com/custom-search/docs/tutorial/implementingsearchbox)