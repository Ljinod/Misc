Scénario : un user veut partager un ensemble dynamique de documents depuis une app

Etape 0 - création du partage app -> DS

Au niveau user, le partage est déclenché depuis un bouton 'share' qui appelle un intent de la home, et va lui permettre de séléctionner les options du partage, notamment :
    * Le(s) destinataire(s)
    * Une description (optionnelle)
    * isSynced -> pour indiquer si ce qui est partagé est modifiable par les deux parties (celui qui partage et celui/ceux qui reçoit/reçoivent le partage).
    * IsReadOnly -> pour indiquer que le partage n'est pas modifiable par le(s) récepteur(s).

Selon le use case, différents types de partage peuvent être gérés, chacun ayant des paramètres spécifiques :

     Partage statique: partager un ensemble de docs bien définis, sans ajouts à posteriori.

    Params : [ids], isSync, isReadOnly

    Partage dynamique structuré : partager un ensemble de docs dynamiques dans un conteneur où chaque élément est un enfant du conteneur, et possède un attribut parentID permettant de se référer à son parent

    Params : parentID, [childDocTypes], isReadOnly, isSyncPostOnly, [ids], hasHierarchy

    parentID est l'id du conteneur.

    childDocTypes contient l'ensemble des docTypes des enfants

    Le booleen hasHierarchy permet d'indiquer à la stack que des docs ayant le docType du parent seront susceptibles de rentrer dans le partage, avec leurs enfants

    On peut optionnellement passer la liste initiale d'ids pour éviter au DS de la rechercher

    Le isSyncPostOnly sert a spécifier qu'on propage les POST mais pas les PUT/DEL (pour faire plaisir à Julien ou pour partager un album photo avec sa famille !)

    Partage dynamique non structuré : partager un ensemble de docs dynamique avec un modèle de données custom

    Params : [rules], isReadOnly, isSyncPostOnly, [ids]

    [rules] est un ensemble de prédicats définissant la règle de partage

    Pour éviter l'exécution de code arbitraire, on doit définir une grammaire de règle. On ne réinvente pas la roue : on prend la syntaxe mango https://github.com/cloudant/mango#json-syntax-descriptions

    On peut avoir plusieurs cas de custom rules

    Avec hierarchie, où les enfants sont dépendants d'une "jointure" avec le parent (voir Gestion des hierarchies plus loin)

    Il faut faire apparaitre cette notion de jointure et de dépendance au doc parent.

    Si cette dépendance change (ex du nom du calendrier modifié), il faut pouvoir mettre dynamiquement à jour le filtre, avant que les updates des enfants soient effectués

    Sans hierarchie : partage "à plat", eg un ensembles de notes


Dans tous les cas, un doc sharing est crée et le(s) docs user crée/mis à jour. L'id du doc sharing correspond au shareID, qui sera ajouté dans tous les docs du partage.

Initialisation du filtre côté stack
Quelque soit le type de partage, un createFilter est appellé, qui va l'enregistrer dans un nouveau doc access (?) et l'ajouter dans les filtres maintenus en ram.
Les filtres ont donc  2 formes possibles :

    Liste d'ids, pour un partage statique

    ([parentIDs], [childDocTypes], hasHierarchy) pour un partage dynamique structuré

    [rules] pour un partage dynamique non structuré


* Si la liste d'ids a été fournie (pour le partage statique ou dynamique), tous les docs sont récupérés puis envoyés en POST sur la bd /sharing
* Si elle n'a pas été fournie, l'ensemble des docs ayant le/les docType enfant sont requetés pour vérifier s'ils rentrent dans le filtre

    * Par le parentID (de manière récursive sur les conteneurs « enfants » – si hiérarchie) pour un partage structuré

    * Par la custom rule pour un partage non structuré : ça correspond

    * Chaque doc à true dans le filtre est POST vers la bd /sharing


