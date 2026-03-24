#!/bin/bash
args=$@
SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &> /dev/null && pwd)
export TMPDIR="${SCRIPT_DIR}/tmp"

for arg in ${args[@]}
do
    if [[ $arg == '-h' ]] || [[ $arg == '--help' ]]; then
        ${SCRIPT_DIR}/bin/python ${SCRIPT_DIR}/automata_browser/auto_browser.py -h
        exit 0
    elif [[ $arg == '-t' ]] || [[ $arg == '--test' ]]; then
        ${SCRIPT_DIR}/bin/python ${SCRIPT_DIR}/automata_browser/auto_browser.py -t
        exit 0
    fi
done

if [[ $(echo ${args[@]} | wc -w) -eq 0 ]]; then
    ${SCRIPT_DIR}/bin/python3 -i ${SCRIPT_DIR}/automata_browser/auto_browser.py ${args[@]}
else
    ${SCRIPT_DIR}/bin/python3 ${SCRIPT_DIR}/automata_browser/auto_browser.py ${args[@]}
fi
