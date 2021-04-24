FROM python:3.10.0a7-alpine3.13
LABEL author="George Spyropoulos"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN apk add --update --no-cache postgresql-client
RUN apk add --update --no-cache --virtual .tmp-build-deps gcc libc-dev linux-headers postgresql-dev
RUN pip install -r requirements.txt
RUN apk del .tmp-build-deps

RUN mkdir -p /roamium/static
WORKDIR /roamium
COPY ./roamium /roamium

RUN chmod +x /roamium/entrypoint.sh

RUN adduser -D user
RUN chown -R user:user /roamium
USER user

ENTRYPOINT ["/roamium/entrypoint.sh"]
