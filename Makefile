# Basic Makefile for Mappy

default:
	@source env/bin/activate; python mappy.py
	
test:
	@source env/bin/activate; python tests.py

env:
	@virtualenv env
