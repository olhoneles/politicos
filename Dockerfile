FROM python:3.7

RUN	apt-get update && \
	apt-get -y install libcurl4-openssl-dev build-essential libssl-dev

RUN mkdir -p /usr/share/politicos-api
WORKDIR /usr/share/politicos-api

COPY . /usr/share/politicos-api
RUN pip install --no-cache-dir -r /usr/share/politicos-api/requirements.txt
