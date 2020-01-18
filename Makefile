clean:
	find . -type f -name '*.pyc' -delete
	find . -type f -name '*.log' -delete

db_init:
	.venv/bin/python manage.py db init

db_migrate:
	cd user && ../.venv/bin/python manage.py db migrate --message 'initial database migration'

db_upgrade:
	cd user && ../.venv/bin/python manage.py db upgrade

celery-worker-up:
	watchmedo auto-restart --directory . --pattern '*.py' --recursive -- celery worker -A app.main.worker.tasks

up-production:
	docker-compose -f docker-compose.yml -f docker-compose.production.yml up -d

up-staging:
	docker-compose -f docker-compose.yml -f docker-compose.staging.yml up -d

up-development:
	docker-compose -f docker-compose.yml -f docker-compose.development.yml up -d

pgbouncer-chown:
	sudo chown -R postgres:postgres pgbouncer/log