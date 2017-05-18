#!/bin/bash

# This script was intended for Cozy V3.
#
# This script aims at facilitating the creation of an OAuth client that has
# the necessary rights to create a recipient (doctype: io.cozy.recipients).

if [ $# -gt 0 ]; then
	export COZY_STACK_DOMAIN="$1"
else
	export COZY_STACK_DOMAIN="cozy1.local:8080"
fi

COZY_CLIENT_ID=$(cozy-stack instances client-oauth "$COZY_STACK_DOMAIN" \
	http://$COZY_STACK_DOMAIN cli-test github.com/cozy/test)

export COZY_STACK_TOKEN=$(cozy-stack instances token-oauth \
	"$COZY_STACK_DOMAIN" "$COZY_CLIENT_ID" io.cozy.photos)

if [ -z "$COZY_STACK_TOKEN" ]; then
	echo "[ERROR]\t The token could not be generated."
	exit 1
fi

echo "[INFO]\t A token was generated for domain" "$COZY_STACK_DOMAIN"
echo -n "[INFO]\t "
echo $COZY_STACK_TOKEN
