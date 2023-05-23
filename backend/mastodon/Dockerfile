FROM python:3.10

USER root
WORKDIR /data/app

COPY . .


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


RUN apt-get -y install gcc libffi-dev  \
    && pip install --upgrade pip  \
    && pip install -r requirements.txt  \
    && chmod +x start.sh  \
    && chmod +x wait-for-it.sh \


ENTRYPOINT ["/data/app/start.sh"]