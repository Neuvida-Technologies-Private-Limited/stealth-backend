FROM python:3.11

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src

RUN pip install --upgrade pip 

COPY ./requirements.txt . 

RUN pip install -r  requirements.txt

COPY . .

EXPOSE 8000