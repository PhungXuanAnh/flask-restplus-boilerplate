FLASK RESTFUL API BOILER-PLATE WITH JWT

- [1. Deploy local or vm cloud](#1-deploy-local-or-vm-cloud)
  - [1.1. Install required packages](#11-install-required-packages)
  - [1.2. change Procfile](#12-change-procfile)
  - [1.3. change celery config](#13-change-celery-config)
  - [1.4. change database config](#14-change-database-config)
  - [1.5. Create database](#15-create-database)
  - [1.6. Boot up rabbitmq and start celery worker](#16-boot-up-rabbitmq-and-start-celery-worker)
  - [1.7. Run test](#17-run-test)
  - [1.8. Run app](#18-run-app)
  - [1.9. Run all command](#19-run-all-command)
- [2. Deploy heroku](#2-deploy-heroku)
  - [2.1. Create a git repo](#21-create-a-git-repo)
  - [2.2. login heroku accounts](#22-login-heroku-accounts)
  - [2.3. create or add heroku app](#23-create-or-add-heroku-app)
  - [2.4. change Procfile](#24-change-procfile)
  - [2.5. change celery config](#25-change-celery-config)
  - [2.6. change database config](#26-change-database-config)
    - [2.6.1. Using sqlite](#261-using-sqlite)
    - [2.6.2. using postgres](#262-using-postgres)
  - [2.7. deploy app](#27-deploy-app)
  - [2.8. Upgrade database](#28-upgrade-database)
- [3. Viewing api in swagger and trying test](#3-viewing-api-in-swagger-and-trying-test)
- [4. Test using curl](#4-test-using-curl)
  - [4.1. Test publish api](#41-test-publish-api)
  - [4.2. Logging of this user api](#42-logging-of-this-user-api)
  - [4.3. Guide about token for normal user and admin](#43-guide-about-token-for-normal-user-and-admin)
  - [4.4. Normal user](#44-normal-user)
  - [4.5. Admin user and celery task](#45-admin-user-and-celery-task)
- [5. Full description and guide](#5-full-description-and-guide)
- [6. Contributing](#6-contributing)
- [7. Response format message convention](#7-response-format-message-convention)

# 1. Deploy local or vm cloud
## 1.1. Install required packages

`pip install -r requirements.txt`

## 1.2. change Procfile

```ini
api: gunicorn wsgi:app --reload --threads 1 --workers=1 -b :5000
worker: watchmedo auto-restart --directory . --pattern '*.py' --recursive -- celery -A app.main.worker.tasks worker -c 1
```

## 1.3. change celery config

Change config in file [config.py](app/main/config.py) to:

```python

CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL

# OR

CELERY_BROKER_URL = RABBITMQ_URL
CELERY_RESULT_BACKEND = RABBITMQ_URL
```

## 1.4. change database config


Change config in file [config.py](app/main/config.py) to:

```python
class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, '../../flask_boilerplate_main.db')
    # ----------------- OR
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
```

NOTE: if you add more model to model folder, it must be import in method **create_app** in file [__init__.py](app/main/__init__.py)
    
## 1.5. Create database

By default, this sample app using sqlite, if you want to change to postgres:

```shell
docker-compose up -d postgres
docker-compose ps
```

Then run:

```shell
make db_migrate
make db_upgrade
```

## 1.6. Boot up rabbitmq and start celery worker

```shell
docker-compose up -d rabbitmq
docker-compose ps
```

## 1.7. Run test

**TODO:** run test is failed, fix this

`make tests`

## 1.8. Run app

`make run`

or 

`make run-gunicorn`

## 1.9. Run all command

`make all`

# 2. Deploy heroku

## 2.1. Create a git repo

```shell
cd flask-restplus-boilerplate/user
git init
```

## 2.2. login heroku accounts

```shell
heroku accounts     # list account
heroku accounts:current     # get current account
heroku accounts:add flask-restplus-boilerplate      # NOTE: get account from dropbox
heroku account:set flask-restplus-boilerplate
```

## 2.3. create or add heroku app

```shell
make heroku-app-create
# or
make heroku-add-app
```

## 2.4. change Procfile

```ini
web: gunicorn wsgi:app --log-file -
worker: celery worker -A app.main.worker.tasks
```

## 2.5. change celery config

Change file [config.py](app/main/config.py) to:

```python
# CELERY_BROKER_URL = RABBITMQ_URL
# CELERY_RESULT_BACKEND = RABBITMQ_URL

CELERY_BROKER_URL = 'memory://localhost/'
CELERY_RESULT_BACKEND = 'db+sqlite:///celery-task-results.sqlite'
```

## 2.6. change database config

### 2.6.1. Using sqlite

**NOTE:** sqlite just for testing, it will be remove if app is reseted

Change file [config.py](app/main/config.py) to:

```python
class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, '../../flask_boilerplate_main.db')
```

### 2.6.2. using postgres

see heroku postgres add-on

```shell
heroku addons
heroku config
heroku pg
```

if there is no postgres, add one:

```shell
make heroku-db-add
heroku config
heroku pg
```

Change file [config.py](app/main/config.py) to:

```python
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
```

## 2.7. deploy app

```shell
make heroku-deploy

make heroku-logs
```

## 2.8. Upgrade database

sqlite:

```shell
heroku ps:exec
# then
python manage.py db upgrade
```

postgres:

```shell
make heroku-db-upgrade
```

if error, then

```shell
# get DATABASE_URL:
heroku config
# then add it to app
heroku config:set DATABASE_URL=...
```

# 3. Viewing api in swagger and trying test 

http://127.0.0.1:5000/api/v1/

https://flask-restplus-boilerplate.herokuapp.com/api/v1/


# 4. Test using curl

## 4.1. Test publish api

```shell
curl -X GET -i "http://127.0.0.1:5000/api/v1/user/publish"
curl -X GET -i "https://flask-restplus-boilerplate.herokuapp.com/api/v1/user/publish"
```

## 4.2. Logging of this user api

See log message in folder log

## 4.3. Guide about token for normal user and admin

Authorization header is in the following format:

- Key: Authorization
- Value: "token_generated_during_login"

For testing authorization, url for getting all user requires an admin token while url for getting a single
user by public_id requires just a regular authentication.

## 4.4. Normal user

Create user:

```shell
URL=http://127.0.0.1:5000
# URL=https://flask-restplus-boilerplate.herokuapp.com
curl -X POST -i "${URL}/api/v1/user/" \
    -H "accept: application/json" \
    -H "Content-Type: application/json" \
    -d "{ \"email\": \"test@gmail.com\", \"username\": \"test\", \"password\": \"1234\"}"
# output
{
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1NzczNTc4NTgsImlhdCI6MTU3NzI3MTQ1Mywic3ViIjoxNH0.L2goXfgYTuIB8rpz5MZDyOkqhpyj_IjbNIIHZwYwhVM"
}

```

Login:

```shell
URL=http://127.0.0.1:5000
# URL=https://flask-restplus-boilerplate.herokuapp.com
curl -X POST -i "${URL}/api/v1/auth/login" \
    -H "accept: application/json" \
    -H "Content-Type: application/json" \
    -d "{ \"email\": \"test@gmail.com\", \"password\": \"1234\"}"
# output
{
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1NzczNTc4NTgsImlhdCI6MTU3NzI3MTQ1Mywic3ViIjoxNH0.L2goXfgYTuIB8rpz5MZDyOkqhpyj_IjbNIIHZwYwhVM"
}
```

Get user:

```shell
# URL=http://127.0.0.1:5000
URL=https://flask-restplus-boilerplate.herokuapp.com
curl -X GET -i "${URL}/api/v1/user/5f8abe86-83dc-47d7-a7ee-2808d35124d7" \
    -H "accept: application/json" \
    -H "Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1NzY2NjAyMjAsImlhdCI6MTU3NjU3MzgxNSwic3ViIjo1fQ.Dz1YxY0fCAsNxrj8_KRrTgjk8T5g_DZ2-D5TjUmT9dg"
# output
{
    "email": "test@gmail.com",
    "username": "test",
    "password": null,
    "public_id": "5f8abe86-83dc-47d7-a7ee-2808d35124d7"
}
```

Log out:

```shell
# URL=http://127.0.0.1:5000
URL=https://flask-restplus-boilerplate.herokuapp.com
curl -X POST -i "${URL}/api/v1/auth/logout" \
    -H "Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1NzczMjg3OTAsImlhdCI6MTU3NzI0MjM4NSwic3ViIjoxNH0.nRebBwsrIGBrGCclKVAB17F_QmiUE9nJVAdtzfThzUk"
# output
"Logout successfully"
```

## 4.5. Admin user and celery task

Login:

```shell
# URL=http://127.0.0.1:5000
URL=https://flask-restplus-boilerplate.herokuapp.com
curl -X POST -i "${URL}/api/v1/auth/login" \
    -H "accept: application/json" \
    -H "Content-Type: application/json" \
    -d "{ \"email\": \"admin@gmail.com\", \"password\": \"admin\"}"
# output
{
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1Nzc0MTQzOTQsImlhdCI6MTU3NzMyNzk4OSwic3ViIjowfQ.bKLTgo-rv9jeqm3bwH3X1VnkOtDVvujh5mxZHW-EX7c"
}
```

List all user:

See log file for more detail:

[app.DEBUG.log](log/app.DEBUG.log)
[celery.DEBUG.log](log/celery.DEBUG.log)

```shell
# URL=http://127.0.0.1:5000
URL=https://flask-restplus-boilerplate.herokuapp.com
curl -X GET -i "${URL}/api/v1/user/" \
    -H "accept: application/json" \
    -H "Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1NzY3NDc4NTYsImlhdCI6MTU3NjY2MTQ1MSwic3ViIjowfQ.UpLjwQDgTJor1xDPP2AxrHSo3_1Koxk2N1hYp5qPmwY"
# output
{
    "data": [
        {
            "email": "admin@gmail.com",
            "username": "admin",
            "password": null,
            "public_id": "196e9bad1d1541c9b858e35ee1e8642b"
        },
        {
            "email": "user1@gmail.com",
            "username": "user1",
            "password": null,
            "public_id": "cebd65d1af534fc19f43460e0a6871fa"
        },
        {
            "email": "user2@gmail.com",
            "username": "user2",
            "password": null,
            "public_id": "698ccc22fca04fada9f92c4ad7787b2e"
        },
        {
            "email": "user3@gmail.com",
            "username": "user3",
            "password": null,
            "public_id": "29f8652348fe4656b036328fa400031f"
        },
        {
            "email": "user4@gmail.com",
            "username": "user4",
            "password": null,
            "public_id": "c480b9afb9ba425ba3c6e476a8df330e"
        }
    ]
}
```

# 5. Full description and guide

https://medium.freecodecamp.org/structuring-a-flask-restplus-web-service-for-production-builds-c2ec676de563

or [here](How_to_structure_a_Flask-RESTPlus_web_service_for_production_builds.pdf)


# 6. Contributing
If you want to contribute to this flask restplus boilerplate, clone the repository and just start making pull requests.

```
https://github.com/cosmic-byte/flask-restplus-boilerplate.git
```

# 7. Response format message convention

With **success** response, status code is 2xx and format message arbitrary

With **fail** response, status code is differ than 2xx and format message:

```python
{
    "message": "content of fail message"
}
````
