install:
	(cd ./cluedin && poetry install)

build:
	(cd ./cluedin && poetry build)

publish:
	(cd ./cluedin && poetry publish --build --username __token__ --password ${PYPI_TOKEN})