.PHONY: build

# run app
run:
	@pipenv run app

# package app in one executable file
build:
	@pipenv run build

# remove bundled package
clean:
	@pipenv run clean

lint:
	@pipenv run black .
	@pipenv run isort .
