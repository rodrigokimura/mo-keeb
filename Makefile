.PHONY: build

# run app
run:
	@pipenv run app

# package app in one executable file
build:
	@pipenv run build

lint:
	@pipenv run black .
	@pipenv run isort .
