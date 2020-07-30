FROM python:3.7-slim

RUN pip install pipenv

RUN groupadd --gid 1000 monitoring && \
    useradd --create-home --system --uid 1000 --gid monitoring monitoring && \
WORKDIR /home/monitoring

# Dev defaults?
ENV RABBITMQ_SERVICE_HOST rabbitmq
ENV RABBITMQ_SERVICE_PORT 5672
ENV RABBITMQ_HTTP_PORT 15672
ENV RABBITMQ_VHOST /
ENV RABBITMQ_USER guest
ENV RABBITMQ_PASSWORD guest

COPY Pipfile* /home/monitoring/
RUN pipenv install --system --deploy
USER monitoring

RUN mkdir /home/monitoring/.postgresql &&  mkdir /home/monitoring/.postgresql-rw &&  mkdir /home/monitoring/.postgresql-action

COPY --chown=monitoring . /home/monitoring