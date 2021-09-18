clean-db:
	rm db.sqlite3
	rm -R */*/*/migrations/*

setup-dev:
	python -m venv venv
	source venv/bin/activate
	pip install -r requirements/development.txt

setup-django:
	python manage.py makemigrations authorization
	python manage.py migrate

run:
	python manage.py runserver