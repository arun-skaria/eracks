# Should be run from conf/ subdir

# make sure no containers are running, dust database container - DESTRUCTIVE!

echo WARNING - THIS WILL DESTORY THE EXISTING DATABASE CONTAINER in 5 seconds - Ctrl-C to stop
sleep 5

sudo docker kill eracks11
sudo docker kill eracks-postgres
sudo docker rm eracks-postgres

echo INIT DONE