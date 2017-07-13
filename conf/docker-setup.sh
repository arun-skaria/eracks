# Should be run from conf/ subdir

# Must not already have containers present - run docker-init first

# Set project dir
projectdir=$(dirname $(dirname $(readlink -f $0)))

# Set up db container for eracks-postgres, which eracks11 will connect to (this can fail on repeated runs if it's already up)
sudo docker run --name eracks-postgres -e POSTGRES_USER=eracks -e POSTGRES_DB=eracksdb -e POSTGRES_PASSWORD=Wav3lets9 -d --net=host postgres

# Run initial setup scripts - static files, compile themes, collect static, setup db, setup search
sudo docker run -itv $projectdir:$projectdir --net host eracks11 -c "cd $projectdir && conf/setup-envo.sh"  && \
sudo docker run -itv $projectdir:$projectdir --net host eracks11 -c "cd $projectdir && conf/setup-db.sh"    && \
sudo docker run -itv $projectdir:$projectdir --net host eracks11 -c "cd $projectdir && conf/setup-search.sh"

echo SETUP DONE