# Social network http://ok.ru profile parser

## Create `ok.env` file

```
LOGIN=""
PASSWORD=""
```

## Build

```
docker build -t python-alpine-chromedriver .
```

## Run

```
docker run --env-file ok.env --rm -p 8080:8080 --name ok_friends_run python-alpine-chromedriver
```

## Tests

```
docker run --entrypoint "python" --env-file ok.env --rm -p 8080:8080 --name ok_friends_testapp python-alpine-chromedriver -m tests.testapp
docker run --entrypoint "python" --env-file ok.env --rm -p 8080:8080 --name ok_friends_testcommon python-alpine-chromedriver -m tests.testcommon
```
