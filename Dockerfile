FROM python:3.10.0a7-alpine3.13
LABEL author="George Spyropoulos"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN pip install -r requirements.txt

RUN mkdir /roamium
WORKDIR /roamium
COPY ./roamium /roamium

RUN python manage.py migrate

RUN adduser -D user
USER user

