#!/bin/bash

export PROD_ONLY=
if [[ $DESECSTACK_E2E_TEST = "TRUE" ]]
then
    export PROD_ONLY='#'
fi

for file in www/conf/sites-available/*.var www/conf/donf.d/*.var; do
    # we only replace occurances of the variables specified below as first argument
    (envsubst "$DESECSTACK_IPV4_REAR_PREFIX16" |
    envsubst "$DESECSTACK_DOMAIN" |
    envsubst "$CERT_PATH" |
    envsubst "$PROD_ONLY" ) < "$file" > "$DIR"/$(basename "$file" .var)
done
