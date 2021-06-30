#!/bin/bash

install_dependencies() {
    pip3 install -r requirements.txt
}

find_diff_transactions() {
    new_tradebook=$1
    old_tradebook=$2
    diff_tradebook=$3

    head -n 1 ${new_tradebook} > ${diff_tradebook}
    pyset ${new_tradebook} ${old_tradebook} --operation subtract >> ${diff_tradebook}
}

preprocess_as_pp_input() {
    tradebook=$1
    output_tradebook=$2
    python3 preprocess.py --input_csv "${tradebook}" --output_csv "${output_tradebook}" --use_exchange "NSE"
}

install_dependencies

if [ "$1" = "new" ]; then
    tradebook=$2
    output_tradebook="out_${tradebook}"
    echo "Parsing new tradebook ${tradebook}"
    preprocess_as_pp_input "${tradebook}" "${output_tradebook}"

elif [ "$1" = "add" ]; then
    new_tradebook=$2
    old_tradebook=$3
    diff_tradebook="diff_$2"
    output_tradebook="out_${diff_tradebook}"
    echo "Finding new transactions in ${new_tradebook} compared to ${old_tradebook}"
    find_diff_transactions "${new_tradebook}" "${old_tradebook}" "${diff_tradebook}"
    preprocess_as_pp_input "${diff_tradebook}" "${output_tradebook}"

fi
