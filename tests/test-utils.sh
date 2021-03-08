#!/bin/sh

usage="Usage: $(basename $0) [-h|--help] [--debug] MODULE_TO_TEST: tests the Python toolbox module provided as argument.
Ex: $(basename $0) file_utils.py"

if [ $# -eq 0 ]; then
	echo "  Error, not enough arguments.
${usage}" 1>&2
	exit 5
fi

if [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
	echo "${usage}"
fi

if [ "$1" = "--debug" ]; then
	do_debug=0
	shift
else
	do_debug=1
fi

tested_module_path="$(dirname $(pwd))"

# Ex: "file_utils.py"
tested_module="$1"
#echo "tested_module = ${tested_module}"

# Ex: "file_utils_test.py"
testing_module="$(echo "${tested_module}" | sed 's|\.py$|_test.py|1')"
#echo "testing_module = ${testing_module}"

test_target="${tested_module_path}/tests/${testing_module}"

if [ ! -f "${test_target}" ]; then
	echo "  Error, no test target available ('${test_target}').
${usage}" 1>&2
	exit 15
fi


debug()
# Displays a debug message iff debug mode is activated (do_debug=0).
# Usage: debug "message 1" "message 2" ...
{
	[ $do_debug -eq 1 ] || echo "[Debug] $*"
}



export PYTHONPATH="${tested_module_path}:$PYTHONPATH"

echo

debug "Tested module path is '${tested_module_path}'."
debug "Test target is '${test_target}'."

if [ $do_debug -eq 0 ]; then
	python -i ${test_target}
else
	${test_target}
fi
