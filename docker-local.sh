#!/bin/bash

docker network create local_network

docker pull mongo:5.0.22
docker run -dp 27017:27017 --name mongo_local --network local_network mongo:5.0.22

docker build --platform linux/arm64/v8 -f Dockerfile -t restaurants .
docker run -dp 8080:80 -w /app -v "$(pwd):/app" --name restaurants-app --network local_network restaurants