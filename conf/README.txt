9/23/16 JJW

deploy.sh <instance> is now for remote only - dev, prod, staging - 
and installs PostgreSQL, and nginx (in the case of prod &* staging)

it is not strictly necessary for local dev, for which the new vagrant/docker 
mechanism works great, and you can connect to a remote db via port forwarding.


JJW 1/7/16 migration
sudo pip install django-loginas


JJW 12/24/15 migration:

# Do them in this order, as the first two install 1.9 Django, we need 1.8

sudo pip install "django-guardian>=1.3.2" --upgrade
sudo pip install "pyjade>=3.1" --upgrade
sudo pip install "django-debug-toolbar>=1.3" --upgrade
sudo pip install Django==1.8 --upgrade

Anything else? (What else did Mani install/upgrade?)


Mani 10/26/2015:
Test Cases:
All our test cases are there in each app in tests.py file.
- to run all our test cases we can use  'python manage.py test'
- to run particular app test cases, use 'python manage.py test App-name'
- to run particular test case we need to run like ' python manage.py test App-Name.tests.TestCaseClassName'
- to run tests against production database we have some management test commands
-     ' python manage.py test_production_livedb '
      ' python manage.py longemail_test.py '
      ' python manage.py test_long_email '


JJW 10/4-10/5/15 added:
sudo pip install Werkzeug
sudo pip install django-extensions
sudo pip install django-easy-select2
  ./manage.py collectstatic -l
sudo pip install -e git+https://github.com/jowolf/django-webshell.git#egg=django-webshell
  ./manage.py migrate webshell

(No migration added, only added to requirements.txt - cut & paste the above)


JJW 8/29/15
- We now use ./salt-requirements.sh, which:
  - Runs requirements.sls as a salt state
  - Places the requirements in a python venv (env/)
- This should be run from this directory (conf).
- The requirements.sls will undo old cruft and ensure idempotent consistency prior to installing requirements.txt in the venv
- We could convert the whole thing to salt, see txt2sls.py
- When creating incremental requirements changes, put them BOTH in requirements.txt, AND in the migrations/ subdir.

JJW 1/13/15
  571  pip install Pillow --upgrade
  572  # install libjpeg-dev with apt
  573  sudo apt-get install libjpeg-dev
  574  pip install -I Pillow


JJW 12/28/14 San Pedro:
The recent need to fix both gnupg (delete & use python-gnupg) and shpaml (delete & use django-shpaml) highlights the need for requirements migrations:

After today,

- Whenever a change in requirements is indicated, produce a script which will move us forward to point B :)

- This is in addition to the change to the requirements.txt file itself, which does NOT do uninstalls of non-present items, nor is there an optiojn to do so.

- In the future, a salt state .sls file (with appropriate package: absent states) will help this.

Need to develop and test a masterless standalone Salt .sls here, that perhaps can integrate with a remote master - #36

Also add Git metadata plugin - #37


JJW 10/19/14:

A Docker conainer can now used for deployment.
See the eracks11/docker/ subdir and the master saltstack config for further details.

The etc/ subdir here is to be symlimked into the corresponding /etc locations:

- etc/nginx/eracks into /etc/nginx/sites-available/
- /etc/nginx/sites-available/eracks into /etc/nginx/sites-enabled/

- etc/supervisor/conf.d (which will include the contents) onto /etc/supervisor/conf.d

this will include gunicorn, sshd, nginx, etc

todo: cron and syslog?


JJW 7/5/14 nginx & gunicorn now used as of October 2013:

This directory contains the nginx & gunicon configurations for eRacks production - eracks10+


To use:

for nginx:

 - symlink the nginx config file 'eracks' into /etc/nginx/sites-available/
 - symlink /etc/nginx/sites-available/eracks into /etc/nginx/sites-enabled/


for gunicorn:

 - symlink the /upstart/eracks.conf file into /etc/init/



