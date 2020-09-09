FROM python:3.8.5

ENV PYTHONNUMBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY . /code/
RUN pip install -r requirements.txt
