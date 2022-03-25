#!/bin/sh

ROAMIUM_DIRECTORY=/home/george/roamium/

scp -i /tmp/deploy_rsa docker-compose.yml george@roamium.software:$ROAMIUM_DIRECTORY
scp -i /tmp/deploy_rsa env/production.env george@roamium.software:$ROAMIUM_DIRECTORY
ssh -i /tmp/deploy_rsa george@roamium.software "echo $CR_PAT | docker login ghcr.io -u $DOCKER_USERNAME --password-stdin"
ssh -i /tmp/deploy_rsa george@roamium.software cd $ROAMIUM_DIRECTORY && \
    export POSTGRES_PASS=$(openssl rand -base64 32) && \
    export SECRET_KEY=$(openssl rand -base64 32) && \
    docker-compose --env_file $ROAMIUM_DIRECTORY/env/production.env down && \
    docker-compose --env_file $ROAMIUM_DIRECTORY/env/production.env pull && \
    docker-compose --env_file $ROAMIUM_DIRECTORY/env/production.env up -d
ssh -i /tmp/deploy_rsa george@roamium.software docker logout ghcr.io
