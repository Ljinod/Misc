# Réplication CouchDB

## Pourquoi on a choisi de ne pas en faire

* La partie « écriture » n'est pas prête et demande du travail. Si on veut tenir le délai ce n'est pas dans notre intérêt de l'implémenter. Voici ce que m'a dit Bruno quand on en a discuté :

> 12:12:02        @N` | julien: il me semble bien que la stack ne peut faire que de la lecture lors d'une réplication et qu'il n'y a pas les routes pour l'écriture

> 12:12:40        @N` | celles de la deuxième liste de https://cozy.github.io/cozy-stack/replication.html#routes-used-by-replication ne sont pas encore implémentées

> 12:14:37        @N` | pour info, c'est compliqué à implémenter

> 12:14:50        @N` | à cause de la gestion des permissions et du real-time

> 12:15:27        @N` | peut-être que c'est possible de faire une session de pair-programming avec romain (ou autre chose dans ce style) pour déminer un peu la zone

> 12:17:23     romain | Peut-être pas de pair-programming, mais du pair-exploring ça vaudrait le coup


* On a un problème complexe à gérer si on fait de la réplication sur des fichiers : on ne peut pas avoir exactement les mêmes documents JSON des deux côtés. Or c'est le but de la réplication…  
Exemple concret : Alice partage un fichier avec Bob, ce fichier est dans `/home/Alice/Dossier`. Bob veut recevoir tous les fichiers qu'on lui a partagé dans `/home/Bob/Partagés avec moi`. Les JSON ne peuvent pas être identiques vu que les chemins diffèrent. Si on décide quand même de synchroniser en passant par de la réplication alors il faut le faire sur des fichiers « tampons » qui ne contiennent que les éléments en communs (typiquement le chemin n'apparaîtra pas dedans).  
Ce problème se transpose aux autres documents : un tag pour un contact, le nom d'un calendrier, etc…


* On ne peut pas utiliser la réplication pour des fichiers : la stack ne permet pas de dissocier binaire et JSON. Dans tous les cas on est obligé d'envoyer le fichier et le JSON le décrivant en même temps.
