install:
	poetry install

build:
	rm -rf ./dist && poetry build

publish:
	rm -rf ./dist && poetry publish --build