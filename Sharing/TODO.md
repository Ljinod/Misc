# Cozy-sharing TODO list

* Adapt the protocol/diagrams to the different types of sharing:
    * [x] Master-master
    * [x] Master-slave
    * [x] One-shot

* Diagrams to add:
    * [x] Modifying a sharing (add/remove recipients/documents)
    * [x] Deleting a sharing (initiator/recipient perspective, Master-Master share)
    * [x] Creating a sharing
    * [x] Receiving a request by mail
    * [x] Sending binaries (included in 5-New-sharing-dedicated-process)
    * [x] Receiving replication

* [ ] Specify who is the originator of a sharing somehow, somewhere.
* [x] In the diagrams show that the replication must be routed on a special route where we can check that the documents are legit.

* [x] In the creation step if the type is "Master-Master" check for each document if it is already shared with someone else in "Master-Master". If it is then the creation must be forbidden because modifications to the incriminated documents could impact more than just the recipients.
* [x] In the creation step add a "shared" tag to all documents that are shared.
* [x] Add a "owner" field in the sharing document.

* [x] In "2-Sending-sharing-request" specify how to send the request by mail.


# Misc questions

* One sharing multiple docTypes (hence databases)?
* UX: What happens if there is a "name" collision?
* How do we present the "filter" to the end-user? What format could we use to display something understandable?
