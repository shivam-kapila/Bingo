#!/bin/bash

function setup_cron {
    echo "Creating user bingo if it doesn't exist..."
    id -u bingo &>/dev/null || useradd bingo

    echo "Adding cron entry..."
    crontab -l -u bingo > results-crontab
    echo "* * * * * cd '$PWD' && source bingo/bin/activate && /usr/bin/python3 compute_results.py >> >/dev/null 2>&1" >> results-crontab
    crontab -u bingo results-crontab
    rm results-crontab
}


if [[ "$1" == "cron" ]]; then
    setup_cron
fi