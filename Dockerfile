FROM alpine:3.10
# Set environment variables.
# PYTHONDONTWRITEBYTECODE prevents Python from writing pyc files to disc.
# PYTHONUNBUFFERED Prevents Python from buffering stdout and stderr.
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk add --update --no-cache chromium-chromedriver chromium

RUN apk add --no-cache python3 python3-dev && \
    if [ ! -e /usr/bin/python ]; then ln -sf python3 /usr/bin/python ; fi && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --no-cache --upgrade pip setuptools wheel && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi

# pip install -r requirements.txt
COPY requirements.txt requirements.txt
RUN apk add --no-cache --virtual .build-deps gcc libc-dev libxslt-dev linux-headers && \
    apk add --no-cache libxslt && \
    pip install --no-cache-dir -r requirements.txt && \
    apk del .build-deps

# nginx and uwsgi install
RUN apk add --no-cache nginx uwsgi uwsgi-python3 supervisor
# RUN rm /etc/nginx/conf.d/default.conf
# RUN rm -r /root/.cache

# Copy the Nginx global conf
COPY nginx.conf /etc/nginx/
# Copy the Flask Nginx site conf
COPY flask-site-nginx.conf /etc/nginx/conf.d/
# Copy the base uWSGI ini file to enable default dynamic uwsgi process number
COPY uwsgi.ini /etc/uwsgi/
# Custom Supervisord config
COPY supervisord.conf /etc/supervisord.conf

WORKDIR /app
COPY . /app

ENV LOGIN="defined in Dockerfile ARG"
ENV PASSWORD="defined in Dockerfile ARG"
ENV FLASK_ENV=prod

EXPOSE 8080
CMD ["/usr/bin/supervisord"]
# CMD [ "python", "./app.py" ]
