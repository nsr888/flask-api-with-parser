# Python Flask-Restful API
Python Flask-Restful endpoint to retrive list of user's friends from http://ok.ru social network.

__Tech stack:__ Python Flask RESTful, Selenium, BeautifulSoup, Docker, uwsgi, nginx


<img width="1223" alt="screenshot" src="https://user-images.githubusercontent.com/12528718/134766130-57810cb4-0bc4-4095-b8df-361183190f90.png">

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
