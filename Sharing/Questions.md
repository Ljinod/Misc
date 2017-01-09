Est-ce qu'on a un token pour l'envoi de données et un autre pour la réception ?

**Réponse** : Non.

---

Est-ce que si un partage master-master est entre plusieurs personnes on communique la liste complète des destinataires à tout le monde ?

Pour :
* si quelqu'un modifie un fichier la modification est répercutée chez tout le monde.

Contre :
* Peut-être qu'on a envie de faire du travail collaboratif sans se connaitre les uns les autres.

**Réponse** : Oui. Mais cela soulève une nouvelle question : est-ce qu'on autorise l'ajout de nouveaux destinataires par quelqu'un d'autre que l'initiateur du partage ?

---

Est-ce qu'on autorise l'ajout de nouveaux destinataires par quelqu'un d'autre que l'initiateur dans un partage master-master ?
Par exemple : dans un partage A(initiateur)-B-C est-ce qu'on autorise B ou C à ajouter quelqu'un qui pourrait donc aussi modifier les fichiers partagés chez A ?

---

Que fait-on du pretoken ?

Dans les scénarii que j'ai mis en forme je l'écris dans le document de partage au moment de la réception de la demande. Est-ce qu'on le supprime ? Est-ce qu'on le laisse là ?

**Réponse** : Dans un partage A-B, ça permet de s'assurer que C ne réponde pas à la place de B. Une fois que ce rôle est joué on peut effectivement le supprimer.

---

Est-ce qu'il faut détailler plus la création des filtres dans les diagrammes ?

---

Est-ce qu'on génère un token par partage ? Ça nous oblige peut-être à créer plus de replications mais peut-être pour une meilleure sécurité ? On peut le mettre dans la liste des partages : { id, filter, token }.

**Réponse** : Oui, pour éviter que tous les partages avec un même destinataire soient compromis au cas où un token viendrait à atterrir entre de mauvaises mains.

---

Comment est-ce qu'on gère les nouveaux partages ?

J'avais dans l'esprit de créer une queue pour ne pas lancer tous les partages en même temps. Après réflexion je me suis dit que si on a deux jobs différents dans la stack 1) pour gérer les nouveaux partages et qu'on réveille à chaque création ; 2) pour gérer les mises-à-jour, qu'on réveille à intervalle régulier et qui dispose de seuils à ne pas dépasser pour ne pas impacter les performances du Cozy on a peut-être pas besoin de se casser la tête avec des scénarii compliqués…

**Réponse** : oui, les create et updates sont 2 process différents. Pour le create, la complexité est de pouvoir exécuter le filtre sur tout le cozy, pour les updates, d'avoir un impact minimal en RAM (en gardant une synchro un minimum performante).

---

Vérifier avec l'équipe back que la manière de procéder est bien la bonne.

---

Dans le diagramme "./diagrams/5-New-sharing-dedicated-process.png" est-ce que les champs `doc_ids` et `selector` ne sont pas redondants ?

**Réponse** : on peut le garder pour les partages statiques, et considérer que si le champ doc_ids existe, il ne faut pas prendre en compte le selector.

---

Comment est-ce qu'on gère la « suppression » d'un partage de type "Master-Master" d'un des destinataires lorsqu'il reste, après son désistement, plus de deux destinataires ?

Scénario typique : partage "Master-Master" entre A-B-C et A supprime le partage.

---

Si on lance une réplication vers une bd existante chez le destinataire et qu'on a bien les droits (un document "access" existe), que se passe-t-il ?
