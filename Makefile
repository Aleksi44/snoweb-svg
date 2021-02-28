start:
	python manage.py runserver 0.0.0.0:4243

shell:
	python manage.py shell

mm:
	python manage.py migrate

superuser:
	python manage.py createsuperuser

loc:
	python manage.py makemessages --ignore build -l en -l fr -l de && python manage.py compilemessages

deploy:
	rm -rf dist/*
	yarn build
	python setup.py sdist bdist_wheel
	python -m twine upload dist/*

patch:
	npm version patch
	git push --tags origin master

test:
	python manage.py test -v 2

svg_build:
	python manage.py svg_build

rm_db:
	rm -f db.sqlite3

coverage:
	coverage run --source='.' manage.py test
	coverage report -m

fresh: rm_db mm test svg_build coverage
