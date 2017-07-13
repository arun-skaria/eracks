# Should be run from conf/ subdir

# Set up initial Docker envo
sudo docker build -t eracks11 .
sudo docker pull postgres

echo BUILD DONE