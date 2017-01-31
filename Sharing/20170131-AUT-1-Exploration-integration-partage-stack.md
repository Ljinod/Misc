# Dynamic sharing

## Structure of the documents used

### _io.cozy.sharings_

A sharing document will look like:

```json
    {
        "documents": ["id1", "id2", "id3"],
        "recipients": [
            {"id":"url.cozy1", "status":"pending"},
            {"id":"url.cozy2", "status":"pending"}
        ],
        "type": "ONE-SHOT",
        "description": "Give it to me baby!"
    }
```

- [ ] Est-ce qu'on rajoute des meta-données ? Date de création ? Date de dernière mise-à-jour ?

#### Documents

Which documents will be shared. We provide their identifiants, a more dynamic solution (through some sort of selector) will be studied later.

#### Recipients

An array of the recipients and, for each of them, the status of the sharing. The possible values for the sharing are:
* `pending`: the recipient didn't reply yet.
* `accepted`: the recipient accepted.
* `refused`: the recipient refused.

#### Type

`type` is the type of sharing. It should be one of the followings: `MASTER-MASTER`, `MASTER-SLAVE`, `ONE-SHOT`.  
They represent the access rights the recipient and sender have:
    * `MASTER-MASTER`: both recipient and sender can modify the documents and have their modifications pushed to the other.
    * `MASTER-SLAVE`: only the sender can push modifications to the recipient. The recipient can modify localy the documents.
    * `ONE-SHOT`: the documents are duplicated and no modifications are pushed.

#### Description

The answer to the question: "What are you sharing?". It is an optional field but, still, it is recommended to provide a small description.


### _io.cozy.permissions_

The recipient will need to give access rights to the sender. We will use the permission structure described [here](https://github.com/cozy/cozy-stack/blob/master/docs/permissions.md).

```json
    {
        "data": {
            "type": "io.cozy.permissions",
            "attributes": {
                "application-id": "associated-sharing-id",
                "permissions": {
                    "type": "associated-sharing-docType",
                    "verbs": ["GET","POST","PUT","PATCH"],
                    "values": ["id1", "id2", "id3"],
                    "description": "Aha aha!"
                }
            }
        }
    }
```

- [ ] Est-ce qu'il faut aussi créer une permission chez l'émetteur ? Pour que la stack autorise la réplication.
- [ ] Est-ce qu'on doit instaurer une gestion fine des verbes http en fonction du type du partage ? Par exemple un partage de type `ONE-SHOT` n'aura pas besoin de `PATCH`.
- [ ] Que fait-on du verbe `DELETE` ?
- [ ] Explorer OAuth pour savoir exactement ce qui doit être mis dans ce document, comment on peut l'utiliser.

#### Application-id

It is the identifiant of the sharing document that describes the sharing.

#### Type

The docType of the shared documents.

#### Verbs

The actions the sender has to be able to do on the recipents Cozies. Combined with the `values` it limits those to the documents specified in the latter.

#### Values

It corresponds to the `documents` in the `io.cozy.sharings` document: it is the list of documents that will be shared.


## Where to integrate the sharing code?

### cozy-stack/pkg/sharings

The implementation of the logic: creating a new sharing, handling an answer, starting a replication, etc…

### cozy-stack/web/sharings

The declaration of the routes and their chaining.


## Routes

### POST /sharings

Create a new sharing.

### POST /sharings/request/:id

Receive a sharing request.

### POST /sharings/answer/:id

Answer a sharing request.

### DELETE /sharings/:id

Delete the specified sharing (both the sharing document and the associated permission).

### POST /sharings/replicate/:id

Start the replication (create the correct document in _\_replicator_) for the specified sharing.
