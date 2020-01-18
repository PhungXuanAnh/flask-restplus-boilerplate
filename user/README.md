FLASK RESTFUL API BOILER-PLATE WITH JWT

- [1. Deploy](#1-deploy)
  - [1.1. Install required packages](#11-install-required-packages)
  - [1.2. Create database](#12-create-database)
  - [1.3. Boot up rabbitmq and start celery worker](#13-boot-up-rabbitmq-and-start-celery-worker)
  - [1.4. Run test](#14-run-test)
  - [1.5. Run app](#15-run-app)
  - [1.6. Run all command](#16-run-all-command)
- [2. Viewing api in swagger and trying test](#2-viewing-api-in-swagger-and-trying-test)
- [3. Test using curl](#3-test-using-curl)
  - [3.1. Test publish api](#31-test-publish-api)
  - [3.2. Logging of this user api](#32-logging-of-this-user-api)
  - [3.3. Guide about token for normal user and admin](#33-guide-about-token-for-normal-user-and-admin)
  - [3.4. Normal user](#34-normal-user)
  - [3.5. Admin user and celery task](#35-admin-user-and-celery-task)
- [4. Full description and guide](#4-full-description-and-guide)
- [5. Contributing](#5-contributing)
- [6. Response format message convention](#6-response-format-message-convention)

# 1. Deploy
## 1.1. Install required packages

`pip install -r requirements.txt`
    
## 1.2. Create database

By default, this sample app using sqlite, if you want to change to postgres:

```shell
docker-compose up -d postgres
docker-compose ps
```

Change config in file [config.py](app/main/config.py)

NOTE: if you add more model to model folder, it must be import in method **create_app** in file [__init__.py](app/main/__init__.py)

Then run:

```shell
make db_migrate
make db_upgrade
```

## 1.3. Boot up rabbitmq and start celery worker

```shell
docker-compose up -d rabbitmq
docker-compose ps
```

## 1.4. Run test

**TODO:** run test is failed, fix this

`make tests`

## 1.5. Run app

`make run`

or 

`make run-gunicorn`

## 1.6. Run all command

`make all`

# 2. Viewing api in swagger and trying test 

http://127.0.0.1:5000/api/v1/


# 3. Test using curl

## 3.1. Test publish api

```shell
curl -X GET -i "http://127.0.0.1:5000/api/v1/user/publish"
```

## 3.2. Logging of this user api

See log message in folder log

## 3.3. Guide about token for normal user and admin

Authorization header is in the following format:

- Key: Authorization
- Value: "token_generated_during_login"

For testing authorization, url for getting all user requires an admin token while url for getting a single
user by public_id requires just a regular authentication.

## 3.4. Normal user

Create user:

```shell
curl -X POST -i "http://127.0.0.1:5000/api/v1/user/" \
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
curl -X POST -i "http://127.0.0.1:5000/api/v1/auth/login" \
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
curl -X GET -i "http://127.0.0.1:5000/api/v1/user/5f8abe86-83dc-47d7-a7ee-2808d35124d7" \
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
curl -X POST -i "http://127.0.0.1:5000/api/v1/auth/logout" \
    -H "Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1NzczMjg3OTAsImlhdCI6MTU3NzI0MjM4NSwic3ViIjoxNH0.nRebBwsrIGBrGCclKVAB17F_QmiUE9nJVAdtzfThzUk"
# output
"Logout successfully"
```

## 3.5. Admin user and celery task

Login:

```shell
curl -X POST -i "http://127.0.0.1:5000/api/v1/auth/login" \
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
curl -X GET -i "http://127.0.0.1:5000/api/v1/user/" \
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

# 4. Full description and guide

https://medium.freecodecamp.org/structuring-a-flask-restplus-web-service-for-production-builds-c2ec676de563

or [here](How_to_structure_a_Flask-RESTPlus_web_service_for_production_builds.pdf)


# 5. Contributing
If you want to contribute to this flask restplus boilerplate, clone the repository and just start making pull requests.

```
https://github.com/cosmic-byte/flask-restplus-boilerplate.git
```

# 6. Response format message convention

With **success** response, status code is 2xx and format message arbitrary

With **fail** response, status code is differ than 2xx and format message:

```python
{
    "message": "content of fail message"
}
````
