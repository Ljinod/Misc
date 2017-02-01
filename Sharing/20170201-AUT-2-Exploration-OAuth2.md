# OAuth2 and sharing

## Use case

Alice wants to share a set of documents with Bob, and it is Alice's Cozy that will push the data to Bob's Cozy.  
For that Bob needs to give some access rights to Alice so that her Cozy can transfer the data.

We thought of the following protocol:
1. With the sharing request Alice's Cozy generates a "_pretoken_", unique to Bob and to this request. This _pretoken_ will serve as a means of authentication for Bob when he replies, to ensure that it is indeed him.
2. If Bob accepts the request his Cozy generates a "_token_", unique to Alice and to this request. This _token_ will serve as a means of authentication for Alice when she sends the data, again to ensure that it is indeed her.
3. In the reply, Bob incorporates both the _pretoken_ and the _token_ so that Alice can check the correctness of the reply and get her _token_ to push the documents.


## OAuth workflow

1. Alice asks for a `client_id`, a `client_secret`, and a `registration_access_token` using the "OAuth2 Dynamic Client Registration Protocol".
    * [POST /auth/register](https://github.com/cozy/cozy-stack/blob/master/docs/auth.md#post-authregister)
    * Parameters passed:
        * `redirect_uris`: (idk, see todo below)
        * `client_name`: Bob
        * `software_id`: (RNG?)
        * `client_kind`: sharing
        * `client_uri`: the url of Bob's Cozy
        * `policy_uri`: (Cozy's privacy policy?)


2. Alice asks for an authorization. If Bob accepts she will receive an `access code`.
    * [GET /auth/authorize](https://github.com/cozy/cozy-stack/blob/master/docs/auth.md#get-authauthorize)
    * Parameters passed:
        * `client_id`: id obtained at step 1
        * `redirect_uri`: (idk)
        * `state`: RNG
        * `response_type = code`
        * `scope`: the permissions asked


3. Alice finally asks for an `access_token` and its corresponding `refresh_token` with which she will be able to push the documents. For that she will need her `client_id`, `client_secret` and `access_code`.
    * [POST /auth/access_token](https://github.com/cozy/cozy-stack/blob/master/docs/auth.md#post-authaccess_token)
    * /!\\ **WARNING**: the `access_code` is only valid for 5 minutes so if there is a problem within that time interval and Alice is enable to request an `access_token` she will have to start over.
    * Parameters passed:
        * `grant_type = authorization_code`
        * `code`: code obtained at step 2
        * `client_id`: id obtained at step 1
        * `client_secret`: secret obtained at step 1


4. The token will only be valid for 24 hours so every time Alice wants to send an update she will have to repeat step 3 for a new `access_token`.
    * Parameters passed:
        * `grant_type = refresh_token`
        * `refresh_token`: token obtained at step 2
        * `client_id`: id obtained at step 1
        * `client_secret`: secret obtained at step 1


- [ ] Je ne vois quelle(s) valeur(s) on peut mettre dans `redirect_uri`…
- [ ] Est-ce qu'on refait toute la danse à chaque partage ou est-ce qu'on garde les mêmes `client_id`, `client_secret` pour un destinataire et on demande un nouvel `access_token` pour un nouveau partage ? Est-ce qu'il y a des raisons pour refaire toute la danse ?


## OAuth workflow with sharing?

I don't see any incompatibilities between the protocol we thought and the OAuth danse: we can adapt the first to match the second, which, in addition, increase the security with the notion of "token renewal".

- [ ] Répondre aux questions ci-dessus pour être absolument certain que c'est le cas.
