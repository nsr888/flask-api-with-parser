# Python Flask-Restful API
Python Flask-Restful endpoint to retrive list of user's friends from http://ok.ru social network.

<img width="1187" alt="Снимок экрана 2021-09-25 в 01 07 29" src="https://user-images.githubusercontent.com/12528718/134744579-99b4420e-f462-4e69-abcd-eb372b810870.png">

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
http://localhost:8080/ok/friends?id=<user id>&limit=<fields limit>&timeout=<time limit>
```
