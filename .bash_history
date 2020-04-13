ls
sudo apt-get update
sudo apt-get install     apt-transport-https     ca-certificates     curl     gnupg-agent     software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo apt-key fingerprint 0EBFCD88
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io
apt-cache madison docker-ce
sudo apt-get install docker-ce=5:19.03.7~3-0~ubuntu-bionic docker-ce-cli=5:19.03.7~3-0~ubuntu-bionic containerd.io
sudo docker run hello-world
sudo docker-compose up
sudo curl -L https://github.com/docker/compose/releases/download/1.18.0/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
docker-compose --version
sudo docker-compose up
nano Dockerfile
nano docker-compose.yml
ls
mkdir USERS
mv Dockerfile USERS/
ls
mv user.py USERS/
ls
nano docker-compose.yml
sudo docker-compose up
sudo docker-compose down
cd USERS
ls
nano Dockerfile
cd ..
sudo docker-compose up 
sudo docker-compose down
sudo docker-compose up
sudo docker-compose down
sudo docker-compose up
ls
cd USERS/
sudo docker image build -t users .
cd ..
sudo docker-compose up
