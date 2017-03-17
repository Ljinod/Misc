#!/bin/bash

# This script was intended for Cozy V3.
#
# This script aims at facilitating the creation of a sharing.
#
# A sharing requires at least one recipient (there is no point in sharing with
# noone) so this script expects the environment variable $RECIPIENT_ID to be
# set.

if [ -z "$RECIPIENT_ID" ]; then
	echo "[ERROR]\t The environment variable RECIPIENT_ID is not set."
	echo "\t Do not execute the create_recipient script, source it instead:"
	echo "\v\t source create_recipient.sh"
	exit 1
fi

SHARING_JSON='
{
    "permissions": {
        "tests": {
            "description": "test",
            "type": "io.cozy.tests",
            "verbs": ["GET", "POST"],
            "values": ["test-id"]
        }
    },
    "recipients": [
        {
            "recipient": {
                "type": "io.cozy.recipients",
                "id": "'$RECIPIENT_ID'"
            }
        }
    ],
    "desc": "I want you to go elsewhere!",
    "sharing_type": "one-shot"
}
'

export SHARING_ID=$(curl -s -X POST \
	-H "Host: $COZY_STACK_DOMAIN" \
	-H "Content-Type: application/json" \
	http://localhost:8080/sharings/ -d "$SHARING_JSON" \
	| jq --raw-output '.data | .id')

if [ -z "$SHARING_ID" ]; then
	echo "[ERROR]\t The sharing could not be created."
	# exit 1
fi

echo "[INFO]\t Sharing id: $SHARING_ID"
