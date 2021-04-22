#!/bin/sh

until nc -z $POSTGRES_HOST $POSTGRES_PORT; do
        echo 'Waiting for DB...'
        sleep 1
done

python manage.py migrate
python manage.py collectstatic --no-input

exec "$@"