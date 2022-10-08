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
$ git clone https://github.com/forDeFan/FastAPI_apis_example.git
$ cd FastAPI_apis_example
```

B. Run docker build to get app running

```
$ docker-compose up -d --build
```
<br>
Docs available at <div style="display: inline">http://localhost:8008/docs</div>
<br>
The app in basic mode available at <div style="display: inline">http://localhost:8008/</div>
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

The app uses local Postgres folder to keep all data in it (data in project root). 
<br>
If docker images to be removed for new build also data folder must be deleted for fresh DB to be settled by docker in next run. 
<br>
Standard error output when building image again when data folder present will be:
```
PermissionError: [Errno 13] Permission denied: 'your_app_root/data/postgres'...
```
<br>
If in need to remove db folder (all data lost) simply use:

```
$ cd FastAPI_apis_example
$ sudo rm -fr data
```
