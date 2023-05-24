FROM python:3.10

USER root
WORKDIR /data/app

COPY . .

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


RUN apt-get update \
    && apt-get -y install gcc libffi-dev  \
    && pip install --upgrade pip  \
    && pip install -r backend/nlp/requirements.txt \
    && chmod +x backend_start.sh  \
    && chmod +x wait-for-it.sh


EXPOSE 8000

ENTRYPOINT ["/data/app/backend_start.sh"]