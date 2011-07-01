# Basic Makefile for Mappy
.PHONY: test

test:
	@source env/bin/activate; python tests.py
