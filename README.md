# Python Flask-Restful API
Python Flask-Restful endpoint to retrive list of user's friends from http://ok.ru social network.

__Tech stack:__ Python Flask RESTful, Selenium, BeautifulSoup, unittest, Docker, uwsgi, nginx

<img width="1348" alt="screenshot" src="https://user-images.githubusercontent.com/12528718/134766709-f0bff3a3-b026-4c12-b59a-a8814a7d8067.png">

# How to launch

1) Create `.env` file (fill LOGIN, PASSWORD and PROXY fields):

```
LOGIN=
PASSWORD=
FLASK_ENV=prod
PROXY=
```

2) Build:

```
make build
```

3) Run:

```
make run
```

3) Open in browser: 
```
http://localhost:8080/ok/friends?id=<user_id>&limit=<fields_limit>&timeout=<time_limit>
```
