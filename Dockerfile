FROM python:3.7-alpine
# Set environment variables.
# PYTHONDONTWRITEBYTECODE prevents Python from writing pyc files to disc.
# PYTHONUNBUFFERED Prevents Python from buffering stdout and stderr.
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk add --update --no-cache chromium-chromedriver chromium

COPY requirements.txt requirements.txt

RUN apk add --no-cache --virtual .build-deps gcc libc-dev libxslt-dev && \
    apk add --no-cache libxslt && \
    pip install --no-cache-dir -r requirements.txt && \
    apk del .build-deps

WORKDIR /app
COPY . /app

ENV LOGIN="defined in Dockerfile ARG"
ENV PASSWORD="defined in Dockerfile ARG"
ENV FLASK_ENV=prod

EXPOSE 8080
CMD [ "python", "./app.py" ]
