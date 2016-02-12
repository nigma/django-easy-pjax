.PHONY: flake8 test coverage

flake8:
	flake8

example:
	python demo.py

test:
	which python
	python --version
	which django-admin.py
	python -c 'import django; print("Django version: " + django.get_version())'
	PYTHONPATH=. DJANGO_SETTINGS_MODULE=tests.settings \
		django-admin.py test -v 2 tests

coverage:
	coverage erase
	coverage run --branch --source=easy_pjax python run_tests.py
	coverage html
