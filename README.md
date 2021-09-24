# Social network http://ok.ru profile parser

## Create ok.env file

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
docker run --env-file ok.env --rm -p 8080:8080 --name sl python-alpine-chromedriver
```

## Tests

```
docker run --entrypoint "python" --env-file ok.env --rm -p 8080:8080 --name sl python-alpine-chromedriver -m tests.testapp
docker run --entrypoint "python" --env-file ok.env --rm -p 8080:8080 --name sl python-alpine-chromedriver -m tests.testcommon
```
