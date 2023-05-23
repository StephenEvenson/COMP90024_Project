FROM python:3.10

WORKDIR /data/app

COPY . .

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


RUN apt-get -y install gcc libffi-dev && pip install --upgrade pip && pip install -r backend/nlp/requirements.txt

# 指明监听的端口
EXPOSE 8080

# 运行的命令
CMD ["uvicorn", "backend.nlp.nlp_server:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]