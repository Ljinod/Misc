#!/bin/bash

# This script was intended for Cozy V3.

if [ $# -gt 0 ]; then
	SHARING_ID="$1"
else
	echo "[ERROR]\t Please give me a sharing id"
	exit 1
fi

curl -s -X POST \
	-H "Host: $COZY_STACK_DOMAIN" \
	-F 'state="$SHARING_ID"' \
	http://localhost:8080/sharing/formRefuse
