# Makefile for Caysen.

init:
	pip install -r requirements.txt --user

run:
	python3 caysen/main.py

test:
	nose2 tests