#!/bin/bash

ROAMIUM_DIRECTORY=/home/george/roamium

scp -i /tmp/deploy_rsa docker-compose.yml george@roamium.software:$ROAMIUM_DIRECTORY
scp -i /tmp/deploy_rsa env/production.env george@roamium.software:$ROAMIUM_DIRECTORY/.env
scp -i /tmp/deploy_rsa nginx/production.conf george@roamium.software:$ROAMIUM_DIRECTORY/nginx.conf
scp -i /tmp/deploy_rsa scripts/init-letsencrypt.sh george@roamium.software:$ROAMIUM_DIRECTORY
ssh -i /tmp/deploy_rsa george@roamium.software "echo $CR_PAT | docker login ghcr.io -u $DOCKER_USERNAME --password-stdin"
ssh -i /tmp/deploy_rsa george@roamium.software "cd $ROAMIUM_DIRECTORY && \
    docker compose down && \
    docker compose pull && \
    export POSTGRES_PASS=$(openssl rand -base64 32) && \
    export SECRET_KEY=$(openssl rand -base64 32) && \
    export ORS_API_KEY=$ORS_API_KEY && \
    chmod +x init-letsencrypt.sh && \
    ./init-letsencrypt.sh && \
    rm init-letsencrypt.sh && \
    docker compose up -d"
ssh -i /tmp/deploy_rsa george@roamium.software docker logout ghcr.io