Evaluation dynamique
Les partages statiques et dynamiques sont différenciés ici :

    Pour un partage statique, on intercepte tous les PUT/DELETE, et on vérifie si l'id du doc match dans une liste d'id. Si oui, on route la requête à la bd /sharing

    Pour un partage dynamique, on intercepte tous les POST/PUT/DELETE.

    Une structure {docType, [ids]} est maintenue en RAM (correspond à une vue sur /sharing)

    Dans le cas d'un POST/DELETE évalué positivement par une règle, on route vers la bd /sharing, et on update la structure en ram

    Dans le cas d'un PUT : on évalue les filtres et on vérifie si le document existe dans la liste {docTypes, [ids]}

    Si evalué positivement, et doc existant : on route le PUT

    Si évalué positivement et doc non existant : on ajoute l'id dans la structure et on POST le doc dans /sharing

    Si évalué négativement et doc existant : on enlève l'id dans la structure et on DELETE dans /sharing

    Si évalué négativement et doc non existant : on ne fait rien

    Cas bonus : doc qui sort d'une règle et rentre dans une autre par le PUT (#utilisateurVicieux)

    Lorsqu'un conteneur est mis à jour et qu'il impacte tous les enfants (eg nom d'un calendar), on a 1 possibilités selon le type de partage (a noter qu'un doc conteneur modifié doit toujours rester dans le filtre):

    Partage structuré

    capable de détecter que le PUT concerne un parentID, et de modifier le filtre en conséquence avant l'updates des enfants => il faut que le sharing manager soit capable de bloquer les updates

    Partage non structuré : doit être géré côté applicatif, en déclenchant un updateFilter avant l'updates des enfants


Gestion des hierarchies
Le cas peut se poser pour le partage structuré et non structuré :

    Partage structuré : on suppose ici que les sous-conteneur référencent le conteneur parent par son parentID

    on ne gère plus un parentID, mais une liste de [parentID]. Le parentID correspondant au doc root est identifié et son docType permet d'identifier les conteneurs enfants

    on ne sait pas s'il peut y avoir plusieurs types de « sous-conteneurs »… Exemple à trouver.

    Un partage basé sur un "tag" sur un album de photos, qui lui-même contient des sous-albums mais sans le tag cette fois… Est-ce que le partage est basé sur le tag ou sur les albums qui ont ce tag ?

    -> S'il se base sur le tag, pour moi le sous album ne doit pas rentrer dans le partage. L'utilisation des tags crée une hierarchie transerve (eg partage de tous les docs avec tag 'team').  S'il se base sur l'album, le sous album rentre dedans par la hierarchie.

    POST d'un conteneur : check s'il référence un [parentID], si c'est le cas, on l'ajoute à la liste des [parentID]

    DELETE d'un conteneur : DELETE du parentID, et des docs enfants => maintenant d'une structure (parentID, [ids]) ?

    PUT sur un conteneur

     Le comportement est le même que décrit dans l'Evaluation dynamique pour le conteneur root

    Pour un conteneur enfant, évaluation pour vérifier que son parentID est toujours dans les [parentID]. Si ce n'est plus le cas (eg déplacement de répertoire), DELETE du conteneur et des enfants

    POST/PUT/DEL : même comportement que pour les docs de l'Evaluation dynamique

    pour l'init, on vérifie récursivement toute la hierarchie pour construire la liste [parentID] et identifier les [ids] à partager

    Partage non structuré

    Le filtre est capable d'exprimer cette hierarchie, ex. (docType == 'file' && path.contains('cozy')) || (docType == 'folder' && path.contains('cozy')

    Les docs de la hierarchie sont naturellement évalués par le filtre

    Un PUT sur le conteneur root doit être traité comme décrit dans la partie Evaluation dynamique : le filtre doit être mis à jour côté applicatif avant les updates des enfants

    Un PUT sur un conteneur enfant est géré comme les docs dans Evaluation dynamique, en rajoutant les DELETE des docs enfants s'il sort du filtre.



