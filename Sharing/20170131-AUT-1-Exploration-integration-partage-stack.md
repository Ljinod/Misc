# Dynamic sharing

## Structure of the documents used

### _io.cozy.sharings_

A sharing document will look like:

```json
    {
        "_id": "xxx",
        "_rev": "yyy",
        
        "owner": true,
        "permissions": {
            "doctype1": {
                "description": "doctype1 description",
                "type": "io.cozy.doctype1",
                "values": ["id1", "id2"],
                "selector": "calendar-id", //not supported yet
                "verbs": ["GET","POST", "PUT"]
            }          
        },
        "recipients": [
                {
                    "recipientID": "recipientID1",
                    "status": "accepted",
                    "access_token": "myaccesstoken1",
                    "refresh_token": "myrefreshtoken1"
                }, 
                {
                    "recipientID": "recipientID2",
                    "status": "pending"
                }
        ],
        "type": "one-shot",
        "description": "Give it to me baby!",
        "shareID": "xxx"
    }
```

- [ ] Est-ce qu'on rajoute des meta-données ? Date de création ? Date de dernière mise-à-jour ?

#### Owner

To tell if the owner of the Cozy is also the owner of the sharing. This field is set automatically by the stack when creating (`true`) or receiving (`false`) one.

#### Permissions

Which documents will be shared. We provide their ids, and eventually a selector for a more dynamic solution (this will come later, though). See [here](https://github.com/cozy/cozy-stack/blob/master/docs/permissions.md) for a detailed explanation of the permissions format.

#### Recipients

An array of the recipients and, for each of them, their recipientID, the status of the sharing as well as their token of authentification and the refresh token, if they have accepted the sharing. 

The recipientID is the id the document storing the informations relatives to a recipient. The structure would be the following:
```json
{
    "type": "io.cozy.recipient",
    
    "url": "bob.url",
    "mail": "bob@mail",
    
    "oauth": {
        "client_id": "myclientid",
        "client_name": "myclientname",
        "client_secret": "myclientsecret",
        "registration_access_token": "myregistration",
        "redirect_uri": ["alice.cozy/oauth/callback"]
    }
}

```

From a OAuth perspective, Bob being Alice's recipient means Alice is registered as a OAuth client to Bob's Cozy. Thus, we store in this document the informations sent by Bob after Alice's registration.

- [ ] Stockage des informations clientes OAuth: comment sont-elles stockées dans la stack? N'y a t'il pas doublon ?

For the sharing status, the possible values are:
* `pending`: the recipient didn't reply yet.
* `accepted`: the recipient accepted.
* `refused`: the recipient refused.

#### Type

The type of sharing. It should be one of the followings: `master-master`, `master-slave`, `one-shot`.  
They represent the access rights the recipient and sender have:
* `master-master`: both recipient and sender can modify the documents and have their modifications pushed to the other.
* `master-slave`: only the sender can push modifications to the recipient. The recipient can modify localy the documents.
* `one-shot`: the documents are duplicated and no modifications are pushed.

#### Description

The answer to the question: "What are you sharing?". It is an optional field but, still, it is recommended to provide a small human-readable description.

#### ShareID

This uniquely identify a sharing. This corresponds to the id of the sharing document, on the sharer point of view. 

### Recipient's permissions

The recipient will need to give access rights to the sender. We will use the permission structure described [here](https://github.com/cozy/cozy-stack/blob/master/docs/permissions.md) sent by the sharer:

```json
    {
        "data": {
            "type": "io.cozy.permissions",
            "attributes": {
                "application-id": "xxx",
                "permissions": {
                    "type": "io.cozy.doctype1",
                    "verbs": ["GET","POST","PUT"],
                    "values": ["id1", "id2"],
                    "description": "Give it to me baby!"
                }
            }
        }
    }
```

#### Application-id

It is the identifiant of the sharing document that describes the sharing. It corresponds to the shareID sent by the sharer.

#### Type

The docType of the shared documents.

#### Verbs

The actions the sharer has to be able to do on the recipents Cozies. Combined with the `values` it limits those to the documents specified in the latter. The PUT verb is only needed for large documents.

#### Values

It corresponds to the documents specified by the sharer.


## Where to integrate the sharing code?

### cozy-stack/pkg/sharings

The implementation of the logic: creating a new sharing, handling an answer, starting a replication, etc…

### cozy-stack/web/sharings

The declaration of the routes and their chaining.


## Routes

### POST /sharings

Create a new sharing.

### PUT /sharings/:id

Receive a sharing request.

### POST /sharings/:id/answer

Answer a sharing request.

### DELETE /sharings/:id

Delete the specified sharing (both the sharing document and the associated permission).

