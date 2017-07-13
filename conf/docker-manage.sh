# can be run from any dir - due to pathing based on filename -  uncomment for illustration:

#echo $0
#echo realpath $0
#echo $(dirname $(realpath $0))
#echo $(dirname $(dirname $(realpath $0)))
#exit

projectdir=$(dirname $(dirname $(readlink -f $0)))
sudo docker run -itv $projectdir:$projectdir --net host \
    -e DOCKER=1 \
    -e CIRCLECI=$CIRCLECI \
    eracks11 \
    -c "cd $projectdir && echo ./manage.py $* && ./manage.py $*"

#    -e WERCKER=$WERCKER \
#    -e SELENIUM=$SELENIUM \
