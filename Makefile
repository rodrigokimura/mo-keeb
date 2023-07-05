.PHONY: build

# run app
run:
	# @rm config.toml -f
	@pipenv run app

# package app in one executable file
build:
	@pipenv run build

version:
	@pipenv run version

lint:
	@pipenv run black .
	@pipenv run isort .

test:
	@pipenv run pytest . -s
