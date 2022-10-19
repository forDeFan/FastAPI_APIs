<h1>FastAPI examples</h1>

Readme and app itself - in live development.

## The plan

### Short term goals:

* Implementation of FastAPI in Rest and GraphQL approach
* API versioning for REST and GraphQL
* Dockerization
* Implementation of user login along with authentication and authorization
* Implementation of Front End layer with usage of server side engine Jinja2
* Unit testing, integration testing
* Usage of conventional commit messages
* OWASP API and Web app rules implementation

### Long term goals:

* Web app pen testing
* Docker deployment in Heroku
* App health monitoring in cloud
* Web service load testing and performance tuning

### To run app at current stage

1. Prerequisites

* Python 3.8 or higher installed
* Docker installed

2. To run the app

A. Install codebase:

```
$ git clone https://github.com/forDeFan/FastAPI_APIs.git
$ cd FastAPI_APIs
```

B. Run docker build to get app running

```
$ docker-compose up -d --build
```
<br>
<strong>THE APP AVAILABLE at <div style="display: inline">http://localhost:8008/</div></strong>
<br>
<br>
Docs available at <div style="display: inline">http://localhost:8008/docs</div>
<br><br>

3. Docker interaction

While in project root.
<br><br>
To start containers up:

```
$ docker-compose up -d
```

To stop containers down:

```
$ docker-compose stop
```

4. To connect to DB from outside container by Database Menager (ex. DBeaver).

a) get a postgres container IP by

```
$ docker inspect {container_id}
```

b) set DB connection to that IP:port, DB, DB username and password indicated in .env




<br><br>
Aditional features:

If persistent data folder needed in project root - uncomment lines in docker-compose:

```
volumes: 
- ./data/postgres:/var/lib/postgresql/data
```

If docker images to be removed for new build also persistent data folder must be deleted for fresh DB (to be created by docker in next run). 

Standard error output when building image again when data folder present will be:
<br>

```
PermissionError: [Errno 13] Permission denied: 'your_app_root/data/postgres'...
```

If in need to remove local persistent data folder (all data lost) simply use:

```
$ cd FastAPI_APIs
$ sudo rm -fr data
```
