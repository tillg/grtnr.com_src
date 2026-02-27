---
date: 2025-11-02
image: swiftdata.jpeg
excerpt: Un guide étape par étape pour ajouter la synchronisation iCloud à une application SwiftData en utilisant CloudKit, incluant la configuration, le débogage et les pièges courants.
title: SwiftData sur iCloud
tags: tech
translation: fr
source_language: en
source_hash: e72d7ff9ad962aa771f3fc92699c91da6d4bf3486cbb78ec2572e22b66b39e62
translator: gpt-4o-2024-08-06
translate_date: 2026-02-27T10:29:48.415617+00:00
generated_by: simplified-translation-system
---

**Remarque** : Le dépôt GitHub associé à cet article se trouve [ici](https://github.com/tillg/SwiftDataOniCloud).

En apprenant Swift et SwiftUI et en commençant à les utiliser, j'ai souvent rencontré des difficultés avec CloudKit. Trop souvent... Voici une configuration minimale que j'ai utilisée pour me rappeler comment j'ai mis en place les choses et documenter mes apprentissages.

- [Point de départ](#point-de-départ)
- [Étape par étape](#étape-par-étape)
  - [Ajouter des capacités au projet Xcode](#ajouter-des-capacités-au-projet-xcode)
  - [Rendre le modèle prêt pour CloudKit](#rendre-le-modèle-prêt-pour-cloudkit)
- [Investigation, Tests, Expérimentations, peut-être compréhension...](#investigation-tests-expérimentations-peut-être-compréhension)
  - [Console CloudKit](#console-cloudkit)
    - [Interroger les données](#interroger-les-données)
  - [Synchronisation en temps réel](#synchronisation-en-temps-réel)
- [Lecture](#lecture)
  - [Apple](#apple)
- [Erreurs fréquentes](#erreurs-fréquentes)
  - [Valeurs par défaut pour les champs](#valeurs-par-défaut-pour-les-champs)
  - [Non connecté avec AppleId](#non-connecté-avec-appleid)
  - [Les droits ont été modifiés pendant la construction](#les-droits-ont-été-modifiés-pendant-la-construction)
  - [Impossible d'initialiser sans un compte iCloud (CKAccountStatusNoAccount).](#impossible-dinitialiser-sans-un-compte-icloud-ckaccountstatusnoaccount)

## Point de départ

Presque tout ce que je sais sur SwiftUI vient du formidable tutoriel [100 Days of SwiftUI](https://www.hackingwithswift.com/100/swiftui) de Paul Hudson. Il fait un travail fantastique pour expliquer SwiftUI et offre ce cours bien entretenu gratuitement.

Pour ne pas avoir à tout recommencer de zéro, j'utilise la leçon du cours qui introduit SwiftData : Au [Jour 53](https://www.hackingwithswift.com/100/swiftui/53), Paul commence un nouveau projet appelé _Bookworm_ qui utilise SwiftData pour stocker ses données de livres. À la fin du [Jour 55](https://www.hackingwithswift.com/100/swiftui/55), il a construit une petite application sympathique qui stocke ses données dans SwiftData. Si vous n'êtes pas à l'aise avec SwiftData ou ne vous en souvenez pas, je recommande fortement de regarder les vidéos de ces 3 jours. Son application utilise SwiftData, mais pas dans le cloud, uniquement localement sur l'appareil.

Je vais utiliser cela comme point de départ pour y ajouter la synchronisation iCloud. Vous pouvez trouver l'application _Bookworm_ dans le [projet Github de Paul Hudson](https://github.com/twostraws/HackingWithSwift) : Elle se trouve sous [SwiftUI > project 11](https://github.com/twostraws/HackingWithSwift/tree/main/SwiftUI/project11).

Si vous clonez/copiez le répertoire _project 11_ et l'ouvrez avec Xcode, vous devez définir votre Équipe et Identifiant de Bundle pour l'exécuter.

Nous allons maintenant essayer d'y ajouter la synchronisation iCloud.

## Étape par étape

### Ajouter des capacités au projet Xcode

Pour utiliser CloudKit pour la synchronisation, nous devons ajouter 2 capacités :

- CloudKit (évidemment)
- Notification : Cela est nécessaire pour que l'appareil puisse recevoir les signaux indiquant que les données ont changé et doivent être resynchronisées avec le cloud.

Si vous ouvrez `Xcode > Projet : MiniSwiftData > Cible : MiniSwiftData > Signature & Capacités`, voici ce que vous devriez voir :

![texte alternatif](signing_wo_capabilities.png)

Cliquez sur le bouton `+ Capability` en haut à gauche et recherchez iCloud :

![texte alternatif](icloud_capability.png)

Ensuite, dans la section `iCloud`, sélectionnez CloudKit comme Service :

![texte alternatif](cloudkit_service.png)

Ensuite, en dessous, nous avons besoin d'un conteneur. Cliquez sur `+` et entrez un nom. Le nom habituel serait l'identifiant de bundle, dans mon cas c'est `com.grtnr.Bookworm` (je le copie-colle simplement depuis le champ _Identifiant de Bundle_).

![texte alternatif](create_new_container.png)

Cela mène à ceci :

![texte alternatif](new_container.png)

C'est en rouge parce qu'il n'a pas encore été créé, cela prend simplement un peu de temps.

Pour garder les appareils synchronisés, iCloud utilise la _Notification Push à Distance_, donc nous devons également ajouter ce service. Cliquez à nouveau sur `+ Capability` et recherchez _Back..._ :

![texte alternatif](background_modes.png)

Ensuite, dans la liste des services de la section _Modes en Arrière-plan_, sélectionnez _Notifications à distance_ :

![texte alternatif](remote_notifications.png)

**Remarque** : Probablement à ce stade, le nom du conteneur est passé de rouge à noir car il a été créé dans iCloud.

### Rendre le modèle prêt pour CloudKit

Lorsque vous démarrez l'application maintenant, vous obtenez une erreur similaire à celle-ci :

```bash
CoreData: error: Store failed to load.  <NSPersistentStoreDescription: 0x600000c0e670> (type: SQLite, url: file:///Users/tgartner/Library/Developer/CoreSimulator/Devices/1464DFC4-EE76-43DB-B178-C33F1FA97A91/data/Containers/Data/Application/34DEE59B-975D-4784-8A87-DC38A9D9DA37/Library/Application%20Support/default.store) with error = Error Domain=NSCocoaErrorDomain Code=134060 "A Core Data error occurred." UserInfo={NSLocalizedFailureReason=CloudKit integration requires that all attributes be optional, or have a default value set. The following attributes are marked non-optional but do not have a default value:
Book: author
Book: genre
Book: rating
Book: review
Book: title} with userInfo {
    NSLocalizedFailureReason = "CloudKit integration requires that all attributes be optional, or have a default value set. The following attributes are marked non-optional but do not have a default value:\nBook: author\nBook: genre\nBook: rating\nBook: review\nBook: title";
}
```

La raison est qu'un modèle doit respecter quelques restrictions. Lors de la création de modèles pour les utiliser avec CloudKit, nous devons respecter certaines règles :

- Valeurs par défaut des propriétés : Chaque propriété doit avoir une valeur par défaut - sauf si elle est optionnelle.
- Ne peut pas utiliser `@Unique`

J'ai donc simplement modifié le fichier `Book.swift` :

```swift
import Foundation
import SwiftData

@Model
class Book {
    var title: String = ""
    var author: String = ""
    var genre: String = ""
    var review: String = ""
    var rating: Int = 3

    init(title: String, author: String, genre: String, review: String, rating: Int) {
        self.title = title
        self.author = author
        self.genre = genre
        self.review = review
        self.rating = rating
    }
}
```

Maintenant, j'exécute l'application sur un simulateur, j'entre 3 livres, je l'exécute sur mon véritable iPhone - et voilà, les livres apparaissent sur mon iPhone !! 🥰

## Investigation, Tests, Expérimentations, peut-être compréhension...

### Console CloudKit

Lors de l'investigation de ce qui se passe, il y a un outil très utile : La [Console CloudKit](https://icloud.developer.apple.com) :

![texte alternatif](cloudkit_console_overview.png)

Sélectionnez _CloudKit Database_ puis sélectionnez la base de données Bookworm :

![texte alternatif](bookworm_db.png)

#### Interroger les données

Pour voir quels livres ont été créés et enregistrés, vous devez sélectionner les options et filtres appropriés

![texte alternatif](bookworm_record_filters.png)

- Assurez-vous qu'au niveau supérieur, vous avez sélectionné la base de données Bookworm > Développement
- Sélectionnez **Base de données privée** : Cela signifie que nous avons une séparation des données par utilisateur
- Dans le menu déroulant de la zone, sélectionnez celle qui n'est pas \__default_, dans mon cas, c'est **com.apple.coredata.cloudkit.zone**. Je n'ai aucune idée (pour l'instant) de ce que ces zones signifient...
- Dans _TYPE D'ENREGISTREMENT_, sélectionnez **CD_Book**, car nous voulons examiner nos livres

Appuyez sur _Query Records_ et obtenez une erreur... 😂
![texte alternatif](query_error.png)

Pour résoudre cela, sélectionnez dans le menu de gauche : Schéma > Types d'enregistrements et voyez ceci :

![texte alternatif](record_types.png)

Nous voyons qu'il avait raison avec son message d'erreur : `recordName` n'est pas marqué comme interrogeable. Alors, corrigeons cela.

Dans le menu de gauche, sélectionnez Schéma > Indexes et cliquez sur `+` pour créer un nouvel index comme ceci :

![texte alternatif](new_index.png)

Retournez à Données > Enregistrements, définissez vos filtres et commutateurs : Base de données privée, zone `com.apple.coredata.cloudkit.zone`, TYPE D'ENREGISTREMENT sur CD_Books et appuyez sur **Query Records** et Baammm :

![texte alternatif](query_records.png)

### Synchronisation en temps réel

L'une des fonctionnalités très cool de CloudKit est la synchronisation quasi en temps réel : Vous modifiez les données sur un appareil, et les modifications deviennent visibles sur l'autre appareil très rapidement - bien sûr sur des appareils connectés avec le même AppleId.

Le fonctionnement est qu'une notification est envoyée à tous les appareils connectés avec cet AppleId, puis ils commencent une synchronisation.

Malheureusement, les simulateurs ne reçoivent pas ces notifications. Donc, pour le tester, vous devez effectuer des modifications sur un simulateur, puis les voir apparaître sur votre appareil réel. Bien sûr, cela fonctionne également si vous utilisez 2 appareils physiques.

## Lecture

Quelques documents et explications précieux que j'ai trouvés.

### Apple

- [Activer CloudKit dans votre application](https://developer.apple.com/documentation/cloudkit/enabling-cloudkit-in-your-app) : Explique comment configurer votre application pour stocker des données dans iCloud en utilisant CloudKit.
- [Gérer les conteneurs iCloud avec l'application CloudKit Database](https://developer.apple.com/documentation/cloudkit/managing-icloud-containers-with-cloudkit-database-app#//apple_ref/doc/uid/TP40014987-CH5) : Explique comment enquêter et voir les données dans vos conteneurs via le Web Dev d'Apple.

- [TN3164 : Déboguer la synchronisation de NSPersistentCloudKitContainer](https://developer.apple.com/documentation/technotes/tn3164-debugging-the-synchronization-of-nspersistentcloudkitcontainer) : En essayant de comprendre pourquoi mon application ne pouvait pas se connecter à son conteneur et continuait de signaler des problèmes d'accès, voici la phrase clé de cette note technique qui m'a sauvé :

> Si le portail montre que l'association entre votre conteneur CloudKit et l'ID de l'application est correcte, mais que l'erreur persiste, il est probable que l'association ne soit pas synchronisée avec le serveur CloudKit. Dans ce cas, envisagez d'utiliser un nouveau conteneur CloudKit pour poursuivre votre développement.

## Erreurs fréquentes

### Valeurs par défaut pour les champs

Les champs d'un modèle doivent avoir des valeurs standard pour pouvoir être enregistrés dans CloudKit. Vous n'en avez pas besoin pour SwiftData si vous enregistrez simplement les données localement sur l'appareil.

### Non connecté avec AppleId

Si l'appareil n'est pas connecté avec un AppleId, il ne synchronise pas.

### Les droits ont été modifiés pendant la construction

```error
Entitlements file "MiniSwiftData.entitlements" was modified during the build, which is not supported. You can disable this error by setting 'CODE_SIGN_ALLOW_ENTITLEMENTS_MODIFICATION' to 'YES', however this may cause the built product's code signature or provisioning profile to contain incorrect entitlements.
```

Bien sûr, je n'ai pas modifié les droits pendant que Xcode construisait. Mais la façon de résoudre cela est assez simple :

- Dans Xcode, allez à _Projet > Cible > Signature & Capacités_
- Décochez (désélectionnez) _Gérer automatiquement la signature_
- Re-sélectionnez-le
- Sélectionnez votre _Équipe_

...et voilà : Xcode reconstruit maintenant votre fichier de droits.

### Impossible d'initialiser sans un compte iCloud (CKAccountStatusNoAccount).

Si vous n'êtes pas connecté sur votre appareil ou simulateur, la synchronisation iCloud ne peut pas fonctionner.

J'ai vu cela et j'étais surpris, car j'ÉTAIS connecté à iCloud. MAIS l'accès à iCloud était désactivé pour l'application :

_Paramètres > iCloud > Enregistré sur iCloud | Tout voir_. Voici à quoi ressemblait le coupable :

![texte alternatif](app_setting_icloud.png)