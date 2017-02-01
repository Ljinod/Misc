# OAuth2 and sharing

## Use case

Alice wants to share a set of documents with Bob, and it is Alice's Cozy that will push the data to Bob's Cozy.  
For that Bob needs to give some access rights to Alice so that her Cozy can transfer the data.

We thought of the following protocol:
1. With the sharing request Alice's Cozy generates a "_pretoken_", unique to Bob and to this request. This _pretoken_ will serve as a means of authentication for Bob when he replies, to ensure that it is indeed him.
2. If Bob accepts the request his Cozy generates a "_token_", unique to Alice and to this request. This _token_ will serve as a means of authentication for Alice when she sends the data, again to ensure that it is indeed her.
3. In the reply, Bob's Cozy incorporates both the _pretoken_ and the _token_ so that Alice's Cozy can check the correctness of the reply and get her _token_ to push the documents.


## Draft: OAuth workflow with sharing

1. Alice's Cozy asks for a `client_id`, a `client_secret`, and a `registration_access_token` using the "OAuth2 Dynamic Client Registration Protocol".
    * [POST /auth/register](https://github.com/cozy/cozy-stack/blob/master/docs/auth.md#post-authregister)
    * Parameters passed:
        * `redirect_uris`: ["https://alice.example.com/sharings/answer"]
        * `client_name`: Bob
        * `software_id`: "github.com/cozy/cozy-stack"
        * `client_kind`: sharing
        * `client_uri`: the url of Bob's Cozy
        * `policy_uri`: (Cozy's privacy policy?)


2. Alice's Cozy asks for an authorization. It will send a special email in her sted to Bob, specifying the permissions needed in the form of a url that Bob's Cozy can interpret. When Bob copy-pastes the url in his Cozy, the permissions will be displayed and Bob will be asked to accept or decline. If Bob accepts his Cozy will send Alice's an `access code`. If he declines the process stops there.
    * [GET /auth/authorize](https://github.com/cozy/cozy-stack/blob/master/docs/auth.md#get-authauthorize)
    * Parameters passed:
        * `client_id`: id obtained at step 1
        * `redirect_uri`: "https://alice.example.com/sharings/answer"
        * `state`: the id of the sharing
        * `response_type = code`
        * `scope`: the permissions asked


3. Alice's Cozy finally asks for an `access_token` and its corresponding `refresh_token` with which it will be able to push the documents. For that it will need its `client_id`, `client_secret` and `access_code`.
    * [POST /auth/access_token](https://github.com/cozy/cozy-stack/blob/master/docs/auth.md#post-authaccess_token)
    * /!\\ **WARNING**: the `access_code` is only valid for 5 minutes so if there is a problem within that time interval and Alice is enable to request an `access_token` she will have to start over.
    * Parameters passed:
        * `grant_type = authorization_code`
        * `code`: code obtained at step 2
        * `client_id`: id obtained at step 1
        * `client_secret`: secret obtained at step 1


4. The token will only be valid for 24 hours so every time Alice's Cozy wants to send an update it will have to repeat step 3 for a new `access_token`.
    * Parameters passed:
        * `grant_type = refresh_token`
        * `refresh_token`: token obtained at step 2
        * `client_id`: id obtained at step 1
        * `client_secret`: secret obtained at step 1


5. Every time Alice wants to share another set of documents, her Cozy will only repeat the steps 2 to 4.


## OAuth workflow with sharing?

For now there is one problem: at the end of the step 3 in the draft proposition, in OAuth it is specified that Bob should be redirected to the url given in `redirect_uri`. In our case it makes no sense to redirect Bob to Alice's Cozy: he will see Alice's login screen and he won't be able to do anything.
