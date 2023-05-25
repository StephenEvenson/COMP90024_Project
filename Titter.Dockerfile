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
    && pip install -r backend/data_process/requirements.txt


CMD ["mpiexec", "-n", "2", "python", "-m", "backend.data_process.process_data"]