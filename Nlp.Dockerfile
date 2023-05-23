FROM python:3.10

USER root
WORKDIR /data/app

COPY . .

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


RUN apt-get update \
    && apt-get -y install gcc libffi-dev  \
    && pip install --upgrade pip setuptools wheel  \
    && pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu \
    && pip install -r backend/nlp/requirements.txt


EXPOSE 8000


CMD ["uvicorn", "backend.nlp.nlp_server:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]