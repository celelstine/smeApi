activate:
	pipenv shell

start:
	python manage.py runserver

test:
	python manage.py test -v 2 ${APP}

migrate:
	python manage.py migrate

check_flake8:
	pip install flake8
	flake8

coverage:
	coverage erase
	coverage run manage.py test --verbosity 2
	coverage report --fail-under=70 --show-missing
	coverage html


ci_test:
	pipenv run flake8 .
	coverage erase
	coverage run manage.py test --verbosity 2
	coverage report --fail-under=70 --show-missing
	coverage html