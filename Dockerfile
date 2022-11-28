FROM python:3.7-slim
LABEL maintainer="Carlos Correa <carlosx-34@hotmail.com>"
EXPOSE 3000
WORKDIR /srv/app
COPY . .
RUN rm -rf infrastructure
RUN apt-get update && apt-get install -y --no-install-recommends build-essential
RUN pip install --no-cache-dir pipenv
RUN pipenv install --system --deploy
RUN apt-get purge -y --auto-remove build-essential
RUN apt-get update && apt-get install -y --no-install-recommends nginx supervisor
COPY infrastructure/default.conf /etc/nginx/conf.d/default.conf
COPY infrastructure/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

CMD supervisord
