# Bingo

![Bingo](/webserver/static/img/logo.png?raw=true "Bingo")

Bingo is a service which allows users to get Lucky Draw Raffle tickets
and use one lucky draw raffle ticket to participate in a lucky draw game. Draw a ticket and win exciting prizes!


# Table of Contents

- [Setting up Bingo](#setting-up-bingo)
    + [Clone Bingo](#clone-bingo)
    + [Install dependencies](#install-dependencies)
      - [Install python dependencies](#install-python-dependencies)
      - [Install node dependencies](#install-node-dependencies)
    + [Initialize the database](#initialize-the-database)
    + [Set up the results computation cron job](#set-up-the-results-computation-cron-job)
    + [Run Bingo](#run-bingo)
- [API Endpoints](#api-endpoints)
    + [`/luck-draw/get-raffle/<int:raffle_id>` [GET]](#--luck-draw-get-raffle--int-raffle-id----get-)
    + [`/luck-draw/get-past-raffles` [GET]](#--luck-draw-get-past-raffles---get-)
    + [`/luck-draw/get-last-week-raffles` [GET] [GET]](#--luck-draw-get-last-week-raffles---get---get-)
    + [`/luck-draw/get-next-raffle` [GET]](#--luck-draw-get-next-raffle---get-)
    + [`/get-upcoming-raffles` [GET]](#--get-upcoming-raffles---get-)
    + [`/luck-draw/get-ongoing-raffles`[GET]](#--luck-draw-get-ongoing-raffles--get-)
    + [`/luck-draw/draw-ticket` [POST]](#--luck-draw-draw-ticket---post-)
    + [`/luck-draw/get-tickets` [GET]](#--luck-draw-get-tickets---get-)
    + [`/luck-draw/enter-raffle/<int:raffle_id>` [POST]](#--luck-draw-enter-raffle--int-raffle-id----post-)
    + [`/luck-draw/create-raffle` [POST]](#--luck-draw-create-raffle---post-)


# Setting up Bingo

### Clone Bingo

Bingo is hosted on GitHub at [https://github.com/shivam-kapila/Bingo/](https://github.com/shivam-kapila/Bingo/).
You can use `git` to clone it to your computer

    git clone https://github.com/shivam-kapila/Bingo.git

### Install dependencies

To work on the project, you first need to install [Python](https://www.python.org/downloads/), [Node.js](https://nodejs.org/en/download/) and [PostgreSQL](https://www.postgresql.org/download/). Follow the respective links and download them for your platform.

#### Install python dependencies

Install `virtualenv` using the command:

    pip install virtualenv

Move into the project directory and create a virtual environment, and install the python dependencies by running the following commands:

	virtualenv bingo
    source bingo/bin/activate
    pip install -r requirements.txt

#### Install node dependencies

Install the node dependencies using the command:

	npm install

The dependencies have been installed and you are good to proceed.


### Initialize the database

To initialize the database for the first time, run the following command:

	./develop.sh init_db --create-db

In case you need to reset the database, run:

	./develop.sh init_db -f

**Note:** In case of the error `peer authentication failed for user "postgres"`, follow the steps given [here](https://docs.boundlessgeo.com/suite/1.1.1/dataadmin/pgGettingStarted/firstconnect.html#setting-a-password-for-the-postgres-user).


### Set up the results computation cron job

The results of lucky draw raffles are calculated, by invoking the `compute_results.py` file every hour. TO setup this cron job run:

	./develop.sh cron	./develop.sh cron


This creates a user `bingo` if it doesn't exist and adds the new cron job to the existing ones.


### Run Bingo

Now the project is setup and ready to run. To run the project run the given command.

	./develop.sh

Additionally you can specify the `host`, `port` and `debug` values, to run the Flask server like this:

	./develop.sh ---host=<host> --port=<port> -debug

or use the shorthand flags as follows:

	./develop.sh-h=<host> -p=<port> -d


# API Endpoints

All these API endpoints require a valid Authorization Header of the form `Token <auth_token>`.

### `/luck-draw/get-raffle/<int:raffle_id>` [GET]

Get raffle with the given `raffle_id`. Returns the raffle applicants too, in case the user is an admin.

**Headers:**
- Authorization: `Token auth_token`

**Returns:**
- raffle: the raffle record for the given `raffle_id`.


### `/luck-draw/get-past-raffles` [GET]

**Headers:**
- Authorization: `Token auth_token`

**Returns**:
- raffles: the list of raffles.

### `/luck-draw/get-last-week-raffles` [GET] [GET]

Get a list of last week raffles.

**Headers:**
- Authorization: `Token auth_token`

**Returns**:
- raffles: the list of raffles.



### `/luck-draw/get-next-raffle` [GET]

**Headers:**
- Authorization: `Token auth_token`

Get the next raffle.

**Returns:**
- raffle: the next raffle.


### `/get-upcoming-raffles` [GET]
Get a list of upcoming raffles.

**Headers:**
- Authorization: `Token auth_token`

**Returns**:
- raffles: the list of raffles.

### `/luck-draw/get-ongoing-raffles`[GET]

Get a list of ongoing raffles.

**Headers:**
- Authorization: `Token auth_token`

**Returns**:
- raffles: the list of raffles.



### `/luck-draw/draw-ticket` [POST]
Draw a new ticket for the given user.

**Headers:**
- Authorization: `Token auth_token`

**Returns**:
- ticket: the newly drawn ticket.


### `/luck-draw/get-tickets` [GET]
def get_tickets_for_user():
    """ Get a given user's tickets.

**Headers:**
- Authorization: `Token auth_token`

**Returns**:
- tickets: the tickets of the given user.


### `/luck-draw/enter-raffle/<int:raffle_id>` [POST]

Create an entry for the given user for the raffle ``raffle_id``. The earliest valid non-redeemed ticket is used to enter the raffle.
**Headers:**
- Authorization: `Token auth_token`

**Raises**:
 - BadRequest(404): The user has no valid non-redeemed tickets
 - BadRequest(404): The raffle doesn't exist
 - BadRequest(404): The raffle entries are closed
 - Conflict(409): The user has already entered the raffle



### `/luck-draw/create-raffle` [POST]

Create a new raffle. This endpoint is admin only.

**Headers:**
- Authorization: `Token auth_token`

**Raises**:
- BadRequest(401): The user is not an authorized admin
- BadRequest(404): Incomplete form POSTed

**Returns**:
- raffle_id: the id of the newly created raffle.
