# Nope! no includes - see notes in deploy.sh
#
#include:
#  - base

# NOTE: ONLY WORKS FOR USER JOE FOR NOW

{% set as       = salt['environ.get']('as') %}
{% set cwd      = salt['environ.get']('cwd') %}
{% set me       = salt['environ.get']('me') %}
{% set project  = salt['file.dirname'](cwd) %}


nginx-repo:
  pkgrepo.managed:
    - humanname: nginx stable for ubuntu 14.04
    - ppa: nginx/stable
    # This works, but doesn't have debianized config - so use PPA, above
    #- name: deb http://nginx.org/packages/ubuntu/ trusty nginx
    ##- dist: stable
    #- file: /etc/apt/sources.list.d/nginx-stable.list
    ##- gpgcheck: 1
    #- key_url: http://nginx.org/keys/nginx_signing.key
    - require_in:
      - pkg: nginx
  pkg.installed:
    - name: nginx

prod-packages:
  pkg.installed:
    - names:
      - memcached
      - gnupg
    #- logging? backups?
    #- require:
    #  - cmd: my-packages

#service
#etc


## Users & packages

{{ as }}:
  user.present:
    - fullname: eRacks {{ as }} User
    - gid_from_name: True
    - optional_groups:
      - ssh
      - www-data
  # - name: dev
  # - home: /home/dev
    - shell: /bin/bash
    # zsh?

sudoers-{{ as }}:
  file.managed:
    - name: /etc/sudoers.d/sudoers-{{ as }}
    - contents: "{{ as }} ALL=(ALL)NOPASSWD: ALL"
    - makedirs: True
    - replace: False
    - user: root
    - group: root
    - mode: 644

sshkeys:
  ssh_auth:
    - present
    - user: {{ as }}
    - enc: ssh-rsa
    - comment: Keys for {{ as }}
    - names:
      - ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC+xUBBvQ7+5WiKLSsBUrIbqyecadH+FFSJzrvA43hxM+z1LP5G0CnMHFVIYF68b58rzPvWurYshCRwOf6Z0ZOc0IAqyOxRQeIG6hphT5TfL+gB+h/BJ+YaWxNR0s7EJYr/2hWUP0j1xJ6EFt1EUH9p5vi4tRo1NcX7syxQUmedtkLrOgM7p5wAbcNGkjog8SmMyHyMZD5yQPt7kbkz2qUmZzf2CNR4aUZEoJnvyLoXDrz1OxZPklcjeXVUH7w91WKPIrTm+lt4xOn0XuCqmHzIlNixyHTBOrdoDuRbejhn/UOFswb3YFRMLczK6f3N+UqqpV9PAErK9QGOAyEjLRHZ root@mintstudio-maya
      - ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEA3LLGEPMDbN91Ia5ue9dgXc0tvAMNxhbhSPatVTkdVxjdUPEXlyi763G5IKg5amp+UwUuXm+PRCgoXCY5qVdhgIIlE2QhNN6WhMXP1WO0nYHAeUuFuZVhj8f/MAtweMTQcvst6xO0Q1ned4e1/C1Vxgk3K4DNkjvmmZKCVLhQq3yVugURMKoRaUbylcTSd644sv4s0uHCvgwoqeo1mbs6B78tt8l9NgcRMCqHbS6Fr9FeOPOBh2AM74M4GbOTmDNsPlIKTU1QbuUWTtZhl+PyJ9s7f7YCARczz2T1zqeW9TX+g6LUcvliDcXvAPctpLQtDR0saFlrvv43ZLGnp0JO2Q== root@ubuntustudio
      - ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEAvYqSpJvAKMqxSa9Mzhdw7pFk/UOzEOith8UolvC5HpeRieZFwPdXeEDbsVSXlzQqy0v1i226W8+CPX9JX82VWI2RZIkB3sJq3AEELO3pDbDe/Uc1WsTzbN6QUBlpl2OvZB0bBvkGbbATUU2xXefDV/g3ma4k1HkiQIAB6Ymw6XM8+5iznhx8ERsUUE9V9NGc52ujAr4Sz5E+wgLxZXWKW25IiPfAMOHvlEzfiL4S3Q8YruSy337C54ttf8VFwBHcotzybhOIUEqCqsAc70RLlhNpafNLx/sJD/yJ+R3AO0z6Brm8eVeax56gSs4eIdY23tufX2drL8ZnY1LNNhdV9w== joe@STUDIO

## github setup for "as" user

github.com:
  ssh_known_hosts:
    - present
    - user: {{ as }}
    #- enc: ecdsa
    - fingerprint: ad:1c:08:a4:40:e3:6f:9c:f5:66:26:5d:4b:33:5d:8c
    # (DSA)
    - fingerprint: 16:27:ac:a5:76:28:2d:36:63:1b:56:4d:eb:df:a6:48
    # (RSA)

# ... more stuff fm eracks dev left out - should move to a salt-master based eracksuser sls, either a loop or call on a per-user basis


## symlinks for nginx conf, upstart, etc

/etc/nginx/sites-available/eracks-{{ as }}:
  file.symlink:
    - target: {{ cwd }}/etc/nginx/eracks-{{ as }}

/etc/nginx/sites-enabled/eracks-{{ as }}:
  file.symlink:
    - target: /etc/nginx/sites-available/eracks-{{ as }}

/etc/nginx/sites-enabled/default:
  file.absent: []

# Nope! symlinks ignored by upstart.  Use hard link.
#/etc/init/eracks.conf:
#  file.symlink:
#    - target: {{ cwd }}/etc/upstart/{{ as }}/eracks.conf

gunicorn-init:
  cmd.run:
    - name: |
        ln {{ cwd }}/etc/upstart/{{ as }}/eracks.conf /etc/init/eracks.conf && \
        initctl reload-configuration && \
        service eracks start


## ssl certs - need for prod, at least, and staging, if not dev

/etc/ssl/eracks/eracks.crt:
  file.symlink:
    - target: /etc/ssl/certs/ssl-cert-snakeoil.pem
    - makedirs: True

/etc/ssl/eracks/eracks.key:
  file.symlink:
    - target: /etc/ssl/private/ssl-cert-snakeoil.key
    - makedirs: True


## Restart nginx after settling in, kluge to avoid annoying salt requires crap (could also just reboot).

ngingx-restart:
  cmd.run:
    - name: sleep 5 && service nginx restart
