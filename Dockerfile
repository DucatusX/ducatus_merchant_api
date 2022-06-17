FROM python:3.7

ENV PYTHONUNBUFFERED=1

RUN mkdir /code
WORKDIR /code

RUN pip install --upgrade pip==20.2.4
RUN apt-get update && apt-get install -y netcat
COPY requirements /code/requirements
RUN pip install -r requirements/dev.txt

EXPOSE 8000

COPY . /code/

