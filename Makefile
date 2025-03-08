install:
	poetry install

test:
	poetry run pytest

build:
	rm -rf ./dist && poetry build

publish:
	rm -rf ./dist && poetry publish --build