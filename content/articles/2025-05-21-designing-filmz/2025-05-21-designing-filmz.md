---
Tags: tech
Title: Designing Filmz 
Date: 2025-05-21
---

Some time ago I built a little iOS App called Filmz: keep track of films and shows you want to see or you have seen. Keep personal additional information like “how did I like it?” (I.e. my personal rating), “For what audience would I recommend it?” (Adults, kids, family) “When and where did I see it” etc. And then comes sharing: passing on film recommendations to friends, either one film at a time or lists. 

As I didn’t know any Swift back then, I built it in a _vibe coding_ style, fully supported by AI (back then mainly Cursor.ai). This gave me a fast start, but I was lost once I wanted to add more complex features that required a well structured code base. And since I didn’t know much about Swift, I couldn’t do it either. Vibe debugging doesn’t work - yet…

So here I start again, and with a different approach: I first want to sketch the structure I would like to have, lay out my design principles, the SDKs I want to use (or the ones I don’t want to use) and then start coding. I also plan to use AI support (my Swift know how is still mediocre), but I hope that this way I can create a code base that is more structured, and that will be able to evolve while staying structured. 

## Main entities

These are the main entities I’m dealing with. 

### ImdbFilm

A film from [IMDB](https://www.imdb.com) - even though I don’t use the real IMDB (API usage is really expensive) but [OMDB, the Open Movie DataBase](https://www.omdbapi.com) that can be queried via a much cheaper API. I use ImdbFilm objects and references throughout my code base to reference a “Film”. 

ImdbFilms are also what I get back from my search (as JSON). And example:

```json
{“Title”:”Harry Potter and the Sorcerer’s Stone”,
”Year”:”2001”,
”Rated”:”PG”,”Released”:”16 Nov 2001”,”Runtime”:”152 min”,
”Genre”:”Adventure, Family, Fantasy”,”Director”:”Chris Columbus”,
”Writer”:”J.K. Rowling, Steve Kloves”,
”Actors”:”Daniel Radcliffe, Rupert Grint, Emma Watson”,
”Plot”:”An orphaned boy enrolls in a school of wizardry, where he learns the truth about himself, his family and the terrible evil that haunts the magical world.”,”Language”:”English, Latin”,”Country”:”United Kingdom, United States”,
”Awards”:”Nominated for 3 Oscars. 20 wins & 74 nominations total”,
”Poster”:”https://m.media-amazon.com/images/M/MV5BNTU1MzgyMDMtMzBlZS00YzczLThmYWEtMjU3YmFlOWEyMjE1XkEyXkFqcGc@._V1_SX300.jpg”,
”Ratings”:[{“Source”:”Internet Movie Database”,”Value”:”7.7/10”},{“Source”:”Rotten Tomatoes”,”Value”:”80%”},{“Source”:”Metacritic”,”Value”:”65/100”}],
”Metascore”:”65”,”imdbRating”:”7.7”,”imdbVotes”:”904,094”,”imdbID”:”tt0241527”,”Type”:”movie”,”DVD”:”N/A”,”BoxOffice”:”$318,886,962”,”Production”:”N/A”,”Website”:”N/A”,”Response”:”True”}
```

Fields of ImdbFilm:

- ID - my internal ID
- Title
- year
- genre - an array of strings
- plot
- Actors - an array of strings
- poster - the url of a poster image
- imdbRating 
- rottenTomatoeRating

Some of the fields are optional, ID and Title are mandatory. At later stages we could think of keeping track of real actor objects and more, but for a start we are good. 


### MyFilm

A film that is on my list. Either one I have seen, or one I plan to see. 

Fields of MyFilm:

- ID
- ImdbId - the film that we talk about
- seen - Boolean 
- seenDate 
- myRating 
- myComments 
- recommendedAudience - kids, adults, family, bodyCountSavvy

## Services

## UI Objects

## Principles

### System boundaries

### Use structs

### Pass on IDs and services

- Passing on IDs and services in my app. Every logic or UI component that needs the entire object gets it from the service
- Take care of caching later