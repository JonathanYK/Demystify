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



# lastly, add a schedule using crontab:
# $crontab -e
# Add there the following command (for each day at 00:15):
# 15 0 * * * /home/ubuntu/src/reclone_project_and_docker_compose.sh >> /home/ubuntu/cron.log 2>&1

# or this one for each 5 minutes (for debug):
# 0,5,10,15,20,25,30,35,40,45,50,55 * * * * /home/ubuntu/src/reclone_project_and_docker_compose.sh >> /home/ubuntu/cron.log 2>&1
