run:
	@pipenv run python src/app.py

lint:
	@pipenv run black .
	@pipenv run isort .
