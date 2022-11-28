path = src
files = `find $(path) -name '*.py'`

run:
	pipenv run python manage.py runserver

test:
	pipenv run python manage.py test --no-input --verbosity=2 --settings=src.app.settings.unittest

test_with_coverage:
	- pipenv run coverage erase
	- pipenv run coverage run manage.py test --no-input --verbosity=2 --settings=src.app.settings.unittest
	- pipenv run coverage report
	- pipenv run coverage xml
format:
	- pipenv run add-trailing-comma $(files)
	- pipenv run pyformat -i $(files)
	- pipenv run isort -rc $(path)

lint:
	pipenv run flake8 $(path)

commit_check:
	pipenv run cz check --rev-range origin/master..HEAD

make_migrations:
	pipenv run python manage.py makemigrations

migrate:
	pipenv run python manage.py migrate

show_migrations:
	pipenv run python manage.py showmigrations

collect_statics:
	pipenv run python manage.py collectstatic --noinput

SHELL=/bin/sh

validate:
	@echo "Validating cloudformation files";
	@ls aws/cloudformation/**/*.yml | xargs -t -I {} aws cloudformation validate-template --template-body file://{} > /dev/null