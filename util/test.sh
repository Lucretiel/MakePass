#!/bin/sh

OUTPUT_FILE="$(mktemp)"

if ! make_pass -v --min_length=24 > "$OUTPUT_FILE"
then
    echo "Something went wrong!"
    exit 1
fi

if test "$(cat "$OUTPUT_FILE" | tr -d ' \n\t' | wc -c)" -ge 24
then
	echo "Successfully generated password!"
else
	echo "make_pass exited successfully, but the password isn't large enough"
	echo "Password: '$(cat "$OUTPUT_FILE")'"
	exit 1
fi
