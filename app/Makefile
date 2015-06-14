install:
	virtualenv venv
	venv/bin/python setup.py install
	venv/bin/python manage.py syncdb --noinput

test:
	rm -rf .tox
	detox

clean:
	rm -rf venv

run:
	venv/bin/python manage.py runserver_plus 0.0.0.0:45000

rename:
	find . -maxdepth 1 -type f \( ! -iname "Makefile" \) -print0 | xargs -0 sed -i 's/planadversity/$(name)/g'
	find planadversity -maxdepth 1 -type f -print0 | xargs -0 sed -i 's/planadversity/$(name)/g'
	mv planadversity/manage_planadversity.py planadversity/manage_$(name).py
	mv planadversity $(name)
	echo "Great, you're all set! Well, you'll probably want to adjust the setup file by hand a bit."
