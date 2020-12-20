start:
	python manage.py runserver 0.0.0.0:4243

shell:
	python manage.py shell

mm:
	python manage.py migrate

superuser:
	python manage.py createsuperuser

deploy:
	rm -rf dist/*
	yarn build
	python setup.py sdist bdist_wheel
	python -m twine upload dist/*

patch:
	npm version patch
	git push --tags origin master
