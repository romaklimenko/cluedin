install:
	(cd ./cluedin && poetry install)

build:
	(cd ./cluedin && rm -rf ./dist && poetry build)

publish:
	(cd ./cluedin && rm -rf ./dist && poetry publish --build --username __token__ --password ${PYPI_TOKEN})