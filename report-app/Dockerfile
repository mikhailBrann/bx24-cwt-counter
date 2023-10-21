FROM python:3.10-alpine
RUN apk add --no-cache bash

# copy project
COPY ./ ./report-app
# set work directory
WORKDIR ./report-app

RUN pip install --upgrade pip
RUN pip install -r ./requirements.txt
