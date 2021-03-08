#!/bin/sh

usage="Usage: $(basename $0) [--debug]: tests all available Python modules"


if [ "$1" = "--debug" ]; then
	do_debug=0
else
	do_debug=1
fi


tested_module_path=$(dirname $(pwd))

export PYTHONPATH=${tested_module_path}:$PYTHONPATH


debug()
# Displays a debug message if debug mode is activated (do_debug=0).
# Usage: debug "message 1" "message 2" ...
{
	[ $do_debug -eq 1 ] || echo "[Debug] $*"
}

echo "Testing all:"

for t in ${tested_module_path}/tests/*_test.py; do

	echo
	echo "Testing with $t:"
	$t

done

echo "End of all tests."
