all: fmt lint

fmt:
	black uds/*.py

lint:
	flake8 --ignore E501 uds/
