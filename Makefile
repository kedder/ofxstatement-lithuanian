all: test mypy

.PHONY: test
test:
	pytest

.PHONY: mypy
mypy:
	mypy src
