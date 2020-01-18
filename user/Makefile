clean:
	find . -type f -name '*.pyc' -delete
	find . -type f -name '*.log' -delete

tests:
	python manage.py test

install:
	pip install -r requirements.txt

run:
	python manage.py run

run-gunicorn:
	gunicorn wsgi:app --reload --workers=1 -b :5000

all: clean install tests db_upgrade run


db_init:
	python manage.py db init

db_migrate:
	python manage.py db migrate --message 'initial database migration'

db_upgrade:
	python manage.py db upgrade

celery-worker-up:
	watchmedo auto-restart --directory . --pattern '*.py' --recursive -- celery worker -A app.main.worker.tasks

APP_NAME=flask-restplus-boilerplate

heroku-run:
	source ../.venv/bin/active && heroku local

heroku-app-create:
	heroku apps:create ${APP_NAME} --buildpack heroku/python

heroku-undeploy:
	heroku addons:destroy heroku-postgresql
	heroku apps:destroy -a ${APP_NAME}
	heroku apps

heroku-app-add:
	heroku git:remote -a ${APP_NAME}

heroku-shell:
	heroku ps:exec

heroku-deploy:
	git add -f log/.gitkeep
	git add .
	git commit -m "."
	git push heroku master
	heroku ps:scale web=1
	curl -X GET -i "https://flask-restplus-boilerplate.herokuapp.com/api/v1/user/publish"


heroku-buildpack:
	heroku buildpacks:set heroku/python

heroku-db-add:
	heroku addons:create heroku-postgresql:hobby-dev -a ${APP_NAME}
	
heroku-db-upgrade:
	heroku run python manage.py db upgrade -a ${APP_NAME}

heroku-logs:
	heroku logs -t