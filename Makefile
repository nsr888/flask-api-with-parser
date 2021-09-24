.PHONY: clean build run stop inspect testapp testcommon

IMAGE_NAME = alpine-python3-flask-chromedriver
CONTAINER_NAME = flask-ok-friends-api

build:
	docker build -t $(IMAGE_NAME) .

run:
	docker run --env-file .env --rm -p 8080:8080 --name $(CONTAINER_NAME) $(IMAGE_NAME)

inspect:
	docker inspect $(CONTAINER_NAME)

shell:
	docker exec -it $(CONTAINER_NAME) /bin/sh

stop:
	docker stop $(CONTAINER_NAME)

testapp:
	docker run --entrypoint "python" --env-file .env --rm -p 8080:8080 --name $(CONTAINER_NAME) $(IMAGE_NAME) -m tests.testapp

testcommon:
	docker run --entrypoint "python" --env-file .env --rm -p 8080:8080 --name $(CONTAINER_NAME) $(IMAGE_NAME) -m tests.testcommon
	
clean:
	docker ps -a | grep '$(CONTAINER_NAME)' | awk '{print $$1}' | xargs docker rm \
	docker images | grep '$(IMAGE_NAME)' | awk '{print $$3}' | xargs docker rmi
