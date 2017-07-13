#!/usr/bin/env python
# -*- coding: utf-8 -*-


# Exclude a certain pk from Yaml file
#
# Usage: ./exclude_pk.py fixture.yaml model pk-to-remove


import sys, yaml
from collections import OrderedDict
from pprint import pprint


dicts = yaml.load (open (sys.argv [1]))

#print dicts

for d in dicts:
  #if d ['model'] == sys.argv [2]:
  #  print d ['pk'], sys.argv [3]

  if d ['model'] == sys.argv [2] and int (d ['pk']) == int (sys.argv [3]):
    dicts.remove (d)
    print >>sys.stderr, 'Removed:', d

print yaml.dump (dicts)  # , indent=4)
