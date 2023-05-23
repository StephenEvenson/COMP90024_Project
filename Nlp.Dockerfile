FROM bitnami/pytorch:latest

USER root
WORKDIR /data/app

COPY . .

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


RUN apt-get update \
    && apt-get -y install gcc libffi-dev  \
    && pip install --upgrade pip setuptools wheel  \
    && pip install -r backend/nlp/requirements.txt

# 指明监听的端口
EXPOSE 8000

# 运行的命令
CMD ["uvicorn", "backend.nlp.nlp_server:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]