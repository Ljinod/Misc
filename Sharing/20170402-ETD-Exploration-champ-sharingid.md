# Constat

En tant que développeur d'application il faut que je puisse savoir :
* Quels documents l'utilisateur partage (utilisateur == émetteur).
* Avec qui on partage (utilisateur == émetteur && destinataires ?)
* Quels documents sont issus d'un partage (utilisateur == destinataire).
* Qui nous a envoyé quel document (utilisateur == destinataire && émetteur ?).


# Existant

## Route /permissions/doctype/:doctype

Une route aux fonctionnalités similaires est en cours de création : `POST /permissions/doctype/:doctype`. Elle permet de savoir, pour le doctype donné, quels documents sont partagés par lien.

Pour se faire l'ensemble des documents `permissions` qui ont pour type `share` sont récupérés et seuls ceux qui référencent des document ayant pour doctype celui fournit lors de l'appel sont retenus.

La vue appelée pour générer les résultats est `PermissionsShareByDocView`.

## Documents `permissions`

Une chose à savoir est que les permissions associées à des tokens OAuth ne sont pas persistés. Des "Go Objects" sont créés à la volée et maintenus en RAM. On ne peut donc pas utiliser la même logique pour le partage C2C.


# Conclusion

On peut créer une vue similaire à `PermissionsShareByDocView` où au lieu de se baser sur les documents de type `permissions` on peut se baser sur les documents `auth.Client` et `oauth.Client`. En effet, un client est créé par partage et contient toutes les informations dont on a besoin.
