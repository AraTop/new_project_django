FROM python:3

WORKDIR /code

COPY ./requirements .

RUN pip install -r requirements

COPY . .