---
layout: post
title: Mes notes du RC3 2020
slug: my-notes-from-rc3-2020
date_published: 2020-12-28T21:52:54.000Z
date_updated: 2021-12-06T11:52:04.000Z
tags: 
image: image-1-rc3.png
translation: fr
source_language: en
source_hash: 3f331ccbf78ad8a586c4e3cc6edadcaff49a25311e10dd4b5185c9fa796bd357
translator: gpt-4o-2024-08-06
translate_date: 2025-07-18T22:28:43.274178
generated_by: simplified-translation-system
---

Cette année (décembre 2020), j'avais un billet pour le RC3. Ils étaient distribués gratuitement, mais se sont épuisés rapidement. J'étais donc fier et j'ai passé pas mal de temps à regarder les sessions du CCC.

Toutes les conférences sont disponibles [ici](https://media.ccc.de/c/rc3). J'en ai regardé certaines (en partie ou en totalité).

En plus des conférences, il y avait un _Monde 2D_ - qui n'a jamais fonctionné pour moi 😢 (et ma connexion réseau était plutôt bonne !) :
![Connexion perdue](image-8.png)

### Une introduction à Tox

Un nouveau service de messagerie. Mieux que l'email, Matrix et toutes les autres plateformes de messagerie. Avantages :

- Pas de serveurs centraux, aucun moyen de désactiver l'une des fonctionnalités de cryptage.
- Fonctionnalités de Tox : Messagerie instantanée, Appels vocaux, Appels vidéo, Partage d'écran, Partage de fichiers, Groupes.

Il était intéressant d'apprendre qu'il existe de NOMBREUX protocoles de chat. Et beaucoup d'entre eux ont des objectifs similaires : Garder les données sécurisées, et parfois même les métadonnées. Il semble qu'il faille décider si votre protocole cache vraiment les métadonnées (généralement cela se fait en utilisant Tor en dessous) ou s'il fournit une faible latence pour permettre également la voix et la vidéo.

Questions qui me viennent à l'esprit :

- Offre-t-il vraiment des appels vidéo, ou lance-t-il simplement d'autres appels vidéo (c'est-à-dire Jitsi) - tout comme Matrix ?
- Les appels vocaux et vidéo sont-ils également vraiment cryptés ? Parce que Cisco Webex ne crypte pas ses appels vidéo (seulement les chats)

![Fonctionnalités clés](image-rc3.png)

À propos de l'intervenant :

![À propos](image-10.png)

![Prendre contact](image-11.png)

### Der netzpolitische Wetterbericht

Écouté en direct, par Markus Beckedahl (de [netzpolitik.org](https://netzpolitik.org))

Qu'est-ce qui s'est passé l'année dernière, quels sujets sont brûlants ?

- Les gouvernements veulent des clés pour écouter les communications cryptées.
- Les chevaux de Troie d'État exploitent des failles de sécurité - au lieu de les combler rapidement.
- Les appareils SmartHome ont été convoqués comme témoins devant les tribunaux : Alexa a raconté ce qu'on lui avait demandé.
- La loi BND a été classée comme inconstitutionnelle - belle expérience 😀. Mais une nouvelle loi BND a été rapidement adoptée...
- Le [podcast avec Idil Baydar](https://podcasts.apple.com/lu/podcast/npp-211-zu-fünft-mit-i-dil-baydar/id1281525246?i=1000492613815) - un peu cru mais assez intéressant, en somme recommandable.

J'ai ensuite arrêté, c'était assez ennuyeux...

![Zu fünft...](image-2.png)

### Intégrité numérique de la personne humaine, un nouveau droit fondamental mise à jour 2020

L'intervenant (Alexis Roussel, Suisse) explique comment les Droits de l'Homme devraient / pourraient être étendus à l'espace numérique.

Quelques points intéressants qu'il a soulevés :

- Il y a un bug dans le RGPD (Article 2) : Le gouvernement peut accéder à toutes les données en cas de danger. Description trop vague et qui brise l'idée de base du RGPD.
- En Suisse, certains cantons mettent à jour leur Constitution pour l'étendre à l'espace numérique.

Je suis passé pour 15 minutes, je n'ai pas écouté jusqu'à la fin...

![Wikipedia](image-3.png)

### Les blocs de construction de la décentralisation

L'intervenant est [Will Scott](https://www.linkedin.com/in/willrscott/). Il semble être un spécialiste d'IPFS.

- Actuellement, le plus grand système décentralisé est BitTorrent

![Chiffres de BitTorrent](image-4.png)

- Un autre grand système distribué est [Mastodon](https://github.com/tootsuite/mastodon) "Le Fediverse". _Qu'est-ce que c'est que ça ?_

![Mastodon](image-5.png)

![Chiffres de Mastodon](image-6.png)

- IPFS a dépassé les 2M d'utilisateurs
- SSB (Secure Scuttlebutt) 100K utilisateurs
- Bitcoin : 1M de comptes actifs

![Modèles de décentralisation](Screenshot-2020-12-28-at-19.37.34.png)

- Centralisé : Facebook. Fédéré : matrix. Réseau maillé décentralisé ?

Les véritables blocs de construction de la décentralisation :

- DHT : Tables de hachage distribuées
- BFT (Tolérance aux pannes byzantines) Consensus. Il semble y avoir une explication [ici](https://academy.binance.com/en/articles/byzantine-fault-tolerance-explained).
- Le consensus peut être atteint par _Proof of Work_ ou par _Proof of Stake_.

Il a ensuite discuté des limitations de ces blocs de construction : Volume, nombre d'entités, combien de sauts --> latence, bande passante (surtout en upload par rapport au download),

![Exposition des métadonnées](image-7.png)

### Autres conférences...

...que j'aimerais écouter :

- [Gestion de projets avec Gitea](https://media.ccc.de/v/rc3-channels-2020-70-verwaltung-von-projekten-mit-gitea) : Après la vente de Github à Microsoft, beaucoup se sont demandé s'il n'existait pas d'alternatives sur lesquelles on aurait un contrôle total. J'utilise depuis deux ans l'application Go Gitea à la fois pour des projets professionnels et Open Source. Gitea a l'avantage que les obstacles à l'installation, à la maintenance et à l'utilisation sont clairs et rapidement surmontés.
  Remarque : j'ai essayé le lien le 28.12.20, il semblait incorrect, on parlait de tout autres sujets (également intéressant : Internationaly Netzpolitik)
- [Salle de classe numérique](https://media.ccc.de/v/rc3-11591-digitales_klassenzimmer) : Dans cet atelier, les enseignants, élèves et autres intéressés peuvent découvrir les logiciels scolaires libres. BigBlueButton ? Moodle ? Nextcloud ? Ce sont les salles de classe numériques de l'avenir.
- [Ouverture du rC3](https://media.ccc.de/v/rc3-11583-rc3_eroffnung)

Et c'était mon programme pour le Jour 3 (mardi 29 décembre) :

![Programme Jour 3](image-9.png)