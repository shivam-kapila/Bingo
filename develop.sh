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

function run_prod {
    echo "Creating static files..."
    npm run build:prod

    echo "Starting Flask server..."
    python3 manage.py run_server
}

function run_dev {
    echo "Running webpack and Flask server..."
    npm run build:prod &
    python3 manage.py run_server -d
}


if [[ "$1" == "cron" ]]; then
    setup_cron
elif [[ "$1" == "-d" ]]; then
    run_dev
else
    run_prod
fi
