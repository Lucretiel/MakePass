#!/bin/sh

OUTPUT_FILE="$(mktemp)"

if ! make_pass -v --min_length=24 > "$OUTPUT_FILE"
then
    echo "Something went wrong!"
    exit 1
fi

test_or () {
	error_msg="$1"
	shift

	if ! "$@"
	then
		echo "$error_msg"
		echo "Password: '$(cat "$OUTPUT_FILE")'"
		exit 1
	fi
}


test_or "make_pass exited successfully, but the password isn't large enough" \
	test "$(cat "$OUTPUT_FILE" | tr -d ' \n\t' | wc -c)" -ge 24


PATTERN='^([A-Z][a-z]{3,7}){4}[0-9]$'
test_or "make_pass exited successfully, but the password doesn't match the pattern $PATTERN" \
	grep -Eq "$PATTERN" "$OUTPUT_FILE"

echo "All tests passed!"
