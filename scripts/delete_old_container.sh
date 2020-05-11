#!/bin/bash

# Remove old container
echo -e "\e[32m----- Stop old container -----"
sudo docker stop $(sudo docker ps --filter name=rpi_server_app --filter name=rpi_server_db --filter name=rpi_server_phpmyadmin -q)

echo -e "\e[32m----- Remove old container -----"
sudo docker rm $(sudo docker ps -a --filter name=rpi_server_app --filter name=rpi_server_db --filter name=rpi_server_phpmyadmin -q)

echo -e "\e[32m----- Remove old volumes -----"
sudo docker volume rm $(sudo docker volume ls --filter name=new-rpi-server_mariadb)

echo -e "\e[32m----- Remove old network -----"
sudo docker network rm $(sudo docker network ls --filter name=new-rpi-server_default)
