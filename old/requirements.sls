# 8/29/15 Saltified prerequisites for requirements.txt - JJW

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


## Ensure virtualenv present, other dependent packages, install my virtualenv & requirements

my-packages:
  pkg:
    - installed
    - names:
      - python-virtualenv
      - python-pip
      - git
      - mercurial
      - python-dev
      - libxml2-dev
      - libxslt-dev
      - zlib1g-dev
      - libjpeg-dev  # for Pillow
      - postgresql
      - postgresql-contrib
      #- python-psycopg2  # this is outside the venv, so need to turn on system_site_packages - moved to pip 9/8/16 JJW
      # for stylus, bower, (and possibly coffeescript)
      - npm  
      # for selenium testing:
      - chromium-chromedriver
      - xvfb
      #- firefox
      # could set up with Salt:  #- chrome
      # for (pip) weasyprint:
      - libffi-dev
      - libcairo2
      - libpango1.0-0
      - libgdk-pixbuf2.0-0
      - shared-mime-info
      # for (pip) psycopg2:
      - libpq-dev


#pip-upgrade:
#  cmd.run:
#    - name: pip install setuptools --upgrade
    #-unless: ??! there is no 'setuptools' in pip freeze
#    - require:
#      - pkg: my-packages

{{ cwd }}/env:
  virtualenv.managed:
    - cwd: {{ cwd }}
    - user: {{ me }}
    - system_site_packages: False
    #- system_site_packages: True
    #- requirements: requirements.txt
    # salt://REQUIREMENTS.txt
    - pip_pkgs: setuptools>=26.0
    #- pip_upgrade: True
    - no_chown: True
    - require:
      - pkg: django-haystack-pkg-removed
      #- cmd: pip-upgrade
      - pkg: my-packages


requirements:
  pip.installed:
    - cwd: {{ cwd }}
    - user: {{ me }}
    - bin_env: {{ cwd }}/env
    - requirements: requirements.txt
    - no_chown: True
    #- activate: True
    - require:
      - virtualenv: {{ cwd }}/env


#requirements:
#  cmd.run:
#    - cwd: {{ cwd }}
#    - user: {{ me }}
#    - name: |
#        env/bin/activate
#        pip freeze
#        pip install -r requirements.txt
#    - require:
#      - virtualenv: {{ cwd }}/env

## Djide permissions

{{ cwd }}/env/src/django-ide/djide/metafiles:
  file.directory:
    - user: {{ me }}
    - mode: 0777
    - require:
      - virtualenv: {{ cwd }}/env
      #- cmd: requirements


## Node.js symlink for Ubuntu

/usr/local/bin/node:
  file.symlink:
    - target: /usr/bin/nodejs


## Stylus

stylus:
  npm.installed:
    - require:
      - pkg: my-packages
      - file: /usr/local/bin/node


## Bower

bower:
  npm.installed:
    - require:
      - pkg: my-packages
      - file: /usr/local/bin/node

magnific-popup:
  bower.installed:
    - dir: {{ cwd }}
    - require:
      - npm: bower

# The remainder of the packages are all now in requirements.txt


## post-install setup - really only needs to be run the 1st time:

compilethemes:
  cmd.run:
    - cwd: {{ project }}
    - name: |
        . conf/env/bin/activate
        ./manage.py compilethemes
    - require:
      - virtualenv: {{ cwd }}/env

collectstatic:
  cmd.run:
    - cwd: {{ project }}
    - name: |
        . conf/env/bin/activate
        ./manage.py collectstatic --link --noinput -v0
    - require:
      - virtualenv: {{ cwd }}/env


# this one doesn't run in wercker, no postgres (no port 5432)

update_index:
  cmd.run:
    - cwd: {{ project }}
    - name: |
        . conf/env/bin/activate
        ./manage.py update_index
    - onlyif: netstat -antp |grep 5432
    - require:
      - virtualenv: {{ cwd }}/env


