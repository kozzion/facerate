# facerate
a facial beauty rating web service

# TODO replace:
# IP, 
# pem file
# start amazon instance
# connect to amazon instance:
ssh -i JaapOosterbroek_EC2_EUC1_2.pem ubuntu@35.158.141.122

# get repro and build docker
sudo apt-get update
sudo apt-get install docker.io
git clone https://github.com/kozzion/facerate.git
cd ~/facerate
sudo docker pull continuumio/anaconda3
sudo docker build -t facerate .
sudo docker run -p 80:80 -it facerate /bin/bash # interactive
sudo docker run -p 80:80 facerate




#inside container
--usefull docker commands

docker --version
sudo docker image ls
sudo docker container ls

sudo docker rm -f $(sudo docker ps -a -q)  Kill all dockers
sudo docker rmi -f $(sudo docker images -q) Remove all images
sudo docker container stop [d87d91196ed9]

sudo docker run -p 80:80 -it facerate

//Reload eviroment after installing anaconda
source ~/.bashrc  
//Top sorted by mem
top -o %MEM


-- for copying data
use winscp
killall5 -9
