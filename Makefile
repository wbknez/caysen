# Makefile for Caysen.

init:
	pip install -r requirements.txt --user

run:
	@ python3 -m caysen.main

test:
	nose2 tests