FROM python:3.12.2-slim-bullseye

WORKDIR /usr/src/DPS

RUN apt-get update && apt-get install -y netcat && apt-get install -y poppler-utils

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /usr/src/DPS/entrypoint.sh
RUN chmod +x /usr/src/DPS/entrypoint.sh

COPY . .

ENTRYPOINT [ "/usr/src/DPS/entrypoint.sh" ]