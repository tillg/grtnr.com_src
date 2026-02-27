---
date: 2026-02-26
image: address-book.svg
excerpt: L'application de contacts que je veux vraiment — un système unique pour toutes mes relations sur iPhone, Mac et iPad, avec des listes au lieu de comptes, une capture intelligente et un réseau de conférences intégré.
title: Peoplez
tags: tech, logicielquonveut
translation: fr
source_language: en
source_hash: c237f7a349ef05208e12c357029768aa52b6b47934421bfb12bf0e3270527102
translator: gpt-4o-2024-08-06
translate_date: 2026-02-27T10:20:55.399734+00:00
generated_by: simplified-translation-system
---

J'ai du mal à garder mes contacts à jour. La plupart d'entre eux sont "presque corrects" et il est difficile de suivre les changements ou les nouvelles personnes que je rencontre. Je ne veux pas d'un CRM. Je veux un système de contacts unique qui fonctionne sur mon iPhone, Mac et iPad — un système qui sait faire la différence entre mon collègue et mon voisin, mais qui ne m'oblige pas à gérer cette séparation manuellement.

Ce système n'existe pas encore. Je l'appelle **Peoplez**.

## Ce qui ne va pas avec le statu quo

L'application Contacts d'Apple prend déjà en charge plusieurs comptes. L'idée est : contacts professionnels dans Exchange, contacts personnels dans iCloud. En pratique, cela crée plus de problèmes que cela n'en résout :

- **Doublons partout** — La même personne se retrouve dans plusieurs comptes parce que vous l'avez ajoutée dans différents contextes.
- **Mauvais paramètres par défaut** — Vous enregistrez un contact et il atterrit dans le mauvais compte. Maintenant, il est invisible dans le mauvais contexte.
- **Pas de chevauchement** — Certaines personnes sont à la fois professionnelles et personnelles. Les comptes imposent un choix binaire.
- **Recherche fragmentée** — Vous pouvez afficher tous les comptes à la fois, mais il n'y a aucun moyen de filtrer par "montrez-moi juste mes contacts professionnels" sans masquer des comptes entiers.

## Ce que Peoplez ferait différemment

### Un système, des listes au lieu de comptes

Tous les contacts vivent au même endroit. Professionnel et privé ne sont pas des comptes séparés — ce sont des **listes**. Par défaut, je vois tout le monde. Quand je veux me concentrer, je filtre par liste.

- Un contact peut être sur plusieurs listes : "Travail", "Amis", "XConf 2026", "Groupe de ski"
- Les listes sont définies par l'utilisateur, non dictées par l'infrastructure de synchronisation
- La vue par défaut montre tous les contacts — pas de masquage, pas de basculement de comptes

### Capture intelligente — réseau de conférences intégré

Quand je suis à une conférence et que je rencontre quelqu'un, je le capture de trois manières :

**Photo de badge** — Les badges sont "presque des contacts" mais pas des contacts. Une photo de badge est une entrée brute. Peoplez extrairait le nom et l'entreprise (OCR), créerait un brouillon de contact et conserverait la photo du badge comme provenance ("rencontré à ...").

**Lien LinkedIn** — Le chemin le plus rapide pour "obtenir l'identité correcte". [LinkedIn positionne les codes QR](https://www.linkedin.com/help/linkedin/answer/a525286/using-a-linkedin-qr-code-to-connect-with-members) comme un moyen de se connecter avec les personnes que vous rencontrez hors ligne. Peoplez récupérerait les connexions faites sur LinkedIn et enrichirait ou mettrait à jour le contact - en une action au lieu de trois. Peoplez rechercherait les liens LinkedIn récemment ajoutés et me proposerait de les ajouter, avec la possibilité d'ajouter des données.

**Note rapide** — Parfois, vous ne voulez pas sortir votre téléphone en pleine conversation. Vous vous souvenez simplement : _"Anna — travaille chez X — a parlé du déploiement iOS — à suivre en mars."_ Peoplez transformerait cette note en contact (ou la ferait correspondre à un existant) et ajouterait le contexte sous forme de données structurées, pas de texte aléatoire qui se perd.

Dans tous les cas : capturer d'abord, organiser plus tard. Le contact atterrit dans mes Contacts, et je décide à quelles listes il appartient quand je suis prêt.

### Ce qu'un contact devrait retenir

Un contact utile n'est pas juste un nom et un numéro. Pour les personnes que je rencontre lors d'événements, je veux savoir :

- **Quand** les ai-je rencontrées ?
- **Où** les ai-je rencontrées ? (événement + ville)
- **De quoi** avons-nous parlé ? (sujets)
- **Où** travaillent-elles ? (entreprise + rôle)
- **Quand** devrais-je faire un suivi ?

Apple et Google ont tous deux un champ de notes sur les contacts — il est simplement sous-utilisé parce que rien ne le remplit automatiquement. Peoplez en ferait la norme, pas l'exception. Peoplez est juste une porte / un conduit organisé vers mes Contacts - les données des contacts sont toujours stockées dans mon application Contacts Apple.

### Correspondance, dédoublonnage, enrichissement

Lorsqu'un nouveau contact arrive, Peoplez :

1. **Correspondance** — "Cela ressemble à Anna Müller déjà dans vos contacts — mettre à jour ?"
2. **Dédoublonnage** — Fusionner les doublons à travers ce qui était autrefois des comptes séparés
3. **Enrichissement** — Ajouter entreprise, titre, lien de profil (lorsque permis), conserver la source

### Fonctionne sur tous les appareils Apple

Peoplez stocke les données de contact dans les Contacts d'Apple qui se synchronisent sur iPhone, Mac et iPad. Les mêmes contacts, les mêmes listes, les mêmes notes. Un système — pas trois applications avec trois histoires de synchronisation différentes.

## L'application que je veux dans ma pile

Peoplez n'est pas un CRM. Ce n'est pas une "application de réseautage". C'est une porte vers les Contacts Apple : **un système unifié pour toutes les personnes de votre vie**, avec des listes au lieu de silos de comptes, une capture intelligente pour la réalité désordonnée des rencontres, et un contexte riche pour que vous vous souveniez vraiment de qui est quelqu'un six mois plus tard.

C'est le logiciel que je veux.