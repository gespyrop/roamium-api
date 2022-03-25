#!/bin/sh

scp -i /tmp/deploy_rsa ../docker-compose.yml george@roamium.software:
ssh -i /tmp/deploy_rsa george@roamium.software docker-compose down && docker-compose pull && docker-compose up -d
