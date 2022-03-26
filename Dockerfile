FROM python:3.9.6-slim-buster

RUN useradd snowebsvg

EXPOSE 8000

ENV PYTHONUNBUFFERED=1 \
    PORT=8000

RUN apt-get update --yes --quiet && apt-get install -y curl
RUN apt-get upgrade -y ca-certificates
RUN curl -sL https://deb.nodesource.com/setup_14.x | bash -
RUN apt-get install --yes --quiet --no-install-recommends \
    build-essential \
    libpq-dev \
    libmariadbclient-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libwebp-dev \
    gettext \
    python3-wand \
    nodejs \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /snowebsvg
COPY --chown=snowebsvg:snowebsvg . .

RUN pip install "gunicorn==20.0.4"
RUN pip install -r requirements.txt
RUN npm install
RUN npm run build

USER snowebsvg

CMD set -xe; gunicorn wsgi:application -k gevent --workers 3 --timeout 30 --env DJANGO_SETTINGS_MODULE=settings.production --bind 0.0.0.0:8000
