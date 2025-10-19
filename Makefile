venv:
	python3 -m venv .env

activate:
	. .env/bin/activate && exec bash

install:
	pip install .

docker-build:
	docker build -t test .

docker-test-build:
	docker build -t test -f Dockerfile.test .

docker-test-run: docker-test-build
	docker run -it --rm test

docker-test-env: docker-test-build
	docker run -it --rm --entrypoint=bash test 
