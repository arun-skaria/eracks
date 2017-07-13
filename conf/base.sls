# 8/29/15-9/24/16 Saltified deployment - JJW

## These first two are set in the command line in salt-requirements.sh:
{% set cwd      = salt['environ.get']('cwd') %}
{% set me       = salt['environ.get']('me') %}
{% set project  = salt['file.dirname'](cwd) %}


## Clean up possible leftover cruft, ensure certain packages not present:

django-haystack-pkg-removed:
  pkg.removed:
    - name: django-haystack

# can't have two of the same ID, can't have two xxx.removed states.  Yuk.
#django-haystack-pip-removed:
#  pip.removed:
#    - name: django-haystack

# really need ensure_removed, or ensure_python_removed - start with pkg, then pip, then manual..
#django-haystack.egg:
  #file: absent

# commenting out, not idemoptent - returns False if already not present
#gnupg:
#  pip.removed
#
#django-admin-tools:
#  pip.removed


## Call centralized install-packages script, also used by Vagrant/dev/docker/wercker/CI

my-packages:
  cmd.run:
    - name: bash {{ cwd }}/install-packages.sh
    - require:
      - pkg: django-haystack-pkg-removed


## For full deploy, ensure Postgres present in addition to usual packages & requirements

deploy-packages:
  pkg.installed:
    - names:
      - python-virtualenv
      - postgresql
      - postgresql-contrib
    - require:
      - cmd: my-packages


## Use virtualenv for pip packages, to isolate from OS

pip-packages:
  virtualenv.managed:
    - name: {{ cwd }}/env
    - system_site_packages: True  # necessary for psycopg2
  #pip.installed:
    - user: {{ me }}
    - requirements: {{ cwd }}/requirements.txt
    #- log: {{ cwd }}/pip.log
    - require:
      - pkg: deploy-packages


## Djide permissions

# TODO: git submodule
{{ cwd }}/env/src/django-ide/djide/metafiles:
#/usr/local/lib/python2.7/dist-packages/django-ide/djide/metafiles:
  file.directory:
    - makedirs: True
    - user: {{ me }}
    - mode: 0777
    - require:
      - virtualenv: pip-packages


## Node.js symlink for Ubuntu

/usr/local/bin/node:
  file.symlink:
    - target: /usr/bin/nodejs
    - require:
      - cmd: my-packages


## npm packages - Stylus & Bower - at some point we may want a local npm dir, like venv

npm-packages:
  npm.installed:
    - pkgs:
      - stylus
      - bower
    - require:
      - cmd: my-packages
      - file: /usr/local/bin/node


## bower packages

magnific-popup:
  bower.installed:
    - dir: {{ cwd }}
    - require:
      - npm: npm-packages
      #bower

# The remainder of the packages are all now in requirements.txt


## post-install setup - really only needs to be run the 1st time:

setup-envo:
  cmd.run:
    - cwd: {{ project }}
    - user: {{ me }}
    - name: bash -c "source conf/env/bin/activate && {{ cwd }}/setup-envo.sh"
    - require:
      - virtualenv: pip-packages

setup-db:
  cmd.run:
    - cwd: {{ project }}
    - user: {{ me }}
    - name: bash -c "source conf/env/bin/activate && {{ cwd }}/setup-db.sh"
    - require:
      - virtualenv: pip-packages

setup-search:
  cmd.run:
    - cwd: {{ project }}
    - user: {{ me }}
    - name: bash -c "source conf/env/bin/activate && {{ cwd }}/setup-search.sh"
    - require:
      - cmd: setup-db

#compilethemes:
#  cmd.run:
#    - cwd: {{ project }}
#    - name: |
#        source conf/env/bin/activate
#        env
#        pwd
#        id
#        ./manage.py compilethemes
#    - require:
#      - pip: pip-packages

#collectstatic:
#  cmd.run:
#    - cwd: {{ project }}
#    - name: |
#        source conf/env/bin/activate
#        ./manage.py collectstatic --link --noinput -v0
#    - require:
#      - pip: pip-packages


# this one doesn't run in wercker, no postgres (no port 5432)

#update_index:
#  cmd.run:
#    - cwd: {{ project }}
#    - name: |
#        source conf/env/bin/activate
#        ./manage.py update_index
#    - onlyif: netstat -antp |grep 5432
#    - require:
#      - pip: pip-packages


