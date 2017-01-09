# Sharing use cases for Cozy V3

The goal of this file is to be able to determine what we need in the stack to implement the sharing feature.


## Create a new sharing

1. The user gives a list of documents' IDs corresponding to: containers (folders, albums, etc…) and/or documents.
2. The "sharing process" computes the actual list of documents to share (by getting the children of the containers).
3. The "sharing process" waits until a threshold is reached (we wait for a timeout or a full buffer) and then starts replications.
4. The "sharing process" updates the "monitoring lists" by adding the ids of the new shared documents.


## Propagating updates

1. The "sharing process" fetches all the updates of all the databases and compare those with the lists of "parentsIDs" and "IDs" of shared documents.
2. The "sharing process" starts replication after a threshold is reached (after a timeout or a full buffer).


## Handling conflicts

1. We let CouchDB resolve the conflict.
2. We create a new document with the loosing revision, we just append to the original name "__CONFLICT".
3. Users are free to do what they want with those afterwards.


## Modifying a sharing

* Adding recipient(s).
* Removing recipient(s).

* Adding document(s).
* Removing document(s).

* Changing access rights.


## (BONUS) Devices

* Being able to share from different devices (smartphone).
