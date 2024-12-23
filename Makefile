.PHONY: install test lint clean build publish

install:
	pip install -e ".[dev]"

test:
	pytest

lint:
	flake8 src/hfpics
	mypy src/hfpics
	black --check src/hfpics
	isort --check-only src/hfpics

format:
	black src/hfpics
	isort src/hfpics

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name .pytest_cache -exec rm -rf {} +
	find . -type d -name .mypy_cache -exec rm -rf {} +

build: clean
	python -m build

publish: build
	twine upload dist/* 