Note : Les listes d'ids à maintenir pour gérer les PUT peuvent être potentiellement grandes. Peut être explorer des pistes d'opti vers les arbres en mémoire et/ou bloom filter et/oiu hash table, qui semble particulièrement adapté (O(0) en moyenne)
Il y a probablement un design hybride à trouver pour savoir quelles structures utiliser et comment gérer RAM vs disque : si on a 9M d'éléments faisant 49 octets chacun, , ça couterait 499Mo à garder en RAM...
Avec l'exemple précédent, ça prendrait 10Mo avec un bloom filter de 0% de faux positifs (http://hur.st/bloomfilter?n=9999999&p=-1.0)
Voir aussi http://stackoverflow.com/questions/4282374/what-is-the-advantage-to-using-bloom-filters
Dans notre cas, l'avantage du bloom filter n'est pas forcément évident, c'est probable qu'on ait plus de de cas positifs que de négatifs

Idée de structure révolutionnaire : Une hash table stockant 0 bit pour dire si la valeur recherchée existe ou non. 0 bit/element -> + léger que le bloom filter \o/
On ne peut pas avoir de fonction de hash qui empêche les collisions, une HT de 0M d'éléments, aura une proba de collision > 49% à parrtir de 1149 éléments (cf paradoxe des anniversaires)
=> commen gérer les collisions ?

Note : Si on a beaucoup de partages, et donc de filtres, l'éval peut devenir couteuse. Envisager des stratégies alternatives, comme évaluer périodiquement les derniers docs modifiés ? Peut être intéressant pour des partages ne nécessitant pas de temps réel

Note : une API pourrait permettre la création d'un partage pour les doctypes "connus", du type shareCalendar, shareDirectory, etc.
L'app n'aurait alors plus qu'à passer le parentID en paramètre, le DS étant capable de retrouve le bon docType des enfants et la bonne vue pour récupérer tous les ids qui vont bien
(Julien) Je ne suis pas très tenté par cette idée parce que ça pourrait induire des coups de maintenance supplémentaires.

    -> (Paul) Si on ne gère que quelques cas bien définis, ça ne me parait pas insurmontable. De toute façon ce n'est pas prioritaire, ce serait une fois qu'on aurait toute la mécanique


Note : pour pas mal de choses on est dépendant du contexte pour choisir la meilleure stratégie : nombre de partages, nombre de destinataires, nombre de docs, besoin  ou non d'updates rapides...
On ne pourra pas tout gérer, il va falloir trancher et bien définir les cas limites => besoin d'un benchmark



Etape 1 - shared bd - (Ok pour moi) : yeah !

Docs sharing et user_sharing
On mutualise les process de réplication par users. On a donc 0 document user_sharing contenant les infos sur le user (url, name ,etc) et 0 doc sharing contenant les infos du partage (description, isReadOnly, etc).
On a une relation (n,n) entre ces docs : 0 user peut référencer plusieurs partages, et 0 partage peut référencer plusieurs users.
On choisit de référencer les docs sharing  par un champ [shareIDs] depuis les docs user_sharing. L'inverse est aussi possible, on fait ce choix car la vue (shareID, [repID, url]), est plus simple à faire dans ce sens là : on a toutes les infos depuis le doc user_sharing

