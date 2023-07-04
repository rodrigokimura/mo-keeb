run:
	@pipenv run sudo python src/app.py

lint:
	@pipenv run black .
	@pipenv run isort .
