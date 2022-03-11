FROM python:3.9-buster

WORKDIR /celery

ENV PATH="${PATH}:/root/.local/bin"
ENV PYTHONPATH=.

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY src/ .

ENTRYPOINT celery -A src.task worker --loglevel=info