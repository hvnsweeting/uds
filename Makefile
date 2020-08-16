all: fmt lint test

fmt:
	black uds/*.py

lint:
	flake8 --ignore E501 uds/

test:
	python -m doctest uds.py -v
