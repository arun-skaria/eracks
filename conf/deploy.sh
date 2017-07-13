#!/bin/bash

if [ "$1" == "" ]
then

echo
echo "Usage: $0 <dev | staging | prod>"
echo
echo "Be sure to run $0 as the user you want the venv installed as, from the conf/ subdir!"
echo "(It will ask for your pw if you are set up that way for sudo)"
echo

else

echo $1

me=`id -un`
cwd=`pwd`
if [ `id -u` -ne '0' ]; then sudo=sudo; fi

echo Running base first, then $0 for $1 as $me in $cwd
echo $sudo env me=$me cwd=$cwd salt-call -l debug --local state.template $1.sls
echo FIRST BASE
$sudo env me=$me cwd=$cwd salt-call -l debug --local state.template base.sls
echo NOW $1
# This one could be in jjw-salt-master, and called directly from there locally, since we have the repo
$sudo env as=$1 me=$me cwd=$cwd salt-call -l debug --local state.template $1.sls
echo DONE

# Nope! Salt sucks - apparently salt-call can't do includes without an 'environment' (saltenv), which implies a topfile
#$sudo env me=$me cwd=$cwd salt-call -l debug --local -c . -m . --file-root=. --pillar-root=. --metadata state.template $1.sls
#$sudo env me=$me cwd=$cwd salt-call -l debug --local --metadata state.template $1.sls

# also tried state.apply, etc
# could probably wrok something out with state.sls_id, and get all the requisites right..

# Let's migrate to Ansible!  at least for these standalone brewpub-3-style idems

fi
