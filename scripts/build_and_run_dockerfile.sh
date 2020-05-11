#!/bin/bash

docker stop $(docker ps -a -q --filter name=rpi_server_app)
docker rm $(docker ps -a -q --filter name=rpi_server_app)
docker image rm $(docker images -q --filter reference=rpi_server_app)

cd ..

docker build -t rpi_server_app .
docker run -d -p 5000:5000 --name=rpi_server_app --restart always -it rpi_server_app
