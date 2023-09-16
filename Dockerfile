FROM python:3.11

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN pip install --upgrade pip 

COPY ./requirements.txt . 

RUN pip install -r  requirements.txt

RUN pip install pre-commit

COPY . /app

COPY ./entrypoint.sh /

ENTRYPOINT [ "sh", "entrypoint.sh"]

EXPOSE 8000