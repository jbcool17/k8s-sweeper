venv:
	python3 -m venv .env

activate:
	. .env/bin/activate && exec bash

install:
	pip install .

docker-build:
	docker build -t test .

docker-test:
	docker build -t test -f Dockerfile.test . --no-cache && docker run -it --rm test