Process de replication
Chaque process de réplication contient l'ensemble des docids autorisés pour 0 user. Il faut donc maintenir cette liste de docids en tenant compte de leur taille potentiellement élevée (plusieurs millions potentiels)
On passe donc par des vues plutôt que par un stockage de la liste dans un doc (impliquerait de ré-écrire le doc à chaque update, donc beaucoup d'IO).
1 vues sont nécessaires :
    * (shareID, docid) -> chaque doc partagé (et donc répliqué dans la bd sharing) contient le shareID du partage concerné. Cette vue indexe donc l'ensemble des docids pour un shareID
    * (shareID, [repID, url]) -> chaque doc user_sharing contient le repID, l'url du destinataire et la liste des shareID qui le concerne. Le map-reduce permet d'associerr à un shareID l'ensemble des [repID, url]

Quand un doc arrive, on requete la vue (shareID, [repID, url])  avec ?key=shareID, pour récupérer l'ensemble des repID, et pour chacun, on fait un get sur \_replicator pour recuperer les docids courant et ajouter le nouveau

Bufferisation des nouveaux docs
Dans le cas de partages avec beaucoup de nouveaux docs, ça peut être couteux de remettre à jour continuellement la réplication. Il pourrait être intéressant de bufferiser les nouveaux docs s'ils concernent un même partage.


Etape 2 - destinataire

L'emetteur (A) envoie une demande de partage au destinataire (B). Cette demande contient les champs suivants :
    * shareID -> identifiant unique du partage
    * Filter -> {parentID, [childDocTypes], parentInChild
    * sharerUrl
    * sharerName
    * description
    * token -> préalablement généré par un précédent partage, pre_token sinon

Si B accepte la demande de partage, un access est généré, contenant le login / token de l'emetteur, qui sera le même pour tous les futurs partage de A.  
Le filtre correspond à l'expression des permissions que B donne à A. B peut avoir à gérer beaucoup de filtres -> où le stocker ? Dans un doc sharing avec la description et le shareID ?
Même question pour les infos du user A : dans un doc user avec sharerUrl et sharerName ?
Les informations « sensibles » (identifiant, mot de passe, filtre) sont dans le document "Access" qui sera chiffré.

Question : comment stocker intelligement toutes les infos dans le cas d'un partage bilatéral où chacun est à la fois emetteur et destinataire, en évitant les doublons ?
- Quelles informations (« toutes les infos ») ?
- On met les deux utilisateurs en émetteurs du partage : puisqu'ils ont tous les deux les droits en lecture / écriture c'est comme s'ils s'étaient fait tous les deux le même partage. Chacun doit avoir un document "Access" et un document de partage (entre-autre pour le filtre).

    - Après discussion avec les gens du bureau ils trouvent ça très étranges qu'un récepteur puisse supprimer, même dans le cadre d'un partage bilatéral. Il faudrait donc faire un tri des \_changes pour que la suppression entraîne juste un arrêt du partage…

    -> je suis étonné de leur étonnement :) C'est le comportement typique de dropbox.

- La situation – future – qui nous pose problème est celle où il y a des conflits des deux côtés. Soit un document D partagé par A à B :

    - Lors de la première réplication le document est à la version D-1 ;

    - A modifie D, D passe en version D0 ;

    - B modifie D, D passe en version D1 ;

    - A reçoit la version D1 et B reçoit la version D0 ; les deux Couch se mettent d'accord sur la version D2 (normalement la même, est-ce que l'algo de résolution de conflit est déterministe ? -> oui) ;

    - A & B ont un conflit dans l'historique ;

    => comment est-ce qu'on le résout ? On présente une pop-up aux utilisateurs ? Qui décide de la version finale si personne n'est d'accord ?

    -> technique dropbox, ie on garde D1 et D0 en les marquant avec un \_CONFLICT dans le nom, répliqué chez A et B. c'est aussi la vision de ben



Une fois l'access crée, B renvoie sa réponse à A qui peut répliquer si c'est ok.


WARNINGS - etape 0
* On peut avoir plusieurs parents par enfant, typiquement, un contact peut avoir plusieurs labels
* Plusieurs filtres peuvent avoir le même parentID. Si A partage avec B un ensemble de docs en bilatéral, puis les mêmes docs avec C mais en read only, ce sont 1 partages différents


PARTAGE DE BINAIRES

* une route spéciale /sharing/binary
* un document décrivant les meta-données doit être présent en base pour être accepté
* on vérifie automatiquement le checksum avant de l'enregistrer
* si une demamde de binaire est reçue mais ne correspond à aucune meta-data on avertit le propriétaire du Cozy
* si la checksum ne matche pas ce qui est écrit dans les meta-data on supprime ce qui a été téléchargé et on demande une ré-émission.
