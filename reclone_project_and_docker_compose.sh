# This shell file should be placed in /home/ubuntu/src in order to restart the docker compose (reclone the project and pull docker image).

echo "------------------"
date -u
echo "------------------"

echo "entring main path"
cd /home/ubuntu

echo "compose down"
sudo docker-compose -f ~/Sessions_Project/src/docker-compose.yml down

echo "removing old clone"
rm -rf Sessions_Project/

echo "cloning ssh from JonathanYK/Sessions_Project.git"
git clone git@github.com:JonathanYK/Sessions_Project.git

echo "entering cloned project"
cd ./Sessions_Project/src

echo "compose up"
sudo docker-compose up -d
