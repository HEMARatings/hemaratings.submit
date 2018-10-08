FROM starter_frontend:latest as frontend

RUN yarn build

FROM python:3.7

ENV PYTHONUNBUFFERED 1

ENV UWSGI_INI /opt/app/config/uwsgi.ini
ENV APP_DIR /opt/app
ENV PYTHONPATH "${PYTHONPATH}:${APP_DIR}/"

# Install required applications
RUN apt-get update \
    && apt-get install -y uwsgi-plugin-python3 \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /var/log/app

WORKDIR ${APP_DIR}

ARG INSTALL_DEV

COPY Pipfile Pipfile.lock ${APP_DIR}/
RUN pip install pipenv==2018.7.1 \
    && pipenv install --system --deploy \

COPY ./config ${APP_DIR}/config
ADD ./backend ${APP_DIR}/backend

RUN chmod +x ${APP_DIR}/backend/init.sh

CMD ${APP_DIR}/backend/init.sh
