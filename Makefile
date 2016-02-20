.PHONY: flake8 demo test coverage dist publish

flake8:
	flake8

demo:
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
	PYTHONPATH=. DJANGO_SETTINGS_MODULE=tests.settings coverage run --source=easy_pjax \
		`which django-admin` test tests
	coverage report -m
	coverage html

dist:
	python setup.py sdist bdist_wheel

publish:
	python setup.py sdist bdist_wheel upload
	# You probably want to also tag the version now:
	#   git tag -a <version> -m 'version <version>'
	#   git push --tags
