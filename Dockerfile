# pull official base image
FROM python:3.7-alpine



# set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# copy project

# install dependencies

RUN pip install --upgrade pip
RUN apk update
RUN apk add --no-cache \
        gcc \
        g++ \
        libxslt-dev\
        python-dev \ 
        python3-dev \
        libressl-dev \
        musl-dev \
        libffi-dev \
        postgresql-dev \
        libxml2-dev \
        libxslt-dev 

# set work directory
ADD requirements.txt /usr/src/app/
WORKDIR /usr/src/app
RUN pip install -r requirements.txt

COPY . /app
