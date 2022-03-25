#!/bin/sh

scp -i /tmp/deploy_rsa docker-compose.yml george@roamium.software:
ssh -i /tmp/deploy_rsa george@roamium.software "echo $CR_PAT | docker login ghcr.io -u $DOCKER_USERNAME --password-stdin"
ssh -i /tmp/deploy_rsa george@roamium.software docker-compose down && docker-compose pull && docker-compose up -d
ssh -i /tmp/deploy_rsa george@roamium.software docker logout ghcr.io
