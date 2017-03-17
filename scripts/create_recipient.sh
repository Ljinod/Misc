#!/bin/bash

# This script was intended for Cozy V3.
#
# This script aims at facilitating the creation of a recipient. It will need a
# token that corresponds to a client that has the rights to create a document
# which doctype is `io.cozy.recipients`.

if [ -z "$COZY_STACK_TOKEN" ]; then
	echo "[ERROR]\t The environment variable COZY_STACK_TOKEN is not set."
	echo "\t Do not execute the generate_token script, source it instead:"
	echo "\v\t source generate_token.sh [domain]"
	exit 1
fi

if [ -z "$COZY_STACK_DOMAIN" ]; then
	echo "[ERROR]\t The environment variable COZY_STACK_DOMAIN is not set."
	echo "\t Please source a generate_token script to set it:"
	echo "\v\t source generate_token.sh [domain]"
	exit 2
fi

RECIPIENT_JSON='
{
	"email": "julien@cozycloud.cc",
	"url": "url.bidon.fr",
	"client": {
		"client_id": "1234BEPO",
		"redirect_uris": [
			"redirect.url.fr/sharings/answer"
		],
		"client_name": "toto",
		"software_id": "toto.test.0"
	}
}
'

export RECIPIENT_ID=$(curl -s -X POST \
	-H "Authorization: Bearer $COZY_STACK_TOKEN" \
	-H "Host: $COZY_STACK_DOMAIN" \
	-H "Accept: application/json" \
	-H "Content-Type: application/json" \
	http://localhost:8080/data/io.cozy.recipients/ -d "$RECIPIENT_JSON" \
	| jq --raw-output '.data | ._id')

if [ -z "$RECIPIENT_ID" ]; then
	echo "[ERROR]\t The recipient could not be created."
	exit 3
fi

echo "[INFO]\t Recipient id: $RECIPIENT_ID"
