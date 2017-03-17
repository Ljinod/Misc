#!/bin/bash

# This script was intended for Cozy V3.
#
# This script aims at facilitating the testing of the "sharing mail invitation".
# This script will either:
#   * Call the route: /sharings/:id/sendMails if the environment variable
#     $SHARING_ID is set.
#   * Create a new oauth client for the domain provided, ask for a new token,
#     create a new recipient, and finally create a new sharing. When each of
#     actions are created, the following environment variables are created:
#       * COZY_STACK_DOMAIN: the domain, it defaults to "localhost:8080";
#       * COZY_CLIENT_ID: the id of the oauth client created;
#       * COZY_STACK_TOKEN: the token given by the stack to the oauth client;
#       * RECIPIENT_ID: the id of the recipient created;
#       * SHARING_ID: the id of the sharing created.

if [ -z "$SHARING_ID" ]; then
	if [ "$1" != "" ]; then
		source generate_token.sh "$1"
	else
		source generate_token.sh
	fi

	source create_recipient.sh
	source create_sharing.sh

	if [ "$?" = "0" ]; then
		echo "[INFO]\t Mail was normally sent, check your inbox!"
	else
		echo "[ERROR]\t An error occurred, the mail was NOT sent."
	fi
else
	curl -s -X PUT \
		-H "Host: $COZY_STACK_DOMAIN" \
		-H "Content-Type: application/json" \
		http://localhost:8080/sharings/"$SHARING_ID"/sendMails

	echo "[INFO]\t Mail was normally sent, check your inbox!"
fi
