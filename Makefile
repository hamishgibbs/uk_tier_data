# Search for .env file variables
ifneq (,$(wildcard ./.env))
    include .env
    export
endif

#Build a new docker image
build:
	docker build -t tier .

#Run image bash
bash:
	docker run -it --rm --mount type=bind,source="${PWD}",target=/usr/tier/ tier bash

scrape:
	docker run --rm --mount type=bind,source="${PWD}",target=/usr/tier/ tier python main.py
