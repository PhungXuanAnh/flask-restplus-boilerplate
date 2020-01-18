FLASK RESTFUL API BOILER-PLATE WITH JWT

- [1. Deploy](#1-deploy)
  - [1.1. Development](#11-development)
  - [1.2. Staging](#12-staging)
  - [1.3. Production](#13-production)
  - [1.4. Prepare database](#14-prepare-database)
- [2. Viewing api in swagger and trying test](#2-viewing-api-in-swagger-and-trying-test)
- [3. Test using curl](#3-test-using-curl)
  - [3.1. Logging](#31-logging)
  - [3.2. Guide about token for normal user and admin](#32-guide-about-token-for-normal-user-and-admin)
  - [3.3. Normal user](#33-normal-user)
  - [3.4. Admin user](#34-admin-user)
- [4. Full description and guide](#4-full-description-and-guide)
- [5. Contributing](#5-contributing)

# 1. Deploy

## 1.1. Development

`make up-development`

## 1.2. Staging

`make up-staging`

## 1.3. Production

`make up-production`

## 1.4. Prepare database

Migrate database

`make db_upgrade`

We can connect directly to postgres or connect to posgres though [PGBouncer](https://www.compose.com/articles/how-to-pool-postgresql-connections-with-pgbouncer/)

To switch between 2 types of connections, change port in [config.py](user/app/main/config.py)

If you want to add more user to PGBouncer, using file [generate-userlist](postgres/pgbouncer/generate-userlist)

Reference [here](https://www.pgbouncer.org/config.html#authentication-file-format)

```shell
./generate-userlist postgres >> userlist.txt
Enter password: 
```

Test connnection:
```shell
pgcli -U admin -h localhost -p 6432 -d flask_sample_app

Enter password:
123456
```

Then change file **config.py**

# 2. Viewing api in swagger and trying test 

http://127.0.0.1:5000/api/v1/

# 3. Test using curl

## 3.1. Logging

See log message in folder log

## 3.2. Guide about token for normal user and admin

Authorization header is in the following format:

- Key: Authorization
- Value: "token_generated_during_login"

For testing authorization, url for getting all user requires an admin token while url for getting a single
user by public_id requires just a regular authentication.

## 3.3. Normal user

Create user:

```shell
curl -X POST "http://127.0.0.1:5000/api/v1/user/" -H "accept: application/json" -H "Content-Type: application/json" -d "{ \"email\": \"test@gmail.com\", \"username\": \"test\", \"password\": \"1234\"}"
# output
{
    "status": "success",
    "message": "Successfully registered.",
    "Authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1NzY2NTM4MzMsImlhdCI6MTU3NjU2NzQyOCwic3ViIjoyfQ.vqunxFCKwFb5boL75jmQJC1U3dVyc9BVJ8MBGIMSTFM"
}
```

Login:

```shell
curl -X POST "http://127.0.0.1:5000/api/v1/auth/login" -H "accept: application/json" -H "Content-Type: application/json" -d "{ \"email\": \"test@gmail.com\", \"password\": \"1234\"}"
# output
{
    "status": "success",
    "message": "Successfully logged in.",
    "Authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1NzY2NTI2OTcsImlhdCI6MTU3NjU2NjI5Miwic3ViIjoxfQ.shyR184DyHtu8j5MZmxOQtn1RG8TSzsCRRsnwLGXqd0"
}
```

Get user:

```shell
curl -X GET "http://127.0.0.1:5000/api/v1/user/5f8abe86-83dc-47d7-a7ee-2808d35124d7" -H "accept: application/json" -H "Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1NzY2NjAyMjAsImlhdCI6MTU3NjU3MzgxNSwic3ViIjo1fQ.Dz1YxY0fCAsNxrj8_KRrTgjk8T5g_DZ2-D5TjUmT9dg"
# output
{
    "email": "test@gmail.com",
    "username": "test",
    "password": null,
    "public_id": "5f8abe86-83dc-47d7-a7ee-2808d35124d7"
}
```

## 3.4. Admin user

Login:

```shell
curl -X POST "http://127.0.0.1:5000/api/v1/auth/login" -H "accept: application/json" -H "Content-Type: application/json" -d "{ \"email\": \"admin@gmail.com\", \"password\": \"admin\"}"
# output
{
    "status": "success",
    "message": "Successfully logged in.",
    "Authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1NzY2NjA5NDksImlhdCI6MTU3NjU3NDU0NCwic3ViIjowfQ.Ky4q-Uu9oG9fHtWQzyEkyFUF6qDZbBwXYh8L8uz7Ltw"
}
```

List all user:

```shell
curl -X GET "http://127.0.0.1:5000/api/v1/user/" -H "accept: application/json" -H "Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1NzY5MTE5NTEsImlhdCI6MTU3NjgyNTU0Niwic3ViIjowfQ.bWwd1z3sHPUTBLuNQDQ-rkOkZ_H8yMT1zjUIBUaVDrE"
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
