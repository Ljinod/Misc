# Carte trello

**VOCABULAIRE** :
* **Fichier** : une photo, un document Word, une musique, etc… Un « binaire ».
* **Document** : le JSON qui décrit un _fichier_.

## Contexte

Dans le cadre d'un partage de fichiers "one-shot" en lecture seule.


## Specs

* Discussion avec l'équipe mobile et desktop : peut-on utiliser le même mécanisme ?
* Doit-on l'adapter ? Si oui, comment ?
* Doit-on / peut-on vérifier l'intégrité du fichier ? Comment s'assurer que le fichier reçu correspond bien au fichier demandé pour le partage ?

## Tâches

* [ ] Je suis capable de spécifier la carte [ETE je peux envoyer le fichier vers le récepteur une fois le partage accepté](https://trello.com/c/cUxWVoXj/17-syn-6-e-2-ete-je-peux-envoyer-le-fichier-vers-le-recepteur-une-fois-le-partage-accepte)

---

# Réflexions : comment partager un fichier ?

## Discussions avec les différents équipes

### Mobile

Pour le moment l'application mobile ne propose pas de synchronisation de fichiers à proprement parlé : elle propose la même expérience que depuis l'interface web. Les fichiers téléversés sont envoyés directement dans le Cozy et le fichier JSON, i.e. les méta-données, est créé à la volée.

Le mobile utilise cependant la réplication en « lecture » :
> 14:20:17     julien | N`: le mobile utilise la partie « lecture » des réplications ou ils ne font pas du tout de réplication ? (je pense que j'ai déjà posé la question hier mais je n'ai pas noté et j'ai un doute d'un coup…)

> 14:21:40        @N` | je crois qu'ils font de la réplication juste en lecture

D'après ce que je comprends de leur code ils veulent utiliser la réplication pour le mode hors-ligne (tout le code est [ici](https://github.com/cozy/cozy-client-js/blob/14cf68ce2c0ab7508da90a3cfd74cfda3ea7194c/src/offline.js)) et uniquement pour faire des réplications de CouchDB (Gozy) vers PouchDB.


### Desktop

L'application "cozy-desktop" n'utilise pas non plus la réplication pour maintenir les documents JSON décrivant les mêmes fichiers conservés à deux « endroits » différents.  
En effet chaque « endroit » à son propre JSON pour décrire le même fichier et, d'après ce que je vois, le Cozy fait office de référence. Les autres JSONs gardent un lien vers ce JSON de référence.  
La structure de ces documents est la suivante :
* `_id` : le chemin normalisé (sans tenir compte des contraintes des OS) ;
* `_rev` : la révision du fichier (soit celle de Pouch, soit celle de Couch) ;
* `path` : le chemin actuellement utilisé sur le VFS et FS ;
* `checksum` : sha1sum du fichier ;
* `remote` : `id` et `rev` du JSON conservé dans le Cozy ;
* `sides` : pour tenir compte de ce qui est fait dans le Cozy et en local.


Le client desktop écoute les changements du Cozy : il se branche sur `_changes` pour savoir ce qu'il se passe exactement. Si un changement a été détecté il va mettre l'un ou l'autre à jour en fonction des nouveautés.

Conversation IRC 2017/03/22 :
> 12:06:18  julien | Vous envoyez les méta-données d'abord et ensuite le fichier en lui-même ? Si c'est le cas vous faites comment pour vérifier que l'un correspond à l'autre ?

> 12:07:16     @N` | non, on envoie juste le fichier

> 12:08:11     @N` | cet appel -> https://cozy.github.io/cozy-stack/files.html#post-filesdir-id-1

> 12:09:12     @N` | on récupère l'id et la révision du fichier que l'on ajoute dans le document JSON du pouch local (dans le champ "remote")

> 12:11:07     @N` | ça ne fonctionne pas comme de la réplication couchdb (même pour les metadonnées)

> 12:11:33     @N` | les documents sur le couchdb du cozy et le pouchdb local de cozy-desktop se ressemblent mais ne sont pas les mêmes

> 12:11:40     @N` | il y a des différences assez fortes

> 12:11:57     @N` | par exemple, les ids ne sont pas les mêmes

> 12:12:19  julien | okay, et comment vous faites pour les comparer pour propager les changements ?

> 12:12:43     @N` | ha, là, tu rentres dans la partie compliquée

> 12:13:43     @N` | la version haut niveau est là -> https://github.com/cozy-labs/cozy-desktop/blob/master/doc/design.md#cozy-desktop---design

> 12:13:48     @N` | mais le diable est dans les détails


### Back

Conversation IRC 2017/03/23 :
> 12:12:02        @N` | julien: il me semble bien que la stack ne peut faire que de la lecture lors d'une réplication et qu'il n'y a pas les routes pour l'écriture

> 12:12:40        @N` | celles de la deuxième liste de https://cozy.github.io/cozy-stack/replication.html#routes-used-by-replication ne sont pas encore implémentées

> 12:14:37        @N` | pour info, c'est compliqué à implémenter

> 12:14:50        @N` | à cause de la gestion des permissions et du real-time

> 12:15:27        @N` | peut-être que c'est possible de faire une session de pair-programming avec romain (ou autre chose dans ce style) pour déminer un peu la zone

> 12:17:23     romain | Peut-être pas de pair-programming, mais du pair-exploring ça vaudrait le coup



## Processus de synchronisation des fichiers ?

### Pull VS Push

(Paul veut voir les aspects)

### Discussion avec Bruno

Conversation IRC 2017/03/22 :
> 16:24:32        @N` | julien: rappelle-moi, dans le partage de cozy à cozy, c'est celui qui a créé le partage qui pousse ses données vers l'autre (ou les autres), c'est bien ça ?  

> 16:24:42        @N` | dans l'autre sens, ça serait plus facile pour les fichiers  

> 16:24:44     julien | N`: yep c'est bien ça  

> 16:24:53        @N` | tu te branches sur le changes feed  

> 16:25:09        @N` | et à chaque document ajouté, tu télécharges le nouveau fichier  

> 16:25:24        @N` | si c'est document supprimé, tu modifies le fichier  

> 16:25:46        @N` | si c'est un document mis à jour, c'est un peu plus compliqué, mais ça se gère aussi  

> 16:26:42     julien | N`: je note ta réponse, je finis ma réunion et je te relance :p  

> 16:28:06        @N` | peut-être que l'émetteur peut envoyer le changes feed sur une route particulière au récepteur  

> 16:28:27        @N` | et charge au récepteur de télécharger le contenu des fichiers et faire les autres opérations  

> 16:28:50        @N` | mais j'ai vraiment le sentiment que c'est beaucoup plus facile à gérer depuis le récepteur que depuis l'émetteur  

> 16:29:26        @N` | parce que tu peux envoyer un bulk ton changes feed  

> 16:29:50        @N` | mais chaque entrée va demander plusieurs interactions avec le couchdb du client  

> 16:30:00        @N` | - est-ce qu'il y a un conflit ?  

> 16:30:07        @N` | - est-ce que le répertoire parent existe bien ?  

> 16:30:18        @N` | - créer le document  

> 18:01:28     julien | N`: on garde tes remarques en tête, on se penche sur le sujet sérieusement (au programme de ce soir/demain) et on n'hésitera pas à te faire des retours  

> 18:01:45     julien | on a déjà une question, pourquoi tu penses que c'est plus simple en pull ?  

> 18:02:13        @N` | pas forcément en pull  

> 18:02:31        @N` | je pense que c'est plus simple si c'est le récepteur qui fait le gros du boulot  

> 18:03:09        @N` | comme je disais plus haut, c'est lui le mieux placé pour détecter les conflits et potentiellement faire des vérifications  

> 18:03:20        @N` | genre que le répertoire parent existe bien  

> 18:04:36     julien | Pour le coup du répertoire ça veut dire qu'on copie l'arborescence de l'émetteur (si je partage le dossier /home/julien/Cozy, ça veut dire que les récepteurs doivent avoir /home/julien) ce qui n'est pas forcément souhaitable  

> 18:06:15        @N` | si tu partages /home/julien/Cozy à paul et que paul a placé ça /home/paul/Cozy, il faut vérifier que le répertoire Cozy n'a pas été supprimé par paul quand tu reçois un fichier  

> 18:07:09        @N` | je parle du répertoire qui n'est pas partagé mais qui contient le partage  

> 18:07:22        @N` | c'est peut-être /home/paul dans le cas précédent  

> 18:08:05        @N` | tu vois l'idée ?  

> 18:08:30       paul | N`: dans un 1er temps on va considérer que tous les fichiers/repertoires partagés sont un dossier racine "shared with me" coté recepteur  

> 18:08:35     julien | (yep, paul est en train de te répondre ^^)  

> 18:09:15       paul | ça limite les problèmes de hierarchie  

> 18:09:34        @N` | ok  

> 18:09:39     julien | et ça veut dire qu'on ne peut pas répliquer tel quel les documents JSON  

> 18:09:46     julien | tels quels *  

> 18:10:37        @N` | oui, il faut recalculer le path, potentiellement modifier le parent_id si le fichier/répertoire est à la racine du partage, etc.  

> 18:11:04     julien | Yep c'est la conclusion à laquelle on était arrivé  

> 18:11:39     julien | mais je ne pensais pas qu'on pouvait intercepter les réplications et modifier en conséquence ce qui arrive, d'où mes précédentes questions  

> 18:12:04        @N` | tu ne peux pas intercepter une réplication  

> 18:12:19        @N` | par contre, la réplication est construite sur la base du changes feed  

> 18:12:39        @N` | et tu peux utiliser le changes feed pour faire déjà pas mal de choses  

> 18:12:43     julien | La stack n'intercepte pas les réplications ?  

> 18:13:01     julien | Pour faire une sorte de proxy  

> 18:13:36        @N` | romain saura te dire mieux que moi  

> 18:14:20        @N` | de ce que j'en comprends, non, la stack ne lit pas les documents, elle ne fait que lire un flux de données entre couchdb et le client  

> 18:14:42     julien | hummm  

> 18:15:43     julien | On n'a aucun moyen de « jouer » avec ce flux de données ?  

> 18:15:59     julien | Il nous avait semblé comprendre que si  

> 18:16:58        @N` | ça doit être possible  

> 18:17:11        @N` | mais va falloir le coder  


Chemin complet d'un dossier :
* https://github.com/cozy/cozy-stack/blob/master/pkg/vfs/directory.go#L37
* https://github.com/cozy/cozy-stack/blob/master/pkg/vfs/file.go#L68


### Réflexions

Le problème majeur qu'on va avoir réside dans les chemins des fichiers : si Alice veut partager avec Bob son dossier `/Alice/Pictures/Holidays/`, Bob ne voudra peut-être pas que cela créé la même arborescence dans son Gozy. Il préfèrerait peut-être mettre tous les fichiers qu'il reçoit dans un répertoire qu'il a prédéfini à l'avance comme `/Bob/SharedWithMe`.

En partant de ce constat on ne peut pas répliquer tels quels les documents JSON entre l'émetteur et les récepteurs du partage. Deux solutions s'offrent à nous :
1. _Intercepter_ : On est capable d'intercepter dans la stack ce qui va être répliqué pour modifier la « destination » des fichiers reçus. Dans notre exemple, remplacer `/Alice/Pictures/Holidays` par `/Bob/SharedWithMe`.
1. _Dupliquer_ : Le document JSON reçu est dupliqué, la « destination » est modifiée dans le doublon et le fichier sera uniquement référencé par le doublon.


#### Discussion : intercepter

Ce qu'il faut faire :
1. Modifier le parent pour le faire pointer vers le dossier accueillant les partages.
1. Se souvenir du parent de l'émetteur pour, quand des modifications sont apportées, pouvoir lui renvoyer une version conforme.

Points négatifs :
* (**gros point négatif**) Si la destination est modifiée, une nouvelle révision est créée et le document JSON est renvoyé vers l'émetteur / récepteur. Ce qui créé une boucle infinie.

Points positifs :
* Un seul document dans les deux Cozy.


#### Discussion : dupliquer

Ce qu'il faut faire :
1. On intercepte la réplication.
1. On copie le document entrant et on modifie, dans la copie, le parent et/ou le chemin dans le VFS.

Gestion des mises-à-jour : un démon dédié s'occupera de vérifier les documents qui décrivent les fichiers partagés où l'utilisateur n'est pas l'émetteur. Ce démon aura un minimum d'intelligence : il ne prendra pas en compte le chemin et le parent du fichier.

Points négatifs :
* Deux documents à gérer chez les récepteurs : la version envoyée par l'émetteur et la copie qui se conforme à ce que le récepteur veut. Il faudra donc gérer de manière fine ce qu'il se passe côté récepteur : identifier les changements apportés à la copie qui impacte l'émetteur et les propager sur le JSON envoyé par l'émetteur.
* Il faudrait « annuler » le document JSON envoyé par l'émetteur : celui-ci n'a pas lieu d'être considéré dans son VFS.

Points positifs :
* Propagation des changements plus propre : on ne propage que les modifications qui impactent l'émetteur ET le récepteur.


#### Choix : dupliquer

À mon avis le meilleur choix reste la duplication tant qu'on ne trouve pas une solution pour ne garder qu'un seul document.
