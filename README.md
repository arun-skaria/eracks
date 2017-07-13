[![wercker status](https://app.wercker.com/status/db7ec8a2b84453468ca275f066b91cb6/s/master "wercker status")](https://app.wercker.com/project/byKey/db7ec8a2b84453468ca275f066b91cb6)

[![CircleCI](https://circleci.com/gh/jowolf/eracks11.svg?style=svg&circle-token=f61a2dd555166e6a8327e0534db5da05ec0f3f99 "CircleCI Status")]
(https://circleci.com/gh/jowolf/eracks11)

eracks11
========

eRacks website private repository

Originally imported from eracks10 with svn2git, circa July 2014

Added Wercker build status widget Oct 5, 2016


Welcome new developers
----------------------

As of Oct 6, 2016, the master branch is the current one.

We are working a new docker-based local development environment script. Stay tuned.
UPDATE: Docker dev envo complete - See below - 

NOTE:

- If you see cruft or what you think is dead code, move it to old/ and run a full test suite - if it passes, check it in!
- We will purge the old/ directory periodically every major release

You can use either a local docker environment, or a local dev environment - the Docker-based environment is better if you want to keep the eRacks environment and packages isolated from your own local desktop or laptop.


Initial Setup and requirements
------------------------------

- A local Linux environment - Ubuntu 14.04 or 16.04, Linux Mint 17.x or 18, etc - Ubuntu and Mint have been tested
- git installed
- Additional requirements depending on which environment you want, below:

Pull the eracks11 repo (This one you are reading!):

    git clone https://github.com/jowolf/eracks11.git

Now read on for which environment is best for you:


Local Docker Enviroment
-----------------------

Additional requirement: Docker installed

Change to the eracks11/conf/ directory:

    cd eracks11/conf/

Do initial Docker build and pull (see the script for details):

    ./docker-build.sh

This will build the local eracks11 Docker container, and pull the official Postgres Docker container. This typically only needs to be done *once*, pending any changes in the Docker environemnt or the eRacks Dockerfile.
Remember, no state is kept in the docker eracks11 container, everything is in the repo (shared as a volume) and the database.

Initialize the eRacks-postgres db container and configure the empty database:

    ./docker-init.sh

This can be run to reinitialize the db as desired, but keep in mind it's *destructive*!  See the script for details.

Set up initial eRacks-postgres db container, then run, link, and fill the eracks11 container and db:

    ./docker-setup.sh

This runs the setup-envo, setup-db, and setup-search scripts, in the context of the new Django environment inside the eracks11 container.  See this and the various other scripts for details.

These scripts (look them over!) do initial migrations, compile themes, collect static files, load the db from fixtures, etc.

Now you can use the docker-manage script, just like you would ./manage.py, eg:

    ./docker-manage.sh check
    ./docker-manage.sh runserver (runs on 127.0.0.1:8000)
    ./docker-manage.sh runserver 0:8000 (visible to other hosts, etc)
    ./docker-manage.sh help
    ./docker-manage.sh collectstatic -l
    ./docker-manage.sh test apps.home.tests

and so on.

Be sure to run:

    docker-manage.sh test

When you're done, there are around 126 tests which should all pass OK.

That's it!

No need to even enter the Docker instance (unless you need to solve problems or fix something).

See also Docker pasteables below.


Local dev environmnt
--------------------

Additional requirements: python, pip, (also virtualenv if desired), PostgreSQL client & server installed locally.

Because these steps are called from several places (environment setup, saltstack-based deployment for prod/dev/staging, Wercker CI or Circle CI Continuous Integration and testing), the steps are broken up into separate scripts.

Change to the eracks11/ directory:

    cd eracks11/

Make sure other required packages are installed:

    ./conf/install-packages.sh

This installs the basic packages required by both the eRacks Django project and the Postgres client.  Look it over, and if you find a (non-python) package needed by some work your're doing, add it here.

Set up npm packages:

    npm install --global stylus bower
    npm list --global

Stylus is used by the theme compiler, and bower is not currently used, but planned to be used shortly as we re-vamp our themes and workflow!

Set up pip requirements:

    cd conf/
    pip install -r requirements.txt
    cd ..

or, if you want a virtualenv:

    cd conf/
    virtualenv env (note: you may need the --system-site-packages flag if you want the system's psycopg, or install it localy in the venv)
    pip install -r requirements.txt
    cd ..

Now set up the local Django environment (be sure you're back in the eracks11/ dir!)

    ./setup-envo.sh

This will compile themes, collect static (symlinks), and

Set up the and load the database:

    ./setup-db.sh

Initialize the haystack search engine:

    ./setup-search.sh

That's it! You should be up and running -

    ./manage.py check
    ./manage.py runserver

And so on.

Be sure to run:

    ./manage.sh test

When you're done, there are around 126 tests which should all pass OK.



Compiling themes
----------------

./manage.py compilethemes

or ./docker-manage.sh compilethemes



Useful Docker pasteables
------------------------

Be sure to note the backticks -

Remove the last nn containers:

    sudo docker rm `sudo docker ps -n <nn> -q`

Remove all the built images (does not affect current repo, but requires docker rebuild):

    sudo docker rmi `sudo docker images -q <image name, eg eracks11>`

Run the current eracks11 container and go inside it (Only needed for troubleshooting):

Assuming you are in your own project directory (eg, something like /home/dev/eracks11):

    export projectdir=`pwd`
    sudo docker run -itv $projectdir:$projectdir --net host -e PROMPT_COMMAND="echo IN DOCKER:" eracks11

Re-run the eracks-postgres database container (once it's been initialized for the first time):

    sudo docker start eracks-postgres

See the Docker cli docs as well: https://docs.docker.com/engine/reference/commandline/cli/


Secure Messaging
----------------

We use Telegram for secure messaging - https://telegram.org/

There are clients available for every platform, Desktop, Android, iOS, Linux, Windows MacOS, etc.

Our CTO's (writing this) username is jowolf.

JJW
