all: test mypy black

.PHONY: test
test:
	pytest

.PHONY: mypy
mypy:
	mypy src

.PHONY: black
black:
	black src setup.py
