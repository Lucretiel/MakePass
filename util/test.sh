#!/bin/sh

OUTPUT_FILE="$(mktemp)"
LOG_FILE="$(mktemp)"

quit() {
	rm $OUTPUT_FILE $LOG_FILE
	exit "$1"
}

for i in {1..20}
do
	printf '.'
	if ! make_pass -v --min_length=24 >> "$OUTPUT_FILE" 2> "$LOG_FILE"
	then
		printf "\nSomething went wrong!\n"
		cat "$LOG_FILE"
		quit 1
	fi
done
echo

assert_pattern () {
	pattern="$1"
	error_msg="$2"

	if MISMATCH="$(grep -Ev "$pattern" < "$OUTPUT_FILE")"
	then
		echo "$error_msg"
		echo "$MISMATCH"
		quit 1
	fi
}

assert_pattern '^.{24,}$' \
	"make_pass exited successfully, but this password(s) isn't long enough"

PATTERN='^([A-Z][a-z]{3,7}){4}[0-9]$'
assert_pattern "$PATTERN" \
	"make_pass exited successfully, but this password(s) doesn't match the pattern $PATTERN" \

echo "All tests passed!"
quit 0
