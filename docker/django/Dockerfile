FROM python:3.7-slim

ENV PYTHONUNBUFFERED 1

ENV UWSGI_INI /opt/app/config/uwsgi.ini
ENV APP_DIR /opt/app
ENV PYTHONPATH "${PYTHONPATH}:${APP_DIR}/"

# Install required applications
RUN apt-get update \
    && apt-get install -y \
        gcc g++ supervisor nginx nginx-extras cron \
        wget curl apt-transport-https gnupg2 \
    && curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/9/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql17 mssql-tools unixodbc-dev \
    && rm -rf /var/lib/apt/lists/*
RUN wget https://dl.eff.org/certbot-auto -O /opt/certbot && chmod a+x /opt/certbot \
    && /opt/certbot --install-only --non-interactive


RUN mkdir -p /var/log/app

WORKDIR ${APP_DIR}

COPY Pipfile Pipfile.lock ${APP_DIR}/
RUN pip install -U pip==18.1 pipenv==2018.10.9 \
    && pipenv install --system --deploy

COPY ./config ${APP_DIR}/config

RUN ln -s ${APP_DIR}/config/supervisord.conf /etc/supervisor/conf.d/supervisord.conf \
    && rm /etc/nginx/sites-enabled/default \
    && rm /etc/nginx/nginx.conf  \
    && ln -s ${APP_DIR}/config/nginx/nginx.conf /etc/nginx/sites-enabled/default \
    && ln -s ${APP_DIR}/config/nginx/base.conf /etc/nginx/nginx.conf

ADD ./backend ${APP_DIR}/backend

CMD ${APP_DIR}/backend/scripts/init.sh
