install:
	virtualenv venv
	venv/bin/python setup.py install
	venv/bin/python manage.py syncdb --noinput

install-deps:
	sudo apt-get install build-essential python-setuptools python-pip redis-server libpython-dev
	homebrew install libpython

test:
	rm -rf .tox
	detox

clean:
	rm -rf venv

run:
	venv/bin/python manage.py runserver_plus 0.0.0.0:45000
