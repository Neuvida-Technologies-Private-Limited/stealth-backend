FROM python:3.11

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src

RUN pip install --upgrade pip 

COPY ./requirements.txt . 

RUN pip install -r  requirements.txt
RUN pip install pre-commit
RUN apt-get update && apt-get install -y netcat-openbsd
# copy entrypoint.sh
COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /usr/src/entrypoint.sh
RUN chmod +x /usr/src/entrypoint.sh

COPY . .

# run entrypoint.sh
ENTRYPOINT ["/usr/src/entrypoint.sh"]

EXPOSE 8000