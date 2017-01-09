# Structure des documents

## Sharing

* Type (Master -> Master, Master -> Slave, One-Shot)
* Last update
* Creation
* Users (public names? ids?) : []
* Tag (e.g. "Family", "Friends")


## Access

* Login
* Token
* Sharings : [{id: filter}]
* User id (the id of the contact in the contact application?)

Idéalement ce document serait chiffré puisqu'il contient des informations qu'on aimerait protéger.
Typiquement un utilisateur qui possède les identifiants de connexion peut demander à avoir les documents partagés en faisant une requête "pull" avec une ancienne révision.

---

Un document décrivant l'utilisateur n'est pas forcément nécessaire : on peut s'appuyer sur l'application contacts. Si l'utilisateur ne veut pas créer un nouveau contact on peut mettre toutes les informations dont on a besoin dans le champ `Users` du document `Sharing`.
