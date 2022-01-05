FROM python:3.9-slim-buster
LABEL author="George Spyropoulos"

ENV PYTHONUNBUFFERED=1

RUN apt update && apt -y upgrade
RUN apt install -y gcc libpq-dev netcat binutils libproj-dev gdal-bin python-gdal python3-gdal

COPY ./requirements.txt /requirements.txt
RUN pip install -r requirements.txt

RUN mkdir -p /roamium/static
WORKDIR /roamium
COPY ./roamium /roamium

RUN chmod +x /roamium/entrypoint.sh

RUN useradd user
RUN chown -R user:user /roamium
USER user

ENTRYPOINT ["/roamium/entrypoint.sh"]
